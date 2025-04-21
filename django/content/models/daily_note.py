from users.models.user import User

from django.db import models


class NoteType(models.IntegerChoices):
    DAYLY      = 1, 'Dayly Note'
    WEEKLY     = 2, 'Weekly Note'

class DaylyNote(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    action = models.PositiveSmallIntegerField(
        choices=NoteType.choices,
        verbose_name='Acction'
    )
    
    def __str__(self):
        return self.id
