# Generated by Django 3.1.7 on 2021-03-26 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorei', '0007_auto_20210326_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationery',
            name='stationery_id',
            field=models.IntegerField(db_column='stationery_id', primary_key=True, serialize=False),
        ),
    ]