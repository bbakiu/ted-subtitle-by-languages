# Generated by Django 3.1.2 on 2021-01-21 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subtitles', '0003_auto_20210121_1149'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subtitle',
            constraint=models.UniqueConstraint(fields=('video_id', 'language'), name='store_unique_video_lang_combination'),
        ),
    ]
