# Generated by Django 2.0.7 on 2018-07-24 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180724_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatter',
            name='nickname',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
