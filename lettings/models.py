"""Models de l'app lettings (Adress & Letting)."""

from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator

class Address(models.Model):
    """Adresse postale normalisée.

    Champs:
        number: Numéro de rue.
        street: Nom de la rue.
        city: Ville.
        state: État (2 lettres).
        zip_code: Code postal.
        country_iso_code: Code pays ISO-3166 alpha-3.
    """
    
    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])
    
    class Meta: 
        verbose_name_plural = "Adresses"

    def __str__(self):
        return f"{self.number} {self.street}"


class Letting(models.Model):
    """Location référencée sur le site.

    Champs:
        title: Titre de l'annonce.
        address: Adresse associée (OneToOne).
    """
    
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    
    class Meta: 
        verbose_name_plural = "Lettings"

    def __str__(self):
        return self.title
