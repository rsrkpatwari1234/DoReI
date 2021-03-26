# Generated by Django 3.1.7 on 2021-03-25 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dorei', '0003_auto_20210325_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Money',
            fields=[
                ('money_id', models.IntegerField(db_column='money_id', primary_key=True, serialize=False)),
                ('t_time', models.DateTimeField(db_column='t_time')),
                ('amount', models.IntegerField(db_column='amount')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='dorei.user')),
            ],
        ),
    ]
