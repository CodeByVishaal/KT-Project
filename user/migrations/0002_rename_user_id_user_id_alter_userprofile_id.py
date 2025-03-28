# Generated by Django 4.2.17 on 2025-01-11 08:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.UUIDField(default=uuid.UUID('f1f18f8d-5cf8-4328-b781-c1229757eb51'), editable=False, primary_key=True, serialize=False),
        ),
    ]
