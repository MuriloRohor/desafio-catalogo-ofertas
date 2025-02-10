from django.db import models

class Product(models.Model):
    """Produto extraido do ML"""
    cod_ml = models.TextField()
    name = models.TextField()
    price = models.FloatField()
    image_url = models.TextField()
    url = models.TextField()
    installment_options = models.JSONField()
    price_with_discount = models.FloatField(null=True)
    percentual_discount = models.IntegerField(null=True)
    freight_free = models.BooleanField()
    freight_full = models.BooleanField()

    def __str__(self):
        """"""
        return self.name
