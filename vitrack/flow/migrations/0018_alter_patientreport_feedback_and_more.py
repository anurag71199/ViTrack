# Generated by Django 4.0.2 on 2022-03-25 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0017_remove_patientreport_id_patientreport_report_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientreport',
            name='feedback',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='patientreport',
            name='refby',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='patientreport',
            name='summary',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='patientreport',
            name='testname',
            field=models.CharField(max_length=500),
        ),
    ]
