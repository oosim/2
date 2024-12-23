from django import forms
from .models import Farm

class UserTypeForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('farmer', '농가 회원'),
        ('general', '일반 회원'),
    ]
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        label="회원 유형",
        widget=forms.RadioSelect
    )

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['farm', 'farm_slug', 'farm_owner', 'owner_image', 'location', 'description']