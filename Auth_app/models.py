from django.db import models

# Create your models here.
question_choices=(
    ('WBD', 'What is your birthdate?'),
    ('OPN','What is your Old Phone Number?'),
    ('YPN','What is your Petname?'),
)
gender_choices = (
    ('M', 'Male'),
    ('F','FeMale'),
)
class Regmodel(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    usrname = models.CharField(max_length=120)
    email = models.EmailField()
    mobile = models.IntegerField()
    password = models.CharField(max_length=120)
    confirm_password = models.CharField(max_length=120, null=True, blank=True)
    security_question = models.CharField(max_length=3, choices=question_choices, null=True, blank=True)
    enter_answer = models.CharField(max_length=120, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=gender_choices, null=True, blank=True)

    def __str__(self):
        return self.usrname