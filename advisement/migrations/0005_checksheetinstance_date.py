# Generated by Django 3.1.5 on 2021-01-22 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisement', '0004_remove_checksheetinstance_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='checksheetinstance',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
