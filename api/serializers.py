from rest_framework import serializers
from .models import User, PerformanceMetric


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para expor os dados do utilizador, principalmente seu 'role'
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

# Serializer de Métricas preparado para lidar com permissões
class PerformanceMetricSerializer(serializers.ModelSerializer):
    """
    Este serializer converte o modelo PerformanceMetric para o formato JSON
    e esconde o campo cost_micros se o utilizador não for um administrador
    """
    class Meta:
        model = PerformanceMetric
        # Campos que devem ser incluidos na resposta
        fields = [
            'date',
            'campaign_id',
            'clicks',
            'conversions',
            'impressions',
            'cost_micros',
        ]

    def to_representation(self, instance):
        """
        Este metodo é chamado pelo DRF antes de serializar os dados.
        Ele permite modificar a forma como os dados sãp apresentados.
        """
        # Pega a representação padrão dos dados.
        representation = super().to_representation(instance)

        # Obtem o objeto 'request' a partir do contexto do serializer
        request = self.context.get('request')

        # Verifica se o usuário existe e se seu papel não é 'admin'.
        if request and getattr(request.user, 'is_authenticated', False):
            if getattr(request.user, 'role', None) != 'admin':
                representation.pop('cost_micros', None)

        return representation