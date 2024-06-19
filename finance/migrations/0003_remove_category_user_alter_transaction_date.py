# Generated by Django 5.0.6 on 2024-06-18 23:33

import django.template.defaulttags
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_remove_transaction_user_alter_transaction_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=django.template.defaulttags.now),
        ),
    ]