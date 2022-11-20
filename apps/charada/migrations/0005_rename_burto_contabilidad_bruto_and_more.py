# Generated by Django 4.1 on 2022-10-19 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charada', '0004_alter_jugada_parlet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contabilidad',
            old_name='burto',
            new_name='bruto',
        ),
        migrations.RemoveField(
            model_name='contabilidad',
            name='horario',
        ),
        migrations.AlterField(
            model_name='contabilidad',
            name='fecha',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha del tiro'),
        ),
    ]