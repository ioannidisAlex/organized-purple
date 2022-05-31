# Generated by Django 3.1.5 on 2022-05-31 16:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('digio', '0002_manager_program_projectngrant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('equity_capital', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('abbreviation', models.CharField(max_length=10)),
                ('phones', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=7)),
                ('city', models.CharField(max_length=20)),
                ('self_street', models.CharField(max_length=30)),
                ('org_type', models.IntegerField(choices=[(1, 'Company'), (2, 'University'), (3, 'ResearchCenter')])),
            ],
        ),
        migrations.CreateModel(
            name='ResearchCenter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('budget_from_the_ministry_of_education', models.FloatField()),
                ('budget_from_private_actions', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('surname', models.CharField(max_length=40)),
                ('birthdate', models.DateField()),
                ('gender', models.IntegerField(choices=[(1, 'male'), (2, 'female'), (3, 'prefer not to say')])),
                ('age', models.IntegerField(default=550)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('budget_from_the_ministry_of_education', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='program',
            name='manager',
        ),
        migrations.AddField(
            model_name='program',
            name='address',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projectngrant',
            name='duration',
            field=models.IntegerField(default=555),
        ),
        migrations.AddField(
            model_name='projectngrant',
            name='summary',
            field=models.CharField(default='al', max_length=3000),
        ),
        migrations.CreateModel(
            name='WorksAt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='digio.researcher')),
            ],
        ),
        migrations.AddField(
            model_name='researcher',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='digio.projectngrant'),
        ),
    ]
