from django.contrib.auth.models import AbstractUser
from django.db import models


# Usuários (ONGs e Protetores)
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_ong = models.BooleanField(default=False)  # Identifica se é uma ONG
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_user_set", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions_set", blank=True
    )

    def __str__(self):
        return self.username


# Animais para adoção
class Animal(models.Model):
    SPECIES_CHOICES = [
        ("dog", "Cachorro"),
        ("cat", "Gato"),
    ]

    SIZE_CHOICES = [
        ("small", "Pequeno"),
        ("medium", "Médio"),
        ("large", "Grande"),
    ]

    STATUS_CHOICES = [
        ("available", "Disponível"),
        ("adopted", "Adotado"),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField()
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    description = models.TextField()
    photo = models.ImageField(upload_to="animal_photos/", blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # ONG ou Protetor

    def __str__(self):
        return self.name


# Pedidos de Adoção (Contato)
class ContactRequest(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interesse em {self.animal.name} por {self.name}"
