# Generated by Django 2.2.1 on 2019-05-30 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortnr', '0004_auto_20190529_0521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlink',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='shortlink',
            name='custom',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='shortlink',
            name='short_path',
            field=models.CharField(db_index=True, max_length=25, unique=True),
        ),
    ]