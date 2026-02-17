from django.urls import path
from .views import (
    applicant_list,
    applicant_success,
    application_invoice,
    application_list,
    application_review,
    application_success,
    apply_licence,
    dashboard,
    fund_application_list,
    fund_application_review,
    fund_apply,
    fund_stub,
    fund_success,
    home,
    licence_certificate,
    mark_application_paid,
    mentorship_stub,
    register_applicant,
    staff_dashboard,
    staff_login,
    start_signin,
    verify_otp,
    youth_report,
)

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home_alias'),
    path('signin/', start_signin, name='start_signin'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register_applicant, name='register_applicant'),
    path('success/', applicant_success, name='applicant_success'),

    path('staff-login/', staff_login, name='staff_login'),
    path('staff-dashboard/', staff_dashboard, name='staff_dashboard'),

    path('apply/', apply_licence, name='apply_licence'),
    path('applications/<int:application_id>/success/', application_success, name='application_success'),
    path('applications/<int:application_id>/invoice/', application_invoice, name='application_invoice'),
    path('applications/<int:application_id>/mark-paid/', mark_application_paid, name='mark_application_paid'),
    path('applications/<int:application_id>/review/', application_review, name='application_review'),

    path('fund/', fund_stub, name='fund_stub'),
    path('fund/apply/', fund_apply, name='fund_apply'),
    path('fund/success/<int:fund_application_id>/', fund_success, name='fund_success'),
    path('fund/applications/', fund_application_list, name='fund_application_list'),
    path('fund/applications/<int:fund_application_id>/review/', fund_application_review, name='fund_application_review'),

    path('reports/youth/', youth_report, name='youth_report'),

    path('mentorship/', mentorship_stub, name='mentorship_stub'),

    path('applicants/', applicant_list, name='applicant_list'),
    path('applications/', application_list, name='application_list'),

    path('licences/<int:licence_id>/certificate/', licence_certificate, name='licence_certificate'),
]
