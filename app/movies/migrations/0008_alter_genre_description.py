# Generated by Django 4.0.2 on 2022-08-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_alter_filmwork_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='description'
            ),
        ),
    ]
