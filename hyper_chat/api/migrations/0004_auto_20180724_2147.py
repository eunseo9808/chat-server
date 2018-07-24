# Generated by Django 2.0.7 on 2018-07-24 12:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180724_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatter',
            name='user',
        ),
        migrations.AddField(
            model_name='chatter',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatter',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatter',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='chatter',
            name='password',
            field=models.CharField(default=django.utils.timezone.now, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatter',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chatter',
            name='nickname',
            field=models.CharField(default='', max_length=100),
        ),
    ]
