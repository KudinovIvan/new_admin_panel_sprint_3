# Generated by Django 4.0.2 on 2022-08-21 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_personfilmwork_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='creation_date',
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name='creation_date'
            ),
        ),
    ]
