# Generated by Django 4.0.4 on 2022-07-18 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_book_is_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='subject',
            field=models.CharField(default='not_setted', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='is_page',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
