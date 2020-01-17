# Generated by Django 2.2.5 on 2020-01-17 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='money_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Carte bancaire Visa (compte rattaché)'), (2, 'Carte bancaire MasterCard (compte rattaché)'), (3, 'Porte-monnaie'), (4, 'Chèque de voyage'), (5, 'Compte Paypal, ApplePay, etc.')], verbose_name='Type de portefeuille'),
        ),
    ]
