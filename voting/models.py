from django.db import models
from account.models import CustomUser
# Create your models here.


class Voter(models.Model):
    PREFER_NOT_TO_SAY = "Prefer not to say"
    MALE = "Male"
    FEMALE = "Female"
    
    GENDER_CHOICES = [
        (PREFER_NOT_TO_SAY, "Prefer not to say"),
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]
    
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, unique=True)  # Used for OTP
    dob = models.DateField()
    sex = models.CharField(max_length=20, choices=GENDER_CHOICES, default=PREFER_NOT_TO_SAY )
    card_uid = models.CharField(max_length=12, null=False, unique=True)
    verified = models.BooleanField(default=False)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_vote = models.IntegerField()
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class Candidate(models.Model):
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates")
    bio = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname


class Votes(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

