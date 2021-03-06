# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-31 15:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('captured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('captured_at', models.DateTimeField(null=True)),
                ('status', models.CharField(default='PENDING', max_length=10)),
                ('destination', models.CharField(max_length=50)),
                ('stripe_id', models.CharField(max_length=50, null=True)),
                ('source', models.CharField(max_length=50)),
                ('currency', models.CharField(default='usd', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='EventRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripeid', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('due', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='StripeAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_publishable_key', models.CharField(max_length=50)),
                ('access_token', models.CharField(max_length=50)),
                ('stripe_user_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StripeCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=50)),
                ('stripe_exp_month', models.IntegerField(null=True)),
                ('stripe_exp_year', models.IntegerField(null=True)),
                ('stripe_last4', models.CharField(max_length=4, null=True)),
                ('stripe_brand', models.CharField(max_length=25, null=True)),
                ('stripe_address_country', models.CharField(max_length=25, null=True)),
                ('stripe_address_city', models.CharField(max_length=25, null=True)),
                ('stripe_address_state', models.CharField(max_length=25, null=True)),
                ('stripe_address_line', models.CharField(max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StripeCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripeid', models.CharField(max_length=50)),
                ('stripetoken', models.CharField(max_length=50)),
                ('billing_email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StripeInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripeid', models.CharField(max_length=50)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
                ('attempt_count', models.IntegerField(default=0)),
                ('last_attempt', models.DateTimeField(null=True)),
                ('closed', models.BooleanField(default=False)),
                ('receipt_number', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StripeSubscripcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripeid', models.CharField(max_length=50)),
                ('stripestatus', models.CharField(max_length=50)),
                ('current', models.BooleanField(default=True)),
                ('current_period_start', models.DateTimeField()),
                ('current_period_end', models.DateTimeField()),
                ('stripecustomer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='stripe_cater.StripeCustomer')),
            ],
        ),
        migrations.AddField(
            model_name='stripeinvoice',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='stripe_cater.StripeSubscripcion'),
        ),
        migrations.AddField(
            model_name='stripecard',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card', to='stripe_cater.StripeCustomer'),
        ),
        migrations.AddField(
            model_name='charge',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stripe_cater.PaymentOrder'),
        ),
    ]
