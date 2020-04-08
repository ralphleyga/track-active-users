from django.db import models
from django.conf import settings


USER_STATUS = (
    (0, 'offline'),
    (1, 'active'),
    (2, 'away'),
)

class ActiveUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.IntegerField(choices=USER_STATUS)
    last_active = models.DateField()

    def __str__(self):
        return f'{self.user.username}'
