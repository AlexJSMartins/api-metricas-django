from django.urls import path

from . import views
from rest_framework_simplejwt.views import (
TokenObtainPairView,
TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    #Urls da Aplicação
    path('relatorio/', views.relatorio_view, name='relatorio_metricas'),
    path('metrics-data/', views.PerformanceMetricAPIView.as_view(), name='metrics_data_api'),
    path('user/me/', views.CurrentUserAPIView.as_view(), name='current_user_api'),

    # Urls Autenticadas
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),




]