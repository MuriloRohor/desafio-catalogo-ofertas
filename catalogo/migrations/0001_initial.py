# Generated by Django 5.1.6 on 2025-02-09 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_ml', models.TextField()),
                ('name', models.TextField()),
                ('price', models.FloatField()),
                ('image_url', models.TextField()),
                ('url', models.TextField()),
                ('installment_options', models.JSONField()),
                ('price_with_discount', models.FloatField(null=True)),
                ('percentual_discount', models.IntegerField(null=True)),
                ('freight_free', models.BooleanField()),
                ('freight_full', models.BooleanField()),
            ],
        ),
    ]
