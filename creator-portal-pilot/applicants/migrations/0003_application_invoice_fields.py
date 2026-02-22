from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0002_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='amount_tzs',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='application',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='payment_status',
            field=models.CharField(default='UNPAID', max_length=20),
        ),
    ]
