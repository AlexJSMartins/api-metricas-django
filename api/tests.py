# api/views.py

from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
# NOVAS IMPORTAÇÕES
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PerformanceMetric
# IMPORTAÇÃO DO NOVO SERIALIZER
from .serializers import PerformanceMetricSerializer, UserSerializer


# ... (view relatorio_view continua a mesma) ...
def relatorio_view(request):
    return render(request, 'api/relatorio.html')


# -----------------------------------------------------------------------------
# VIEW PARA A API DE DADOS (AGORA PROTEGIDA)
# -----------------------------------------------------------------------------
class PerformanceMetricAPIView(generics.ListAPIView):
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer

    # ADICIONADO: Define que esta view requer autenticação.
    # Se o utilizador não enviar um token JWT válido, receberá um erro 401.
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {'date': ['gte', 'lte'], }
    ordering_fields = ['date', 'campaign_id', 'clicks', 'impressions', 'conversions', 'cost_micros']
    ordering = ['-date']


# -----------------------------------------------------------------------------
# NOVA VIEW PARA OBTER DADOS DO UTILIZADOR ATUAL
# -----------------------------------------------------------------------------
class CurrentUserAPIView(APIView):
    """
    Esta view retorna os dados do utilizador atualmente autenticado.
    O frontend usará isto para saber qual é o papel ('role') do utilizador.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

