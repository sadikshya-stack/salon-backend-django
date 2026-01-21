from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import FileExtensionValidator

# ---------- User ----------
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name or self.last_name else self.email




class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(
        upload_to='services/',
        validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])],
        blank=True,
        null=True,
        help_text="Upload service image (jpg, png, webp)"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.name





class ServiceType(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='types'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'service_types'

    def __str__(self):
        return f"{self.service.name} - {self.name}"




# ---------- Staff ----------
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    specialization = models.CharField(max_length=200, blank=True, null=True)
    experience_years = models.IntegerField(default=0)

    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    working_hours_start = models.TimeField(default='09:00')
    working_hours_end = models.TimeField(default='18:00')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class PaymentMethod(models.Model):

    class Meta:
        db_table = 'payment_methods'

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(
        max_length=30,
        unique=True,
        help_text="e.g. cash, esewa, khalti, stripe"
    )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    service_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text="Extra charge for this payment method"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Appointment(models.Model):

    class Meta:
        db_table = 'appointments'

    # ---------------------------
    # SERVICES (IMPORTANT)
    # ---------------------------
    services = models.ManyToManyField(
        ServiceType,
        related_name='appointments',
        help_text="Selected services for this appointment"
    )

    # ---------------------------
    # STAFF ASSIGNMENT
    # ---------------------------
    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        help_text="Staff assigned to this appointment"
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        related_name='appointments'
    )


    # ---------------------------
    # APPOINTMENT STATUS
    # ---------------------------
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # ---------------------------
    # CUSTOMER DETAILS
    # ---------------------------
    name = models.CharField(max_length=100, default="Unknown Customer")
    email = models.EmailField(default="example@example.com")
    phone = models.CharField(max_length=10, default="0000000000")


    # ---------------------------
    # APPOINTMENT SCHEDULE
    # ---------------------------
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    # ---------------------------
    # PAYMENT
    # ---------------------------
    payment_status = models.BooleanField(default=False)  # Paid or Not

    # ---------------------------
    # APPOINTMENT STATUS
    # ---------------------------
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # ---------------------------
    # EXTRA INFO
    # ---------------------------
    notes = models.TextField(blank=True, default="")

    cancelled_reason = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    # ---------------------------
    # TIMESTAMPS
    # ---------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ---------------------------
    # STRING REPRESENTATION
    # ---------------------------
    def __str__(self):
        return f"{self.name} | {self.appointment_date} | {self.status}"


# ---------- AvailableSlot ----------
class AvailableSlot(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='available_slots', null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'available_slots'
        unique_together = ['staff', 'date', 'start_time']
    
    def __str__(self):
        staff_name = f"{self.staff.user.first_name} {self.staff.user.last_name}" if self.staff and self.staff.user else "No Staff"
        return f"{staff_name} - {self.date} {self.start_time}"





class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=350)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"





class InventoryCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Inventory Category"
        verbose_name_plural = "Inventory Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)






class InventoryItem(models.Model):

    class StockStatus(models.TextChoices):
        IN_STOCK = "in_stock", "In Stock"
        LOW_STOCK = "low_stock", "Low Stock"
        OUT_OF_STOCK = "out_of_stock", "Out of Stock"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        InventoryCategory,
        on_delete=models.PROTECT,
        related_name="items"
    )
    brand = models.CharField(max_length=100, blank=True)

    quantity = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=5)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=StockStatus.choices,
        editable=False
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def update_stock_status(self):
        if self.quantity <= 0:
            self.status = self.StockStatus.OUT_OF_STOCK
        elif self.quantity <= self.min_stock:
            self.status = self.StockStatus.LOW_STOCK
        else:
            self.status = self.StockStatus.IN_STOCK

    def save(self, *args, **kwargs):
        self.update_stock_status()
        super().save(*args, **kwargs)
