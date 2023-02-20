from django.db import models

class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    catname=models.CharField(max_length=50)
    subcatname=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    price=models.CharField(max_length=10)
    piconname=models.CharField(max_length=100)
    info=models.CharField(max_length=50)

class Funds(models.Model):
    txnid=models.AutoField(primary_key=True)
    uid=models.CharField(max_length=50)
    amt=models.IntegerField()
    info=models.CharField(max_length=50)    