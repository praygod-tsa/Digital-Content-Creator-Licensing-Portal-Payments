from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licence_category', models.CharField(choices=[('HABARI', 'Habari na Mambo ya Sasa'), ('BURUDANI', 'Burudani'), ('ELIMU', 'Elimu na Dini'), ('SIMULCASTING', 'Simulcasting')], max_length=30)),
                ('is_amateur', models.BooleanField(default=False)),
                ('channel_links', models.TextField(blank=True)),
                ('status', models.CharField(default='DRAFT', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='applicants.applicant')),
            ],
        ),
    ]
