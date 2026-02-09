from django.db import models
from django.utils.translation import gettext as _
# Create your models here.

#We create dummy model for display it in the control panel

class OrderReport(models.Model):
    class Meta:
        verbose_name_plural = _('Order')
