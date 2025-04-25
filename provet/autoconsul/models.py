# some ORM for later searching features

from django.db import models

class Patient(models.Model):
    name           = models.CharField(max_length=100)
    species        = models.CharField(max_length=100)
    breed          = models.CharField(max_length=100)
    gender         = models.CharField(max_length=10)
    neutered       = models.BooleanField(default=False)
    date_of_birth  = models.DateField()
    microchip      = models.CharField(max_length=50, blank=True, default='')
    weight         = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.species})"

class Consultation(models.Model):
    patient        = models.ForeignKey(Patient, 
        on_delete=models.CASCADE, 
        related_name="consultations",
        null=True, blank=True)
    date           = models.DateField(null=True, blank=True)
    time           = models.TimeField(null=True, blank=True)
    reason         = models.CharField(max_length=255, blank=True, default='')
    type           = models.CharField(max_length=50, blank=True, default='')
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consult {self.pk} on {self.date} at {self.time}"

class DischargeNote(models.Model):
    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name="note"
    )
    note_text    = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.consultation}"

class ClinicalNote(models.Model):
    consultation = models.ForeignKey(Consultation, 
        on_delete=models.CASCADE, 
        related_name="clinical_notes"
    )
    type    = models.CharField(max_length=50)
    note    = models.TextField()

    def __str__(self):
        return f"{self.type} note for consult {self.consultation.pk}"

class Procedure(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="procedures")
    date         = models.DateField()
    time         = models.TimeField()
    name         = models.CharField(max_length=255)
    code         = models.CharField(max_length=50)
    quantity     = models.IntegerField()
    total_price  = models.DecimalField(max_digits=12, decimal_places=2)
    currency     = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Medicine(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="medicines")
    name         = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="prescriptions")
    name         = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Food(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="foods")
    name         = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Supply(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="supplies")
    name         = models.CharField(max_length=255)
    quantity     = models.IntegerField(default=1)
    def __str__(self):
        return self.name

class Diagnostic(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="diagnostics")
    description  = models.TextField()
    def __str__(self):
        return f"Diagnostic for consult {self.consultation.pk}"
