# Generated by Django 5.1.2 on 2024-10-22 11:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='caste',
            field=models.CharField(choices=[('general', 'General'), ('obc', 'Other Backward Class'), ('sc', 'Scheduled Caste'), ('st', 'Scheduled Tribe'), ('ews', 'Economically Weaker Section')], max_length=10),
        ),
        migrations.AlterField(
            model_name='application',
            name='cet_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='application',
            name='roll_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='submitted', max_length=20),
        ),
        migrations.CreateModel(
            name='Rector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='application',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hostel.student'),
        ),
    ]
