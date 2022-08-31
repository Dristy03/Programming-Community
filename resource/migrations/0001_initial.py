# Generated by Django 3.2.9 on 2021-12-27 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import resource.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=30, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to=resource.models.user_directory_path)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]