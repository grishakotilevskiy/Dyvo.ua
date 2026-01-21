import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomRequirementsValidator:
    def validate(self, password, user=None):
        # Requirement: Latin letters only and digits. No special symbols.
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            raise ValidationError(
                _("Пароль має містити тільки латинські літери та цифри. Спеціальні символи заборонені."),
                code='invalid_chars',
            )

        # Requirement: Must contain at least one digit
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Пароль має містити цифри."),
                code='password_no_number',
            )

        # Requirement: Must contain at least one letter
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _("Пароль має містити літери."),
                code='password_no_letter',
            )

    def get_help_text(self):
        return _(
            "Ваш пароль має містити тільки латинські літери та цифри (мінімум одну літеру та одну цифру)."
        )

# Validator for names
def validate_latin_only(value):
    if not re.match(r"^[a-zA-Z\s-]+$", value):
        raise ValidationError(_("Ім'я може містити тільки латинські літери та дефіс."))

# Validator for email
def validate_email(value):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
        raise ValidationError("Введіть коректну електронну адресу.")

# Validator for phone length
def validate_phone(value):
    if not (re.match(r"^[0-9]+$", value) and (len(value) == 10)):
        raise ValidationError("Введіть коректний номер.")
