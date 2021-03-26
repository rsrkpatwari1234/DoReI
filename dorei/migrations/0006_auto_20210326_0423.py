# Generated by Django 3.1.7 on 2021-03-26 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dorei', '0005_auto_20210325_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.IntegerField(db_column='location_id', primary_key=True, serialize=False)),
                ('floor', models.IntegerField(db_column='floor', default=1)),
                ('room', models.CharField(db_column='room', default=1, max_length=5)),
                ('shelf', models.IntegerField(db_column='shelf', default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(db_column='author', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='edition',
            field=models.IntegerField(blank=True, db_column='edition', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='grade',
            field=models.IntegerField(blank=True, db_column='grade', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(db_column='isbn', default=1, max_length=13, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='subject',
            field=models.CharField(blank=True, db_column='subject', max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(db_column='title', max_length=256),
        ),
        migrations.AddField(
            model_name='book',
            name='location_id',
            field=models.ForeignKey(blank=True, db_column='location_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dorei.location'),
        ),
        migrations.CreateModel(
            name='BookDonate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_time', models.DateTimeField(db_column='t_time')),
                ('is_collected', models.BooleanField(db_column='collected', default=False)),
                ('isbn', models.ForeignKey(db_column='isbn', on_delete=django.db.models.deletion.CASCADE, to='dorei.book')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='dorei.user')),
            ],
            options={
                'unique_together': {('user_id', 'isbn')},
            },
        ),
    ]