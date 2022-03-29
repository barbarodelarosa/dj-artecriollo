from django import forms
from .models import AffiliateApplication, Profile


class AffiliateApplicationForm(forms.ModelForm):

    profile = forms.ModelChoiceField(queryset = Profile.objects.none(),label="Perfil", required=False)
    # aprovated = forms.BooleanField(initial=False)

    class Meta:
        model = AffiliateApplication
        fields = []
