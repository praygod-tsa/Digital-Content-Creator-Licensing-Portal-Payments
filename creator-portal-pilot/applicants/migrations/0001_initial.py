from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('full_name', models.CharField(max_length=150)),
                ('region', models.CharField(max_length=100)),
                ('main_content_category', models.CharField(max_length=100)),
                ('creator_type', models.CharField(choices=[('AMATEUR', 'Amateur'), ('PROFESSIONAL', 'Professional'), ('AGGREGATOR', 'Aggregator')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
