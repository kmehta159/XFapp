# Generated by Django 2.2.2 on 2019-12-17 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20191217_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xftool',
            name='department',
            field=models.CharField(choices=[('Agilent Learning', 'Agilent Learning'), ('Instrument QC', 'Instrument QC'), ('Cartridge QC', 'Cartridge QC'), ('Spotting', 'Spotting'), ('Metrology', 'Metrology')], default='Learning', max_length=50),
        ),
    ]
