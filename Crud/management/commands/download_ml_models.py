from django.core.management.base import BaseCommand
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Descarga modelos de Machine Learning (Stanza, NLTK)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--stanza-only',
            action='store_true',
            help='Descargar solo modelos de Stanza',
        )
        parser.add_argument(
            '--nltk-only',
            action='store_true',
            help='Descargar solo modelos de NLTK',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar descarga incluso si ya existen',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Descarga de Modelos ML ===')
        )
        
        try:
            from Crud.services import ml_model_manager
            
            stanza_only = options['stanza_only']
            nltk_only = options['nltk_only']
            force = options['force']
            
            if not stanza_only and not nltk_only:
                # Descargar ambos
                self.stdout.write('Descargando modelos Stanza...')
                stanza_success = ml_model_manager.ensure_stanza_models()
                
                self.stdout.write('Descargando modelos NLTK...')
                nltk_success = ml_model_manager.ensure_nltk_models()
                
                if stanza_success and nltk_success:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Todos los modelos descargados exitosamente')
                    )
                elif stanza_success or nltk_success:
                    self.stdout.write(
                        self.style.WARNING('⚠ Algunos modelos se descargaron, otros fallaron')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('✗ No se pudieron descargar los modelos')
                    )
                    
            elif stanza_only:
                self.stdout.write('Descargando solo modelos Stanza...')
                success = ml_model_manager.ensure_stanza_models()
                if success:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Modelos Stanza descargados')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('✗ Error descargando modelos Stanza')
                    )
                    
            elif nltk_only:
                self.stdout.write('Descargando solo modelos NLTK...')
                success = ml_model_manager.ensure_nltk_models()
                if success:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Modelos NLTK descargados')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('✗ Error descargando modelos NLTK')
                    )
            
            # Mostrar estado final
            status = ml_model_manager.get_models_status()
            self.stdout.write('\nEstado de modelos:')
            self.stdout.write(f"  Stanza: {'✓' if status['stanza'] else '✗'}")
            self.stdout.write(f"  NLTK: {'✓' if status['nltk'] else '✗'}")
            self.stdout.write(f"  YARA: {'✓' if status['yara'] else '✗'}")
            self.stdout.write(f"  Directorio: {status['models_dir']}")
            
        except ImportError as e:
            self.stdout.write(
                self.style.ERROR(f'Error importando módulos: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error inesperado: {str(e)}')
            ) 