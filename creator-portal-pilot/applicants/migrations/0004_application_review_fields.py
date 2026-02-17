from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0003_application_invoice_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='review_comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='application',
            name='review_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20),
        ),
        migrations.AddField(
            model_name='application',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
