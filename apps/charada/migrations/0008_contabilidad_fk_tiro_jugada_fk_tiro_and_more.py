# Generated by Django 4.1 on 2022-10-22 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('charada', '0007_rename_esvalida_jugada_esganadora_jugada_premio'),
    ]

    operations = [
        migrations.AddField(
            model_name='contabilidad',
            name='fk_tiro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='charada.tiro', verbose_name='Tiro'),
        ),
        migrations.AddField(
            model_name='jugada',
            name='fk_tiro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='charada.tiro', verbose_name='Tiro'),
        ),
        migrations.AlterField(
            model_name='contabilidad',
            name='fecha',
            field=models.DateTimeField(verbose_name='Fecha de entrada de las jugadas'),
        ),
        migrations.AlterField(
            model_name='jugada',
            name='esGanadora',
            field=models.BooleanField(default=False, verbose_name='Jugada valida'),
        ),
        migrations.AlterField(
            model_name='jugada',
            name='fecha',
            field=models.DateTimeField(verbose_name='Fecha de entrada de las jugadas'),
        ),
    ]
