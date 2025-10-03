import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import User,PerformanceMetric
import os

# Definindo a classe que vai herdar o BaseCommand
class Command(BaseCommand):
    # Texto de ajuda que será exibido apos rodar o comando python manage.py load_initial_data
    help = 'Carregar os dados iniciais dos aquivos users.csv e metrics.csv para o banco de dados'

    #Metodo handle
    def handle(self, *args, **kwargs):
        #Caminho para os arquivos CSV
        users_csv_path = os.path.join(settings.BASE_DIR, 'users.csv')
        metrics_csv_path = os.path.join(settings.BASE_DIR, 'metrics.csv')

        # Mensagem indicando o inicio da carga do usuário
        self.stdout.write(self.style.SUCCESS('Iniciando a Carga de Usuários no Banco de Dados'))

        # Bloco 'try ... except' para capturar erros durante a execução
        try:
            # Usa o pandas para ler e carregar o arquivo
            users_df = pd.read_csv(users_csv_path)
            for _, row in users_df.iterrows():
                user_email = row['username']

                # Verififica se ja existe usuário com esse e-mail cadastrado
                if not User.objects.filter(email=user_email).exists():
                    # Se o usuário não existir cria um
                    """
                    Usei o metodo .create para criar um novo usuário ele é um metodo direto para criar
                    e salvar um objeto
                    """
                    user = User.objects.create(
                        username=user_email,# Preenche a coluna 'username' com o email para garantir a unicidade
                        email=user_email,
                        role=row['role'],
                        is_active=True,
                    )
                    # A senha precisa ser "hasheada" antes de ser salva
                    # O set_password() faz isso de forma segura
                    user.set_password(row['password'])
                    # Salva os dados do usuário
                    user.save()

                    self.stdout.write(f"Usuário {user.email} criado com sucesso")
                else:
                    self.stdout.write(self.style.WARNING(f"Usuário {user_email} já existe. Pulando."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Arquivo users.csv não encontrado em '{users_csv_path}'."))
            return

        # --- Iniciando a Carga de dados das Metricas de performance ---
        self.stdout.write(self.style.SUCCESS('\nIniciando a Carga de Métricas de Performance...'))
        try:
            # Caminho do arquivo
            metrics_df = pd.read_csv(metrics_csv_path)
            #Converte a coluna data para o formato correto
            metrics_df['date'] = pd.to_datetime(metrics_df['date'])

            """
            Para evitar duplicidade toda vez que rodar o comando, todos os dados serão deletados cada vez que 
            rodar o comando, garantindo uma carga de dados limpa toda vez que que o comando for executado
             """
            PerformanceMetric.objects.all().delete()

            """
            Prepara uma lista vazia para receber as metricas, isso possibilta usar 
            o 'bulk_create' que é mais rápido do que criar um objeto de cada vez  
             """
            metrics_to_create = []
            for _, row in metrics_df.iterrows():
                # O valor de cost_micros é dividido por 1,000,000
                cost = row['cost_micros'] / 1000000.0
                # Cria um objeto PerformanceMetric na memória
                metrics_to_create.append(
                    PerformanceMetric(
                        account_id=row['account_id'],
                        campaign_id=row['campaign_id'],
                        cost_micros=cost,
                        clicks=row['clicks'],
                        conversions=row['conversions'],
                        impressions=row['impressions'],
                        interactions=row['interactions'],
                        date=row['date'].date() # O .date() pega somente a data sem as horas
                    )
                )
            # O 'bulk_create' pega os objetos e insere ele em uma única e eficiente operação no banco de dados
            PerformanceMetric.objects.bulk_create(metrics_to_create)
            self.stdout.write(self.style.SUCCESS(f'{len(metrics_to_create)} Registros de métricas criado com sucesso.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Arquivo de metricas não encontrado em '{metrics_csv_path}'."))
            return
        # Conclusão do Processo
        self.stdout.write(self.style.SUCCESS(f'\nCarga de Dados Iniciais Concluída com Sucesso...'))
    


