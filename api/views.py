from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PerformanceMetric

from .serializers import PerformanceMetricSerializer, UserSerializer

def login_view(request):
    return render(request, 'api/login.html')

#-----------------------------------------------------------------------------
# VIEW PARA O 'ESQUELETO' HTML (Front-end)
#-----------------------------------------------------------------------------
def relatorio_view(request):
    """
    Esta view serve apenas para o 'esqueleto' da pagina html
    """
    return render(request, 'api/relatorio.html')


#-----------------------------------------------------------------------------
# VIEW PARA A API DE DADOS (Back-ende)
#-----------------------------------------------------------------------------
class PerformanceMetricAPIView(generics.ListAPIView):
    """
    Essa view contruida com o Django Rest Framework é responsavel por:
    - Listar as metricas de perfomance.
    _ Suportar filtragem por intervalo de datas.
    _ Suportar filtragem por qualquer campo.
    - Paginar os resultados automaticamente.
    """

    # Consulta base que busca todos os registros
    queryset = PerformanceMetric.objects.all()

    # Usa o Serializer para converter os dados para JSON.
    serializer_class = PerformanceMetricSerializer

    # Se o usuário não enviar um token JWT válido, receberá um erro 401.
    permission_classes = [IsAuthenticated]

    # Ativa os filtros e ordenação do DEF.
    filter_backends = [ DjangoFilterBackend, filters.OrderingFilter]

    # Configura os campos de filtragem
    # Isso permite que façamos pedidos como: /api/metrics-data/?date__gte=2024-01-01
    filterset_fields = {
        'date': ['gte', 'lte'], # Permite date__gte (maior ou igua a) e date__lte ( menor ou igual a)
    }

    #Configura os campos pelo qual os ultilizadores podem ordernar os dados.
    # Isso permite ordernar por clicks (decresente) ou (cresente)
    ordering_fields = [
        'date',
        'campaign_id',
        'clicks',
        'conversions',
        'impressions',
        'cost_micros',
    ]

    # Define uma ordenaçao padrão caso nenhuma for selecionada
    ordering = ['-date']

    def get_serializer_context(self):

        context = super().get_serializer_context()
        context ['request'] = self.request
        return context

# -----------------------------------------------------------------------------
# VIEW PARA OBTER DADOS DO USUÁRIO ATUAL
# -----------------------------------------------------------------------------

class CurrentUserAPIView(APIView):
    """
    Esta view retorna os dados do usuário atualmente autenticado.
    O front usará isto para saber qual é o papel ('role') do usuário.
    """
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)