# Generated by Django 2.2.2 on 2019-12-17 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20191216_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xftool',
            name='department',
            field=models.CharField(choices=[('Agilent Learning', 'Agilent Learning'), ('Instrument QC', 'Instrument QC'), ('Cartridge QC', 'Cartridge QC'), ('Spotting', 'Spotting'), ('Metrology', 'Metrology')], default='Agilent Learning', max_length=50),
        ),
    ]
