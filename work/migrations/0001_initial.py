# Generated by Django 2.2.7 on 2019-12-11 08:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='work.Company')),
            ],
            options={
                'unique_together': {('company', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WorkPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'New'), (1, 'Approved'), (2, 'Cancelled'), (3, 'Finished')], default=0)),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workplaces', to='work.Work')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workplaces', to='work.Worker')),
            ],
            options={
                'unique_together': {('work', 'worker')},
            },
        ),
        migrations.CreateModel(
            name='WorkTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'New'), (1, 'Approved'), (2, 'Cancelled')], default=0)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.Worker')),
                ('workplace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worktimes', to='work.WorkPlace')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managers', to='work.Company')),
            ],
        ),
    ]
