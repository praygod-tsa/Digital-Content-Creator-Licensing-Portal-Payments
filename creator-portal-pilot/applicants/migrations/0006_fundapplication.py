from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0005_applicant_nin_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund_program', models.CharField(choices=[('GENERAL', 'General Creative Support'), ('TOURISM', 'Tourism Content'), ('SPORTS', 'Sports Content'), ('MUSIC', 'Music'), ('FILM', 'Film'), ('NEWS', 'News / Current Affairs'), ('ARTS', 'Arts & Culture')], max_length=30)),
                ('requested_amount_tzs', models.PositiveIntegerField()),
                ('summary_of_idea', models.TextField()),
                ('status', models.CharField(default='DRAFT', max_length=20)),
                ('review_status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20)),
                ('review_comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fund_applications', to='applicants.applicant')),
            ],
        ),
    ]
