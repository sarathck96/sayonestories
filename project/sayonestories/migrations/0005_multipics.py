# Generated by Django 2.0.2 on 2020-01-16 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sayonestories', '0004_auto_20200114_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='multipics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pics', models.ImageField(upload_to='images')),
                ('text', models.CharField(max_length=30)),
            ],
        ),
    ]