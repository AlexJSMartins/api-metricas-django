from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modelo de usuário customizado que estende o padrão do Django
    para incluir o campo 'role'.

    """

    ROLE_CHOICES = (
        ("admin","Admin" ),
        ("user", "User")
    )

    # O e-mail é o campo de login principal
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='user')

    # Define o e-mail como campo para autenticação.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class PerformanceMetric(models.Model):
    """
    Modelo para armazenar as métricas de performace das campanhas.
    """

    account_id = models.BigIntegerField()
    campaign_id = models.BigIntegerField()

    #Usei o DecimalField para precisão monetaria
    #const_micros é dividido por 1,000,000 para obter o custo real
    cost_micros = models.DecimalField(max_digits=20, decimal_places=2)
    clicks = models.FloatField()
    conversions = models.FloatField()
    impressions = models.IntegerField()
    interactions = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"Métrica de {self.date} para Campanha {self.campaign_id}"

    class Meta:
        #Garante que não tera dados duplicado para a mesma campanha no mesmo dia

        unique_together = ('campaign_id', 'date')
        ordering = ['-date']

