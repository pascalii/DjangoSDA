# Generated by Django 4.0.3 on 2022-04-09 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='average_rating',
            field=models.FloatField(null=True),
        ),
    ]