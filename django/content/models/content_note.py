from users.models.user import User

from django.db import models
from django.db.models.functions import Upper


class ContentType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, unique=True, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Upper('description'),
                name='unique_upper_description'
            )
        ]

    def save(self, *args, **kwargs):
        if self.description:
            self.description = self.description.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description


class ContentNote(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=False, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
