# Generated by Django 5.2 on 2025-04-15 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_category_options_remove_category_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20),
        ),
        migrations.AddField(
            model_name='course',
            name='requirements',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=20),
        ),
        migrations.AddField(
            model_name='course',
            name='what_you_will_learn',
            field=models.TextField(blank=True),
        ),
    ]
