from django.db import models
from django.urls import reverse
from shop.models import Product
from django.db.models.signals import pre_save
from django.utils.text import slugify

from django.contrib.auth import get_user_model

User = get_user_model()


class Lottery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_finish = models.DateTimeField()
    price_lottery = models.IntegerField(verbose_name="Monto de inscripción", default=0) #Establece el valor que hay que pagar para inscribirse
    value_product_lottery = models.FloatField(verbose_name="Valor del producto en el mercado(info)", default=0.00) #Establece el del produto en el mercado(esto es solo informacion)
    related_lottery = models.ManyToManyField('self', blank=True)
    note = models.TextField(blank=True, null=True)
    aprobated = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    total_winners = models.IntegerField(default=1)
    winners = models.ManyToManyField(User, blank=True, related_name="winners")
    

    

    def __str__(self):
        return self.product.title

    def get_absolute_url(self):
        return reverse("lottery:lottery-detail", kwargs={'pk':self.pk})

class ParticipantPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0.00)
    purchused=models.BooleanField(default=False)
    transaction_uuid=models.CharField(max_length=32, blank=True, null=True)
    user_uuid=models.CharField(max_length=32, blank=True, null=True)
    
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0.00)
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    payment = models.OneToOneField(ParticipantPayment, on_delete=models.CASCADE)
    winner = models.BooleanField(default=False)
    participant_number = models.IntegerField(blank=True)

    def __str__(self):
        return f'{self.user}'

 


def pre_safe_lottery_receiver(sender, instance, *args, **kwargs):
    product = instance.product.id
    product = Product.objects.get(id = instance.product.id)
    product.for_lottery = True
    product.save()
pre_save.connect(pre_safe_lottery_receiver, sender=Lottery)

def pre_safe_participant_receiver(sender, instance, *args, **kwargs):
    lottery_id = instance.lottery.id
 
    total_participants = instance.lottery.participant_set.count()
    print('total_participants',total_participants)
    if not instance.participant_number:
        instance.participant_number = total_participants + 1
 

pre_save.connect(pre_safe_participant_receiver, sender=Participant)