# Generated by Django 2.1 on 2018-08-19 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                ('ipv4', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')),
                ('ipv6', models.GenericIPAddressField(blank=True, null=True, protocol='IPv6')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['zone__domain', 'relative_domain'],
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
                ('keys', models.ManyToManyField(to='whizzdiva.DnsKey')),
            ],
            options={
                'ordering': ['domain'],
            },
        ),
        migrations.AddField(
            model_name='dynamicdomain',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='whizzdiva.Zone'),
        ),
        migrations.AlterUniqueTogether(
            name='dynamicdomain',
            unique_together={('zone', 'relative_domain')},
        ),
    ]
