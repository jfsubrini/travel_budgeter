# Generated by Django 2.2.5 on 2020-01-29 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]