from users.models.user import Staff, User

from django.db import models


class LogAction(models.IntegerChoices):
    LOGIN          = 1, 'User login'
    USER_DATA_UPDATE    = 2, 'User data update'

class UserLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='logs',
        verbose_name='User'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Timestamp'
    )
    action = models.PositiveSmallIntegerField(
        choices=LogAction.choices,
        verbose_name='Acction'
    )

    class Meta:
        verbose_name = 'UserLog'
        verbose_name_plural = 'UserLogs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_action_display()} - {self.timestamp}"
    
class StaffLog(models.Model):
    user = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='logs',
        verbose_name='User'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Timestamp'
    )
    action = models.PositiveSmallIntegerField(
        choices=LogAction.choices,
        verbose_name='Acction'
    )

    class Meta:
        verbose_name = 'StaffLog'
        verbose_name_plural = 'StaffLogs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_action_display()} - {self.timestamp}"
    


    
    
