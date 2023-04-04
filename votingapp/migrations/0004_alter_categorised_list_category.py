# Generated by Django 4.1 on 2023-04-04 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votingapp', '0003_alter_group_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorised_list',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lists', to='votingapp.category'),
        ),
    ]
