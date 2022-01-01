from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid
from datetime import timedelta

from django.db.models.fields import AutoField

# Create your models here.

class UserProfile(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    isSeller = models.BooleanField(default=False)



class Deal(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller')
    product = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    isEnd = models.BooleanField(default=False)

    def update(self, data):

        if 'isEnd' in data:
            self.isEnd = data['isEnd']
        if 'price' in data:
            self.price = data['price']

     ###  Increase end time by number of hours #######
        if 'end_time' in data:
            end_time_hour = int(data['end_time'])
            end_time = self.end_time
            end_time = end_time + timedelta(hours=end_time_hour)
            self.end_time = end_time
        
        if 'claim_deal' in data:
            claim_deal = data['claim_deal']
            if claim_deal:
                quantity = self.quantity
                self.quantity = quantity-1

        res = self.save()
        return res



class ClaimDeal(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)

