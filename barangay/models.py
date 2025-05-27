from django.db import models
from django.contrib.auth.models import User
from django import forms

PUROK_CHOICES = [
    ('Purok 1 Proper', 'Purok 1 Proper'),
    ('Purok 1 Don Julio', 'Purok 1 Don Julio'),
    ('Purok 2 Proper', 'Purok 2 Proper'),
    ('Purok 2 Don Julio', 'Purok 2 Don Julio'),
    ('Purok 3 Proper', 'Purok 3 Proper'),
    ('Purok 3 Don Julio', 'Purok 3 Don Julio'),
    ('Purok 4 Proper', 'Purok 4 Proper'),
    ('Purok 4 Don Julio', 'Purok 4 Don Julio'),
    ('Purok 5 Proper', 'Purok 5 Proper'),
    ('Purok 5 Don Julio', 'Purok 5 Don Julio'),
    ('Purok 6', 'Purok 6'),
    ('Purok 7', 'Purok 7'),
    ('Purok 8', 'Purok 8'),
    ('Purok 9', 'Purok 9'),
    ('Purok Pag-asa', 'Purok Pag-asa'),
    ('Purok Tower', 'Purok Tower'),
]


class ResidentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    age = models.IntegerField()
    purok = models.CharField(max_length=50, choices=PUROK_CHOICES)
    email = models.EmailField(null=False, blank=False)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    

    def __str__(self):
        return self.fullname

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_ACTION', 'In Action'),
        ('RESOLVED', 'Resolved'),
    ]
    
    complaint_text = models.TextField()
    address = models.CharField(max_length=255, default="Not Provided")  # add default here
    email = models.EmailField(default="not_provided@example.com")       # add default here
    contact_number = models.CharField(max_length=20, default="Not Provided")  # add default here
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    date_filed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    resident = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # other fields and methods...

    def __str__(self):
        return self.complaint_text[:50]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    purok = models.CharField(max_length=50, choices=PUROK_CHOICES)

    def __str__(self):
        return self.user.username
