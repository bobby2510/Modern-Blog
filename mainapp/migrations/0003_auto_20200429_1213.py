# Generated by Django 3.0.5 on 2020-04-29 06:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20200428_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 29, 6, 43, 40, 575058, tzinfo=utc)),
        ),
    ]
