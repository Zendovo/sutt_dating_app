# Generated by Django 4.1.3 on 2022-11-25 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_blocklist_userprofile_blocklist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(default='Hi', max_length=300)),
                ('req_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_from', to='user.userprofile')),
                ('req_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to', to='user.userprofile')),
            ],
            options={
                'unique_together': {('req_from', 'req_to')},
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='chat_requests',
            field=models.ManyToManyField(related_name='requests_received', through='user.ChatRequest', to='user.userprofile'),
        ),
    ]
