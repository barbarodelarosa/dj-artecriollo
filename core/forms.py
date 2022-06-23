from core.models import Contact
from django import forms



from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV3
from captcha.widgets import ReCaptchaV2Checkbox

class AllAuthSignupForm(forms.Form):

    # captcha = ReCaptchaField(
    #     widget=ReCaptcha(
    #     attrs={
    #         'required_score':0.90,
    #     }
    # )
    # )

    captcha = ReCaptchaField(
    public_key='6LdkqmogAAAAACD3SkRCdKIVBsT7bwkefz-XWv8b',
    private_key='6LdkqmogAAAAAONNCcBDzyEftTPe5z4LFtg5xKDI',
    widget=ReCaptchaV2Checkbox(
        attrs={
            # 'data-theme': 'dark',
            # 'data-size': 'compact',
        }
    )
)
    field_order = ['email', 'password1', 'password2', 'captcha']
    # def save(self, request, user):
    # def save(self, request, user):
    #     user = super(AllAuthSignupForm, self).save(request)
    #     return user
    def signup(self, request, user):
        user.save()

# from allauth.account.forms import LoginForm
# class MyCustomLoginForm(LoginForm):
#     captcha = ReCaptchaField(
#         widget=ReCaptchaV3(
#         attrs={
#             'required_score':0.90,
#         }

#     )
#     )


    # def login(self, *args, **kwargs):

    #     Add your own processing here.

    #     You must return the original result.
    #     return super(MyCustomLoginForm, self).login(*args, **kwargs)

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
class AuthAdminForm(AuthenticationForm):

    # if not settings.DEBUG:
    #     captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
    #         attrs={
    #             'data-theme': 'light',
    #             'data-size': 'normal',
    #             # 'style': ('transform:scale(1.057);-webkit-transform:scale(1.057);'
    #             #           'transform-origin:0 0;-webkit-transform-origin:0 0;')
    #         }
    #     ))
    captcha = ReCaptchaField(
    public_key='6LdkqmogAAAAACD3SkRCdKIVBsT7bwkefz-XWv8b',
    private_key='6LdkqmogAAAAAONNCcBDzyEftTPe5z4LFtg5xKDI',
    widget=ReCaptchaV2Checkbox(
        attrs={
            # 'data-theme': 'dark',
            # 'data-size': 'compact',
        }
    )
    )
class ContactForm(forms.Form):
    
    name = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(attrs={
        'placeholder': "Tu Nombre",
    }))
    email = forms.EmailField(label='Correo', widget=forms.TextInput(attrs={
        'placeholder': "Tu Correo Electronico"
    }))
    message = forms.CharField(max_length=100, label='Mensaje', widget=forms.TextInput(attrs={
        'placeholder': "Tu Mensaje"
    }))
