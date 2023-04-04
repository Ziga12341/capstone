# Generated by Django 4.1 on 2023-04-04 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votingapp', '0002_categorised_list_category_suggestions_group_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='votingapp.category'),
        ),
    ]