import os, sys
import json
import openai

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import Patient, Consultation, DischargeNote

from celery import shared_task
from celery_progress.backend import ProgressRecorder

openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_DIR = os.path.join(settings.BASE_DIR, '..', 'data')

def upload(request):
    """
    GET handler: show the upload/import form + stored records table.
    """
    server_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    notes = DischargeNote.objects.select_related('consultation__patient') \
                                 .order_by('-created_at')

    return render(request, 'autoconsul/upload.html', {
        'server_files': server_files,
        'notes': notes,
    })


@shared_task(bind=True)
def generate_discharge_note_async(self, data, consultation_id, model_name):
    """
    1) Build the prompt
    2) Call the LLM
    3) Parse the result
    4) Persist the DischargeNote
    5) Emit progress after each step via celery-progress.
    """
    recorder = ProgressRecorder(self)
    total_steps = 4

    prompt = build_llm_prompt(data)
    recorder.set_progress(1, total_steps, description="Prompt prepared")

    try:
        resp = openai.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
            timeout=30
        )
        recorder.set_progress(2, total_steps, description="LLM responded")
        note_text = resp.choices[0].message.content.strip()
    except Exception as e:
        recorder.set_progress(2, total_steps, description="LLM error")
        note_text = f"Error generating note: {e}"

    # Step 3: (Optional) parse/clean result
    recorder.set_progress(3, total_steps, description="Result parsed")

    # Step 4: Persist to DB
    consultation = Consultation.objects.get(pk=consultation_id)
    DischargeNote.objects.create(
        consultation=consultation,
        note_text=note_text
    )
    recorder.set_progress(4, total_steps, description="Note saved")

    return {"note": note_text}

 
def build_llm_prompt(data):
    prompt = (
        "You are a veterinary assistant at a busy veterinary clinic. "
        "You will be provided with a JSON object containing a single patient consultation, "
        "including patient demographics, reason for visit, clinical notes, procedures performed, "
        "medicines administered (with dosages if available), diagnostics run, and any supplies used. "
        "Your task is to output a single, cohesive paragraph that briefly summarizes what happened during the visit, such that:"
        "1) Lists any treatments or medications given, "
        "2) Highlights key observations, and "
        "3) Provides clear next-step instructions or precautions for the owner. "
        "Do not use any bullets, asterisks, lists, markdown, or any additional keys - just plain text in one paragraph.\n\n"
    )
    return prompt + json.dumps(data, indent=2)


def generate(request):
    """
    POST handler: enqueue the Celery task, then render immediately with a task_id for the progress bar widget.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")

    server_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]

    # Load JSON from upload or sample
    if request.FILES.get('file'):
        raw = request.FILES['file'].read().decode('utf-8')
    else:
        fname = request.POST.get('server_file')
        if not fname:
            return render(request, 'autoconsul/upload.html', {
                'server_files': server_files,
                'notes': DischargeNote.objects.select_related('consultation__patient')
                                              .order_by('-created_at'),
                'error': "Please upload a file or select a sample."
            })
        raw = open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8').read()

    data = json.loads(raw)

    # Persist Patient
    p = data.get('patient', {})
    patient, _ = Patient.objects.get_or_create(
        name=p.get('name',''),
        species=p.get('species',''),
        breed=p.get('breed',''),
        gender=p.get('gender',''),
        date_of_birth=p.get('date_of_birth'),
        microchip=p.get('microchip') or '',
        weight=p.get('weight','')
    )

    # Persist Consultation
    c = data.get('consultation', {})
    consultation = Consultation.objects.create(
        patient=patient,
        date=c.get('date'),
        time=c.get('time'),
        reason=c.get('reason',''),
        type=c.get('type','')
    )

    # Enqueue the background job
    # async_result = generate_discharge_note_async.delay(data, consultation.id)

    model_name = request.POST.get('model', 'gpt-4o')
    async_result = generate_discharge_note_async.delay(
        data,
        consultation.id,
        model_name
    )

    # Render page with the task_id for celery-progress to poll
    return render(request, 'autoconsul/upload.html', {
        'server_files': server_files,
        'notes': DischargeNote.objects.select_related('consultation__patient')
                                      .order_by('-created_at'),
        'message': "Generation in progress…",
        'task_id': async_result.id,
    })


def delete_note(request, note_id):
    """
    POST handler: delete the given DischargeNote and redirect back.
    """
    if request.method == "POST":
        get_object_or_404(DischargeNote, pk=note_id).delete()
    return redirect('upload')
