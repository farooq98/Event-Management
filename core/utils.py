from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_contact_number(value):
    if not value.isdigit() or len(value) < 11:
        raise ValidationError(
            _('%(value)s is not a valid contact number'),
            params={'value': value},
        )