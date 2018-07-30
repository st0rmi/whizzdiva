# Generated by Django 2.0.6 on 2018-06-20 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this site.', verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates whether the user has superuser privileges.', verbose_name='superuser status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.Unselect this instead of deleting accounts.', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DnsKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='date last modified')),
                ('usable', models.BooleanField(default=True)),
                ('algorithm', models.CharField(choices=[('HMAC-MD5', 'HMAC-MD5'), ('HMAC-SHA1', 'HMAC-SHA1'), ('HMAC-SHA224', 'HMAC-SHA224'), ('HMAC-SHA256', 'HMAC-SHA256'), ('HMAC-SHA384', 'HMAC-SHA384'), ('HMAC-SHA512', 'HMAC-SHA512')], max_length=32)),
                ('secret', models.CharField(max_length=1000)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DynamicDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='date last modified')),
                ('relative_domain', models.CharField(max_length=50)),
                ('ttl', models.PositiveIntegerField(null=True)),
                ('ipv4', models.GenericIPAddressField(null=True, protocol='IPv4')),
                ('ipv6', models.GenericIPAddressField(null=True, protocol='IPv6')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['relative_domain'],
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='date last modified')),
                ('domain', models.CharField(max_length=200, unique=True)),
                ('default_ttl', models.PositiveIntegerField(default=60)),
                ('hidden', models.BooleanField(default=False)),
                ('keys', models.ManyToManyField(to='dynamicdns.DnsKey')),
            ],
            options={
                'ordering': ['domain'],
            },
        ),
        migrations.AddField(
            model_name='dynamicdomain',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dynamicdns.Zone'),
        ),
        migrations.AlterUniqueTogether(
            name='dynamicdomain',
            unique_together={('zone', 'relative_domain')},
        ),
    ]
