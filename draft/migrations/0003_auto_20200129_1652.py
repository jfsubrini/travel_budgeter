# Generated by Django 2.2.5 on 2020-01-29 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draft', '0002_auto_20200129_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draft',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]