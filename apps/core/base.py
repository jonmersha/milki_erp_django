from django.db import models
from django.utils import timezone
from django.conf import settings

class BaseModel(models.Model):
    """
    Abstract base class for common fields.
    Automatically authorizes records and timestamps authorization.
    """
    is_authorized = models.BooleanField(default=False)
    authorization_time = models.DateTimeField(null=True, blank=True, default=timezone.now, editable=False)  # auto timestamp
    authorized_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
    null=True,
        blank=True,
        editable=False,  # hide from admin/forms
        related_name='authorized_%(class)s_set'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Automatically set authorization time if not already set
        if self.is_authorized and self.authorization_time is None:
            self.authorization_time = timezone.now()
        super().save(*args, **kwargs)
# class UserAction(models.Model):
    