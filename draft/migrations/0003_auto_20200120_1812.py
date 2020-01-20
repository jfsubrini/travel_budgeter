# Generated by Django 2.2.5 on 2020-01-20 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draft', '0002_auto_20200120_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='activities',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Activités'),
        ),
        migrations.AlterField(
            model_name='category',
            name='fooding',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Nourriture'),
        ),
        migrations.AlterField(
            model_name='category',
            name='international_transport',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Transports internationaux'),
        ),
        migrations.AlterField(
            model_name='category',
            name='local_transport',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Transports nationaux'),
        ),
        migrations.AlterField(
            model_name='category',
            name='lodging',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Hébergements'),
        ),
        migrations.AlterField(
            model_name='category',
            name='pre_departure',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Dépenses avant le départ'),
        ),
        migrations.AlterField(
            model_name='category',
            name='souvenirs',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Souvenirs'),
        ),
        migrations.AlterField(
            model_name='category',
            name='various',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Divers'),
        ),
        migrations.AlterField(
            model_name='category',
            name='visiting',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Visites'),
        ),
    ]