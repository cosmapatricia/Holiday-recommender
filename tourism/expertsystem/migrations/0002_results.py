# Generated by Django 2.1.5 on 2019-03-24 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expertsystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_name', models.CharField(max_length=100)),
                ('result_text', models.CharField(max_length=500)),
            ],
        ),
    ]
