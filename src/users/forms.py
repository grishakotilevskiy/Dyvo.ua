from django import forms
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
import re
from .validators import validate_latin_only, validate_email, validate_phone

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    REGION_CHOICES = [
        ('', 'Оберіть область'),
        ('Вінницька область', 'Вінницька область'),
        ('Волинська область', 'Волинська область'),
        ('Дніпропетровська область', 'Дніпропетровська область'),
        ('Донецька область', 'Донецька область'),
        ('Житомирська область', 'Житомирська область'),
        ('Закарпатська область', 'Закарпатська область'),
        ('Запорізька область', 'Запорізька область'),
        ('Івано-Франківська область', 'Івано-Франківська область'),
        ('Київ (місто)', 'Київ (місто)'),
        ('Київська область', 'Київська область'),
        ('Кіровоградська область', 'Кіровоградська область'),
        ('Львівська область', 'Львівська область'),
        ('Миколаївська область', 'Миколаївська область'),
        ('Одеська область', 'Одеська область'),
        ('Полтавська область', 'Полтавська область'),
        ('Рівненська область', 'Рівненська область'),
        ('Сумська область', 'Сумська область'),
        ('Тернопільська область', 'Тернопільська область'),
        ('Харківська область', 'Харківська область'),
        ('Херсонська область', 'Херсонська область'),
        ('Хмельницька область', 'Хмельницька область'),
        ('Черкаська область', 'Черкаська область'),
        ('Чернівецька область', 'Чернівецька область'),
        ('Чернігівська область', 'Чернігівська область'),
    ]

    REGION_COORDINATES = {
        'Вінницька область': (28.4682, 49.2331),
        'Волинська область': (25.3254, 50.7472),
        'Дніпропетровська область': (35.0462, 48.4647),
        'Донецька область': (37.8028, 48.0159),
        'Житомирська область': (28.6687, 50.2547),
        'Закарпатська область': (22.2879, 48.6208),
        'Запорізька область': (35.1396, 47.8388),
        'Івано-Франківська область': (24.7111, 48.9226),
        'Київ (місто)': (30.5234, 50.4501),
        'Київська область': (30.5234, 50.4501),
        'Кіровоградська область': (32.2623, 48.5079),
        'Львівська область': (24.0297, 49.8397),
        'Миколаївська область': (31.9946, 46.9750),
        'Одеська область': (30.7233, 46.4825),
        'Полтавська область': (34.5514, 49.5883),
        'Рівненська область': (26.2516, 50.6199),
        'Сумська область': (34.7981, 50.9077),
        'Тернопільська область': (25.5948, 49.5535),
        'Харківська область': (36.2304, 49.9935),
        'Херсонська область': (32.6169, 46.6354),
        'Хмельницька область': (26.9871, 49.4230),
        'Черкаська область': (32.0637, 49.4444),
        'Чернівецька область': (25.9355, 48.2921),
        'Чернігівська область': (31.2893, 51.4982),
    }

    region = forms.ChoiceField(
        choices=REGION_CHOICES,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Оберіть область",
            "autocomplete": "off",
            "id": "regionInput"
        }),
        label="З якої ви області?"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Придумайте надійний пароль",
            "class": "form-control",
            "id": "id_password"
        }),
        label="Пароль",
        error_messages={"required": "Будь ласка, введіть пароль."}
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Введіть пароль ще раз",
            "class": "form-control",
            "id": "id_confirm_password"
        }),
        label="Підтвердьте пароль",
        error_messages={"required": "Будь ласка, підтвердіть пароль."}
    )
    terms_confirmed = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Згода з правилами",
        error_messages={"required": "Ви повинні погодитися з правилами сайту."}
    )

    class Meta:
        model = User
        fields = ["email", "first_name"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "emailaddress@gmail.com",
                "class": "form-control"
            }),
            "first_name": forms.TextInput(attrs={
                "placeholder": "Введіть ваше ім'я",
                "class": "form-control"
            }),
        }
        labels = {
            "email": "Електронна адреса",
            "first_name": "Введіть ім'я",
        }
        error_messages = {
            "email": {
                "required": "Введіть електронну адресу.",
                "invalid": "Введіть коректну електронну адресу."
            },
            "first_name": {
                "required": "Введіть ваше ім'я."
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ця електронна адреса вже зареєстрована.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        validate_latin_only(first_name)
        return first_name

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Пароль має містити мінімум 8 символів.")
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            raise ValidationError("Пароль не має містити спеціальні символи.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Пароль має містити цифри.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("Пароль має містити літери.")
        return password

    def clean_region(self):
        region = self.cleaned_data.get("region")
        if region:
            valid_regions = [choice[0] for choice in self.REGION_CHOICES]
            if region not in valid_regions:
                pass
        return region

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Паролі не співпадають.")

    def save(self, commit=True):
        user = super().save(commit=False)
        region_name = self.cleaned_data.get("region")

        if region_name and region_name in self.REGION_COORDINATES:
            lng, lat = self.REGION_COORDINATES[region_name]
            user.location = Point(lng, lat)
        else:
            user.location = None

        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class HostRegistrationForm(RegistrationForm):

    # override guest fields with specific labels/placeholders
    email = forms.EmailField(
        label="Електронна адреса",
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            "placeholder": "emailaddress@gmail.com",
            "class": "form-control",
            "id": "id_email"
        })
    )

    first_name = forms.CharField(
        label="Як до Вас звертатися?",
        validators=[validate_latin_only],
        widget=forms.TextInput(attrs={
            "placeholder": "Ваше ім'я та прізвище",
            "class": "form-control",
            "id": "id_first_name"
        })
    )

    region = forms.ChoiceField(
        choices=RegistrationForm.REGION_CHOICES,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Оберіть зі списку",
            "autocomplete": "off",
            "id": "regionInput"
        }),
        label="Ваше місце проживання"
    )

    phone_number = forms.CharField(
        label="Ваш номер телефону",
        required=True,
        validators=[validate_phone],
        widget=forms.TextInput(attrs={
            "placeholder": "+380 _ _  _ _ _  _ _  _ _",
            "class": "form-control"
        })
    )

    avatar = forms.ImageField(
        label="Додайте Ваше найкраще фото",
        required=True,
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    contacts = forms.CharField(
        label="Вкажіть контактну інформацію",
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Вкажіть контактну інформацію",
            "class": "form-control mb-2"
        })
    )

    instagram = forms.CharField(
        label="Ваш Instagram",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Ваш Instagram",
            "class": "form-control"
        })
    )

    facebook = forms.CharField(
        label="Ваш Facebook",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Ваш Facebook",
            "class": "form-control"
        })
    )

    about = forms.CharField(
        label="Розкажіть гостям про себе, щоб підняти довіру до вас",
        required=False,
        widget=forms.Textarea(attrs={
            "placeholder": "Чим Ви займаєтеся? Яким досвідом хочете поділитися з гостями?",
            "class": "form-control",
            "rows": 3
        }),
        help_text="Лише 2-3 речення про Вас. Це може допомогти Вам виділити своє враження серед інших."
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "phone_number", "contacts", "instagram", "facebook", "about"]

    def save(self, commit=True):
        user = super().save(commit=False)

        # set host flag
        user.is_host = True
        user.is_staff = True
        user.is_superuser = False

        # save extra fields specific to host
        user.phone_number = self.cleaned_data.get("phone_number")
        user.avatar = self.cleaned_data.get("avatar")
        user.contacts = self.cleaned_data.get("contacts")
        user.instagram = self.cleaned_data.get("instagram")
        user.facebook = self.cleaned_data.get("facebook")
        user.about = self.cleaned_data.get("about")

        if commit:
            user.save()
            if user.is_host:
                try:
                    host_group = Group.objects.get(name='Hosts')
                    user.groups.add(host_group)
                except Group.DoesNotExist:
                    pass
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Електронна адреса",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "emailaddress@gmail.com",
            "id": "id_email",
            "autofocus": True
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ваш пароль",
            "id": "id_password"
        })
    )
