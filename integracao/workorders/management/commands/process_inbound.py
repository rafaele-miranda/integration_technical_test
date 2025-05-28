import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from workorders.models import WorkOrder
from datetime import datetime
from django.utils import timezone
import pytz

class Command(BaseCommand):
    help = 'Process inbound JSON files'

    def handle(self, *args, **options):
        processed = 0
        errors = 0
        
        for filename in os.listdir(settings.DATA_INBOUND_DIR):
            if not filename.endswith('.json'):
                continue
                
            filepath = os.path.join(settings.DATA_INBOUND_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validação básica
                required_fields = ['orderNo', 'summary', 'creationDate', 'lastUpdateDate']
                if not all(field in data for field in required_fields):
                    raise ValueError(f"Campos obrigatórios faltando em {filename}")
                
                # Conversão de datas com tratamento de erro
                try:
                    creation_date = datetime.strptime(
                        data['creationDate'], 
                        '%Y-%m-%dT%H:%M:%SZ'
                    ).replace(tzinfo=pytz.UTC)
                    
                    last_update = datetime.strptime(
                        data['lastUpdateDate'], 
                        '%Y-%m-%dT%H:%M:%SZ'
                    ).replace(tzinfo=pytz.UTC)
                except ValueError as e:
                    raise ValueError(f"Formato de data inválido em {filename}: {str(e)}")

                # Determinação do status
                status = 'pending'
                if data.get('isDone', False):
                    status = 'completed'
                elif data.get('isOnHold', False):
                    status = 'on_hold'
                elif data.get('isCanceled', False):
                    status = 'cancelled'

                # Cria/atualiza o registro
                WorkOrder.objects.update_or_create(
                    number=data['orderNo'],
                    defaults={
                        'status': status,
                        'title': data['summary'][:200],  
                        'description': f"Ordem {data['orderNo']} importada de {filename}",
                        'created_at': creation_date,
                        'updated_at': last_update,
                        'is_synced': False
                    }
                )
                processed += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Processado: {filename}'))

            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f'❌ Erro em {filename}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nProcessamento concluído: {processed} arquivos processados, {errors} erros'))