from users.models.user import User

from django.db import models


class ContentNote(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name='User',
        blank=False,
        null=False,
    )
    
    def __str__(self):
        return self.id
