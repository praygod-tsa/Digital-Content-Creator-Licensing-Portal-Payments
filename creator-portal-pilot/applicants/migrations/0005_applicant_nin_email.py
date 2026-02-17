from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0004_application_review_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='applicant',
            name='national_id_number',
            field=models.CharField(default='NIN-PENDING', max_length=30),
            preserve_default=False,
        ),
    ]
