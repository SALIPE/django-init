from content.models.content_note import ContentType
from users.models.user import Staff, User

from django.db import models


class UserCalls(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=False, null=False)
    
    def __str__(self):
        return self.id
