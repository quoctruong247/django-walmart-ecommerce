# Generated by Django 3.2.1 on 2021-05-30 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20210529_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('True', 'On'), ('False', 'Off')], default='New', max_length=10),
        ),
    ]