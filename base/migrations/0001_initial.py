# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-31 15:09
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stripe_cater', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('tax', models.DecimalField(decimal_places=3, default=0, max_digits=5)),
                ('accout_creation_token', models.CharField(max_length=50, null=True)),
                ('logo', models.FileField(null=True, upload_to='profile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('stripe_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stripe_cater.StripeAccount')),
                ('stripecustomer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stripe_cater.StripeCustomer')),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmEmailOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('checked', models.BooleanField(default=False)),
                ('pending', models.BooleanField(default=True)),
                ('expire_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(blank=True, choices=[('Sir', 'Sir'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Mss', 'Mss'), ('Ms', 'Ms')], max_length=5, null=True)),
                ('suffix', models.CharField(blank=True, choices=[('Jr', 'Jr')], max_length=5, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('comments', models.TextField(null=True)),
                ('activo', models.BooleanField(default=True)),
                ('birthday', models.DateField(null=True)),
                ('cellphone', models.CharField(max_length=25, null=True)),
                ('phone_home', models.CharField(max_length=25, null=True)),
                ('token_removed', models.IntegerField(default=0)),
                ('address', models.TextField(default='', null=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('event_date', models.DateTimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default='0', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('send_token', models.CharField(default='0', max_length=50)),
                ('deleted', models.BooleanField(default=False)),
                ('due_date', models.DateField(default=datetime.datetime(2016, 12, 31, 10, 9, 39, 82385))),
                ('payment_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stripe_cater.PaymentOrder')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=9)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=4)),
                ('description', models.TextField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='N_Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='N_Invoice_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='N_NotificationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('title_format', models.CharField(max_length=50)),
                ('body_format', models.TextField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='N_Prefix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='N_Proposal_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='N_Suffix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField(max_length=150)),
                ('read', models.BooleanField(default=False)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.N_NotificationType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('price', models.DecimalField(decimal_places=3, default=0, max_digits=9)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas', to='base.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_message', models.TextField(default='', max_length=150, null=True)),
                ('number', models.CharField(default='0', max_length=50)),
                ('send_token', models.CharField(default='0', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Event')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.N_Proposal_Status')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Event')),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Oferta')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='oferta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Oferta'),
        ),
        migrations.AddField(
            model_name='item',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Proposal'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Proposal'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.N_Invoice_Status'),
        ),
        migrations.AddField(
            model_name='customer',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.N_Company'),
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together=set([('email', 'activo', 'token_removed', 'business')]),
        ),
    ]
