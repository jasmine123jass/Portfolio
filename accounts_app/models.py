from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, default="AI/ML Specialist and Full Stack Developer")
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.TextField(blank=True, default="Python, Django, Machine Learning, Deep Learning, NLP")
    education = models.TextField(blank=True, default="B.Tech CSE (AI/ML) at LPU")
    experience = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, default="+91 7331180690")
    location = models.CharField(max_length=100, blank=True, default="Visakhapatnam, India")
    github = models.URLField(blank=True, default="https://github.com/jasmine123jass")
    linkedin = models.URLField(blank=True, default="https://linkedin.com/in/srujitha-jasmine-baggam")
    
    def __str__(self):
        return self.name or self.user.username
    
    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',')]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()