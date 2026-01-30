from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.gis.db import models as gis_models  # Import GeoDjango models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = gis_models.EmailField(_('email address'), unique=True)
    first_name = gis_models.CharField(_('first name'), max_length=150)

    # srid=4326 is the standard for GPS coordinates (WGS 84)
    location = gis_models.PointField(srid=4326, blank=True, null=True)

    # host specific fields
    is_host = gis_models.BooleanField(default=False, verbose_name="is host account")
    phone_number = gis_models.CharField(_("phone number"), max_length=20, blank=True, null=True)

    avatar = gis_models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="avatar")

    # Socials
    contacts = gis_models.TextField(_("contacts"), blank=True, null=True)
    instagram = gis_models.CharField(max_length=50, blank=True, null=True)
    facebook = gis_models.CharField(max_length=50, blank=True, null=True)

    # Bio
    about = gis_models.TextField(_("about"), blank=True, null=True)

    # Required for Admin/Auth
    is_staff = gis_models.BooleanField(default=False)
    is_active = gis_models.BooleanField(default=True)
    date_joined = gis_models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email


class Event(gis_models.Model):
    CATEGORY_CHOICES = [
        ("activity", "Активні вихідні"),
        ("handmade", "Своїми руками"),
        ("culture", "Екскурсії та відпочинок"),
        ("food", "Їжа та дегустації"),
        ("other", "Різне"),
    ]

    # Owner
    owner = gis_models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name="Хост"
    )

    # Fields
    title = gis_models.CharField(max_length=200, verbose_name="Назва *")
    description = gis_models.TextField(verbose_name="Опис *")

    category = gis_models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Категорія *"
    )

    address = gis_models.CharField(
        max_length=255,
        verbose_name="Адреса *",
        help_text="Наприклад: м. Київ, вул. Хрещатик, 1"
    )

    max_guests = gis_models.PositiveIntegerField(verbose_name="Максимальна кількість гостей *")

    # Photo
    photo = gis_models.ImageField(upload_to="event_photos/", verbose_name="Фото *")

    # Additional fields
    ticket_price = gis_models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Ціна за особу"
    )

    duration = gis_models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Приблизна тривалість"
    )

    date = gis_models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата"
    )

    social1 = gis_models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Посилання на ваші соціальні мережі"
    )

    social2 = gis_models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Додаткові посилання"
    )

    guests = gis_models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="attended_events",
        blank=True,
        verbose_name="Гості"
    )

    created_at = gis_models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Враження"
        verbose_name_plural = "Враження"
        indexes = [
            gis_models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title
