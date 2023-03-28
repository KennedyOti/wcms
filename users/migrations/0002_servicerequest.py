# Generated by Django 4.1.7 on 2023-03-03 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('location', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
