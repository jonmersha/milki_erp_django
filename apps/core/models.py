from django.db import models
from django.utils import timezone
from apps.core.base import BaseModel
from apps.core.utility.uuidgen import generate_custom_id
import os
import uuid

# -----------------------------
# Admin Region
# -----------------------------
class AdminRegion(BaseModel):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="REG", length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -----------------------------
# City
# -----------------------------
class City(BaseModel):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    admin_region = models.ForeignKey(AdminRegion, on_delete=models.PROTECT, related_name="cities")
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="CTY", length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.admin_region.name})"



def company_media_path(instance, filename):
    """
    Renames the file to a unique string and organizes it by company tracker.
    Example: companies/CMP20260101ABCD/logo_a1b2c3d4.png
    """
    ext = filename.split('.')[-1]
    # Generate a unique filename using UUID
    unique_filename = f"{uuid.uuid4().hex[:12]}.{ext}"
    # Group by the company tracker to keep the storage organized
    return os.path.join('companies', instance.tracker, unique_filename)
# -----------------------------
# Company
# -----------------------------
class Company(BaseModel):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True, db_index=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="companies")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # Real ImageFields with unique renaming logic
    logo = models.ImageField(
        upload_to=company_media_path, 
        blank=True, 
        null=True,
        help_text="Company profile logo"
    )
    banner = models.ImageField(
        upload_to=company_media_path, 
        blank=True, 
        null=True,
        help_text="Company wide banner for the app header"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="CMP", length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.tracker})"

# -----------------------------
# Factory
# -----------------------------
class Factory(BaseModel):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="factories")
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="factories")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(
        blank=True, null=True, 
        help_text="Units per day."
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = "Factory"
        verbose_name_plural = "Factories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="FCT", length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} | {self.company.name}"