from django.contrib import admin
from .models import Lottery, Participant

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'lottery', 'winner')
admin.site.register(Lottery)
admin.site.register(Participant, ParticipantAdmin)

# Register your models here.
