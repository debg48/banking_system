from django.db import models

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=45,null=False,blank=False)
    acc_no = models.IntegerField(null=False,blank=False)
    balance = models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return self.name
    
    def values(self):
        return {
            "name" : self.name,
            "acc_no" : self.acc_no,
            "balance" : self.balance
        }

class Loan(models.Model):
    name = models.CharField(max_length=45,null=False,blank=False)
    acc_no = models.IntegerField(null=False,blank=False)
    balance = models.DecimalField(max_digits=20,decimal_places=2)
    loan = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField(name=False)