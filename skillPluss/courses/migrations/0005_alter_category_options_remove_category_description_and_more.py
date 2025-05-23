# Generated by Django 5.2 on 2025-04-14 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_instructor_lessonresource'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.AddField(
            model_name='rating',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
