from django.contrib import admin
from .models import Lottery, Participant


class LotteryAdmin(admin.ModelAdmin):
    list_display = ('product', 'aprobated', 'active','finished')
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'lottery', 'winner')

admin.site.register(Lottery, LotteryAdmin)
admin.site.register(Participant, ParticipantAdmin)

# Register your models here.
