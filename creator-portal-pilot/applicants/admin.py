from django.contrib import admin
from .models import Applicant, Application, FeeSchedule, FundApplication, Licence


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('national_id_number', 'phone', 'email', 'full_name', 'date_of_birth', 'region', 'creator_type', 'created_at')
    search_fields = ('national_id_number', 'phone', 'email', 'full_name', 'region', 'main_content_category')
    list_filter = ('creator_type', 'region')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'applicant',
        'licence_category',
        'is_amateur',
        'status',
        'payment_status',
        'review_status',
        'invoice_number',
        'amount_tzs',
        'created_at',
    )
    search_fields = ('applicant__full_name', 'applicant__phone', 'applicant__national_id_number', 'status', 'invoice_number')
    list_filter = ('licence_category', 'is_amateur', 'status', 'payment_status', 'review_status')


@admin.register(FundApplication)
class FundApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'fund_program', 'requested_amount_tzs', 'status', 'review_status', 'is_youth_at_application', 'created_at')
    search_fields = ('applicant__full_name', 'applicant__phone', 'applicant__national_id_number', 'fund_program')
    list_filter = ('fund_program', 'status', 'review_status', 'is_youth_at_application')


@admin.register(FeeSchedule)
class FeeScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'licence_category',
        'creator_type',
        'is_amateur',
        'fee_type',
        'amount_tzs',
        'effective_from',
        'effective_to',
        'is_active',
    )
    list_filter = ('licence_category', 'creator_type', 'is_amateur', 'fee_type', 'is_active')
    search_fields = ('licence_category', 'creator_type')


@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ('licence_number', 'application', 'status', 'valid_from', 'valid_to', 'created_at')
    list_filter = ('status', 'valid_from', 'valid_to')
    search_fields = ('licence_number', 'application__applicant__full_name', 'application__applicant__national_id_number')
