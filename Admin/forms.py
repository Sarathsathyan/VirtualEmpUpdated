
from django.forms import ModelForm
from .models import UserDetails

class AddUserForm(ModelForm):
    class Meta:
        model = UserDetails
        fields=['user_phone']