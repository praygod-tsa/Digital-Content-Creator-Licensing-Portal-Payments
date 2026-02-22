from django.db import models
from django.db.models import Q
from django.utils import timezone


class Applicant(models.Model):
    class CreatorType(models.TextChoices):
        AMATEUR = 'AMATEUR', 'Amateur'
        PROFESSIONAL = 'PROFESSIONAL', 'Professional'
        AGGREGATOR = 'AGGREGATOR', 'Aggregator'

    # NOTE: Youth threshold is currently fixed at 35 for pilot purposes.
    # In production this should be policy-configurable.
    YOUTH_AGE_THRESHOLD = 35

    national_id_number = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=150)
    region = models.CharField(max_length=100)
    main_content_category = models.CharField(max_length=100)
    creator_type = models.CharField(max_length=20, choices=CreatorType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} ({self.phone})'

    def age_in_years(self):
        if not self.date_of_birth:
            return None

        today = timezone.localdate()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return years

    def is_youth(self):
        age = self.age_in_years()
        if age is None:
            return False
        return age <= self.YOUTH_AGE_THRESHOLD


class Application(models.Model):
    class LicenceCategory(models.TextChoices):
        HABARI = 'HABARI', 'Habari na Mambo ya Sasa'
        BURUDANI = 'BURUDANI', 'Burudani'
        ELIMU = 'ELIMU', 'Elimu na Dini'
        SIMULCASTING = 'SIMULCASTING', 'Simulcasting'

    class ReviewStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applications')
    licence_category = models.CharField(max_length=30, choices=LicenceCategory.choices)
    is_amateur = models.BooleanField(default=False)
    channel_links = models.TextField(blank=True)
    status = models.CharField(max_length=30, default='DRAFT')

    invoice_number = models.CharField(max_length=40, blank=True)
    amount_tzs = models.PositiveIntegerField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, default='UNPAID')
    paid_at = models.DateTimeField(null=True, blank=True)

    review_status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.PENDING)
    review_comment = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.applicant.full_name} - {self.licence_category} ({self.status})'


class FundApplication(models.Model):
    class FundProgram(models.TextChoices):
        GENERAL = 'GENERAL', 'General Creative Support'
        TOURISM = 'TOURISM', 'Tourism Content'
        SPORTS = 'SPORTS', 'Sports Content'
        MUSIC = 'MUSIC', 'Music'
        FILM = 'FILM', 'Film'
        NEWS = 'NEWS', 'News / Current Affairs'
        ARTS = 'ARTS', 'Arts & Culture'

    class ReviewStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='fund_applications')
    fund_program = models.CharField(max_length=30, choices=FundProgram.choices)
    requested_amount_tzs = models.PositiveIntegerField()
    summary_of_idea = models.TextField()
    status = models.CharField(max_length=20, default='DRAFT')
    is_youth_at_application = models.BooleanField(default=False)

    review_status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.PENDING)
    review_comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.applicant.full_name} - {self.fund_program} ({self.status})'


class FeeSchedule(models.Model):
    class FeeType(models.TextChoices):
        APPLICATION = 'APPLICATION', 'Application'
        LICENCE = 'LICENCE', 'Licence'

    licence_category = models.CharField(max_length=30, choices=Application.LicenceCategory.choices)
    creator_type = models.CharField(max_length=20, choices=Applicant.CreatorType.choices)
    is_amateur = models.BooleanField(default=False)
    fee_type = models.CharField(max_length=20, choices=FeeType.choices, default=FeeType.APPLICATION)
    amount_tzs = models.PositiveIntegerField()
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-effective_from', '-id']

    def __str__(self):
        return (
            f'{self.licence_category} | {self.creator_type} | '
            f'amateur={self.is_amateur} | {self.fee_type} = {self.amount_tzs} TZS'
        )


class Licence(models.Model):
    class LicenceStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        SUSPENDED = 'SUSPENDED', 'Suspended'
        REVOKED = 'REVOKED', 'Revoked'

    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='licence')
    licence_number = models.CharField(max_length=50, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    status = models.CharField(max_length=20, choices=LicenceStatus.choices, default=LicenceStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.licence_number} - {self.application.applicant.full_name}'


def calculate_application_fee(application, fee_type=FeeSchedule.FeeType.APPLICATION):
    today = timezone.localdate()

    fee = (
        FeeSchedule.objects.filter(
            licence_category=application.licence_category,
            creator_type=application.applicant.creator_type,
            is_amateur=application.is_amateur,
            fee_type=fee_type,
            is_active=True,
            effective_from__lte=today,
        )
        .filter(Q(effective_to__isnull=True) | Q(effective_to__gte=today))
        .order_by('-effective_from', '-id')
        .first()
    )

    if fee:
        return fee.amount_tzs

    # Graceful fallback for pilot in case schedule is missing
    if application.is_amateur:
        return 10_000
    if application.applicant.creator_type == Applicant.CreatorType.AGGREGATOR:
        return 100_000
    return 50_000
