# Generated by Django 3.0.9 on 2020-08-10 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200810_0947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postattachfile',
            old_name='File',
            new_name='upload_file',
        ),
    ]