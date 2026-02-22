from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0006_fundapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fundapplication',
            name='is_youth_at_application',
            field=models.BooleanField(default=False),
        ),
    ]
