# Generated by Django 4.0.4 on 2022-08-03 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_subject_alter_book_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.CharField(default='para alterar', max_length=64),
            preserve_default=False,
        ),
    ]
