from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.TextField(null=True, blank=True)
    status = models.CharField(default='inactive', max_length=10)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def choices(self):
        return self.choice_set.all()

class Choice(models.Model):
    q = models.ForeignKey('poll.Question', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    @property
    def vote(self):
        return self.answer_set.count()

class Answer(models.Model):
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    ch = models.ForeignKey(Choice, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.u.first_name + '-' + self.ch.text