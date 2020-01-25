# Generated by Django 2.2.5 on 2020-01-24 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_expense_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='expenses/{self.draft}/%d/%m/%Y', verbose_name='Photo de la facture'),
        ),
    ]