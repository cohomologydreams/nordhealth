# provet/autoconsul/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Route: GET /
    # Description: Displays the upload page
    # View: views.upload
    path('', views.upload, name='upload'),

    # Route: POST /generate/
    # Description: Handles form submission to generate content using some LLM logic
    # View: views.generate
    path('generate/', views.generate, name='generate'),

    # Route: POST /delete/<note_id>/
    # Description: Deletes a note with the given ID from the system.
    # URL Parameter: note_id (int) – The ID of the note to delete.
    # View: views.delete_note
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
]
