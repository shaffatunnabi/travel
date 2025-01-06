# Generated by Django 5.1.2 on 2025-01-06 17:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travel', '0002_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Travel.person'),
        ),
        migrations.AlterField(
            model_name='book',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='book',
            name='numpeople',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='book',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
