# Generated by Django 2.0.1 on 2018-01-29 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='neighborhood',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Colonia'),
        ),
        migrations.AlterField(
            model_name='address',
            name='region',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Estado o Region'),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Calle'),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Número exterior'),
        ),
        migrations.AlterField(
            model_name='address',
            name='town',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Municipio o delegacion'),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Código Postal'),
        ),
    ]
