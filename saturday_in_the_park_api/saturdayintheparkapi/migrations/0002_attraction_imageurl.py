# Generated by Django 3.0.6 on 2020-05-20 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saturdayintheparkapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction',
            name='imageurl',
            field=models.URLField(default='https://semantic-ui.com/images/wireframe/image.png'),
        ),
    ]
