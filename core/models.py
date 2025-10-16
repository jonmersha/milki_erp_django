from django.db import models
from django.utils import timezone
from core.base import BaseModel
from core.utility.uuidgen import generate_custom_id


# -----------------------------
# Admin Region
# -----------------------------
class AdminRegion(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="REG", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -----------------------------
# City
# -----------------------------
class City(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=100)
    admin_region = models.ForeignKey(AdminRegion, on_delete=models.PROTECT, related_name="cities")
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="CTY", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.admin_region.name})"


# -----------------------------
# Company
# -----------------------------
class Company(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, related_name="comapaney"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    logo_url = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="CMP", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} | {self.name}"


# -----------------------------
# Factory home
# -----------------------------
class Factory(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.CharField(
        primary_key=True,
        max_length=16,
        editable=False,
        unique=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="factories"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, related_name="factories"
    )
    capacity = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Maximum production capacity (e.g., units per day)."
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='active'
    )

    class Meta:
        verbose_name = "Factory"
        verbose_name_plural = "Factories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="FCT", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.city.name})"
