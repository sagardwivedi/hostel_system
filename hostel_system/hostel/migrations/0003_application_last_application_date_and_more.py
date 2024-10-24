# Generated by Django 5.1.2 on 2024-10-24 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0002_alter_application_caste_alter_application_cet_marks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='last_application_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='application',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='caste',
            field=models.CharField(choices=[('general', 'General'), ('obc', 'Other Backward Class'), ('sc', 'Scheduled Caste'), ('st', 'Scheduled Tribe'), ('other', 'Others')], max_length=10),
        ),
        migrations.AlterField(
            model_name='application',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.student'),
        ),
    ]
