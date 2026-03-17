from django.db import models


class Task(models.Model):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done'),
    ]

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
