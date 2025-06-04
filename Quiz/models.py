from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class QuesModel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)
    time_limit = models.IntegerField(default=60, help_text="Time limit in seconds")
    points = models.IntegerField(default=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.question

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuesModel, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'question']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    max_attempts = models.IntegerField(default=3)
    last_attempt = models.DateTimeField(null=True, blank=True)
    total_score = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
