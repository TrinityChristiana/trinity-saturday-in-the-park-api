# Generated by Django 3.0.6 on 2020-05-19 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'attraction',
                'verbose_name_plural': 'attractions',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_members', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
            },
        ),
        migrations.CreateModel(
            name='ParkArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('theme', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'parkarea',
                'verbose_name_plural': 'parkareas',
            },
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saturdayintheparkapi.Attraction')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saturdayintheparkapi.Customer')),
            ],
            options={
                'verbose_name': 'itinerary',
                'verbose_name_plural': 'itineraries',
            },
        ),
        migrations.AddField(
            model_name='attraction',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saturdayintheparkapi.ParkArea'),
        ),
    ]
