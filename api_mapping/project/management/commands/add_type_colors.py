# myapp/management/commands/add_type_colors.py

from django.core.management.base import BaseCommand
from django.db import transaction
from project.models import Type_color

class Command(BaseCommand):
    help = 'Adds data to the Type_color table'

    def handle(self, *args, **options):
        self.add_type_colors()

    @staticmethod
    def add_type_colors():
        data = [
            {'type': 'GSLB', 'color': '#FFD700'},    # Gold
            {'type': 'LB', 'color': '#90EE90'},      # Light Green
            {'type': 'DB', 'color': '#87CEFA'},      # Light Sky Blue
            {'type': 'MESSAGE_QUEUE', 'color': '#FFA07A'},  # Light Salmon
            {'type': 'Container', 'color': '#FF69B4'},      # Hot Pink
            {'type': 'API', 'color': '#98FB98'},             # Pale Green
            {'type': 'External_Source', 'color': '#FA8072'},  # Salmon
            {'type': 'Context_Switching', 'color': '#FFB6C1'},# Light Pink
            {'type': 'Middleware', 'color': '#F08080'}        # Light Coral
        ]

        with transaction.atomic():
            for item in data:
                Type_color.objects.create(**item)
