# Generated by Django 3.0.2 on 2020-01-14 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sayonestories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sayoneuser',
            name='profile_pic',
            field=models.ImageField(blank=True, default='static/images/default_pic.jpg', null=True, upload_to='images'),
        ),
    ]
