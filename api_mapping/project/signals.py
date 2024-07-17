# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Project
import os

@receiver(post_save, sender=Project)
def generate_project_html(sender, instance, created, **kwargs):
    if created:
        # Render HTML content for the project page using a template
        html_content = render_to_string('project_page_template.html', {'project': instance})

        # Generate a filename for the HTML page
        file_name = f"{instance.id}.html"

        # Save the HTML content to a file
        file_path = os.path.join('project_pages', file_name)
        with open(file_path, 'w') as f:
            f.write(html_content)
