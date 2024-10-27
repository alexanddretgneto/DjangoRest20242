# Generated by Django 5.1.2 on 2024-10-27 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonDRF', '0002_user_alter_rating_user'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nome',
            field=models.CharField(default='Nome Padrão', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='sobrenome',
            field=models.CharField(default='Sobrenome Padrão', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='Os grupos aos quais este usuário pertence.', related_name='little_lemon_user_set', to='auth.group', verbose_name='grupos'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Permissões específicas para este usuário.', related_name='little_lemon_user_permissions_set', to='auth.permission', verbose_name='permissões de usuário'),
        ),
    ]