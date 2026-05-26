from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "price": str(self.price),
            "created_at": self.created_at.isoformat(),
        }

    def __str__(self):
        return self.name
