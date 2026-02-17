import random
from datetime import timedelta
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    ApplicantForm,
    ApplicationForm,
    ApplicationReviewForm,
    FundApplicationForm,
    FundApplicationReviewForm,
    OTPVerificationForm,
    SignInForm,
)
from .models import Applicant, Application, FundApplication, Licence, calculate_application_fee


ROLE_TCRA_REVIEWER = 'ROLE_TCRA_REVIEWER'
ROLE_MINISTRY_FUND_REVIEWER = 'ROLE_MINISTRY_FUND_REVIEWER'
ROLE_MINISTRY_LEADERSHIP_READONLY = 'ROLE_MINISTRY_LEADERSHIP_READONLY'


def group_required(*group_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            if not user.is_authenticated:
                return redirect('staff_login')
            if user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden('Huna ruhusa ya kufungua ukurasa huu.')

        return _wrapped

    return decorator


def issue_licence_if_eligible(application):
    if application.payment_status != 'PAID' or application.review_status != Application.ReviewStatus.APPROVED:
        return None

    if hasattr(application, 'licence'):
        return application.licence

    today = timezone.localdate()
    valid_to = today + timedelta(days=365)

    licence = Licence.objects.create(
        application=application,
        licence_number=f'LIC-{today.year}-{application.id:06d}',
        valid_from=today,
        valid_to=valid_to,
        status=Licence.LicenceStatus.ACTIVE,
    )
    return licence


def home(request):
    return render(request, 'applicants/home.html')


def staff_login(request):
    if request.user.is_authenticated:
        return redirect('staff_dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('staff_dashboard')

    return render(request, 'applicants/staff_login.html', {'form': form})


@login_required(login_url='staff_login')
def staff_dashboard(request):
    return render(request, 'applicants/staff_dashboard.html')


def start_signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            nin = form.cleaned_data['national_id_number']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            otp_code = f"{random.randint(0, 999999):06d}"

            request.session['otp_nin'] = nin
            request.session['otp_phone'] = phone
            request.session['otp_email'] = email
            request.session['otp_channel'] = 'PHONE'
            request.session['otp_code'] = otp_code
            request.session['otp_verified'] = False

            return redirect('verify_otp')
    else:
        form = SignInForm()

    return render(request, 'applicants/signin.html', {'form': form})


def verify_otp(request):
    otp_phone = request.session.get('otp_phone')
    otp_code = request.session.get('otp_code')

    if not otp_phone or not otp_code:
        return redirect('start_signin')

    error_message = None

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if entered_otp == otp_code:
                request.session['otp_verified'] = True
                return redirect('dashboard')
            error_message = 'OTP si sahihi. Tafadhali jaribu tena.'
    else:
        form = OTPVerificationForm()

    return render(
        request,
        'applicants/verify_otp.html',
        {
            'form': form,
            'otp_for_testing': otp_code,
            'otp_phone': otp_phone,
            'otp_channel': request.session.get('otp_channel', 'PHONE'),
            'error_message': error_message,
        },
    )


def _get_session_applicant(request):
    otp_phone = request.session.get('otp_phone')
    otp_nin = request.session.get('otp_nin')

    if not otp_phone or not otp_nin:
        return None

    return (
        Applicant.objects.filter(phone=otp_phone, national_id_number=otp_nin)
        .order_by('-created_at')
        .first()
    )


def dashboard(request):
    otp_verified = request.session.get('otp_verified', False)
    otp_phone = request.session.get('otp_phone')
    otp_nin = request.session.get('otp_nin')

    if not otp_verified or not otp_phone or not otp_nin:
        return redirect('start_signin')

    applicant = _get_session_applicant(request)

    my_licence_applications = []
    my_fund_applications = []
    if applicant:
        my_licence_applications = list(
            Application.objects.filter(applicant=applicant)
            .select_related('licence')
            .order_by('-created_at')[:5]
        )
        my_fund_applications = list(
            FundApplication.objects.filter(applicant=applicant).order_by('-created_at')[:5]
        )

    return render(
        request,
        'applicants/dashboard.html',
        {
            'applicant': applicant,
            'my_licence_applications': my_licence_applications,
            'my_fund_applications': my_fund_applications,
        },
    )


def register_applicant(request):
    otp_verified = request.session.get('otp_verified', False)
    otp_phone = request.session.get('otp_phone')
    otp_nin = request.session.get('otp_nin')

    if not otp_verified or not otp_phone or not otp_nin:
        return redirect('start_signin')

    locked_identity = {
        'phone': otp_phone,
        'national_id_number': otp_nin,
        'email': request.session.get('otp_email', ''),
    }

    if request.method == 'POST':
        form = ApplicantForm(request.POST, locked_identity=locked_identity)
        if form.is_valid():
            applicant = form.save()
            request.session['current_applicant_id'] = applicant.id
            return redirect('applicant_success')
    else:
        form = ApplicantForm(initial=locked_identity, locked_identity=locked_identity)

    return render(request, 'applicants/applicant_form.html', {'form': form})


def applicant_success(request):
    return render(request, 'applicants/applicant_success.html')


def apply_licence(request):
    applicant = _get_session_applicant(request)

    if not applicant:
        return redirect('register_applicant')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = applicant
            application.status = 'SUBMITTED'
            application.payment_status = 'UNPAID'
            application.save()
            return redirect('application_success', application_id=application.id)
    else:
        form = ApplicationForm()

    return render(
        request,
        'applicants/application_form.html',
        {'form': form, 'applicant': applicant},
    )


def application_success(request, application_id):
    application = get_object_or_404(Application.objects.select_related('applicant', 'licence'), id=application_id)
    return render(
        request,
        'applicants/application_success.html',
        {'application': application, 'licence': getattr(application, 'licence', None)},
    )


def application_invoice(request, application_id):
    application = get_object_or_404(Application.objects.select_related('applicant'), id=application_id)

    if not application.invoice_number:
        today = timezone.localdate().strftime('%Y%m%d')
        suffix = f'{random.randint(0, 9999):04d}'
        application.invoice_number = f'INV-{today}-{suffix}'
        application.amount_tzs = calculate_application_fee(application)
        if not application.payment_status:
            application.payment_status = 'UNPAID'
        application.save(update_fields=['invoice_number', 'amount_tzs', 'payment_status', 'updated_at'])

    return render(request, 'applicants/application_invoice.html', {'application': application})


def mark_application_paid(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == 'POST':
        application.payment_status = 'PAID'
        application.paid_at = timezone.now()
        application.save(update_fields=['payment_status', 'paid_at', 'updated_at'])
        issue_licence_if_eligible(application)

    return redirect('application_invoice', application_id=application.id)


@login_required(login_url='staff_login')
@group_required(ROLE_TCRA_REVIEWER)
def application_review(request, application_id):
    application = get_object_or_404(Application.objects.select_related('applicant'), id=application_id)

    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            reviewed_application = form.save(commit=False)
            reviewed_application.reviewed_at = timezone.now()
            reviewed_application.save(update_fields=['review_status', 'review_comment', 'reviewed_at', 'updated_at'])
            issue_licence_if_eligible(reviewed_application)
            return redirect('application_list')
    else:
        form = ApplicationReviewForm(instance=application)

    return render(
        request,
        'applicants/application_review.html',
        {
            'application': application,
            'form': form,
        },
    )


def fund_apply(request):
    applicant = _get_session_applicant(request)

    if not applicant:
        return redirect('register_applicant')

    if request.method == 'POST':
        form = FundApplicationForm(request.POST)
        if form.is_valid():
            fund_application = form.save(commit=False)
            fund_application.applicant = applicant
            fund_application.status = 'SUBMITTED'
            fund_application.review_status = FundApplication.ReviewStatus.PENDING
            fund_application.is_youth_at_application = applicant.is_youth()
            fund_application.save()
            return redirect('fund_success', fund_application_id=fund_application.id)
    else:
        form = FundApplicationForm()

    return render(
        request,
        'applicants/fund_apply.html',
        {
            'form': form,
            'applicant': applicant,
        },
    )


def fund_success(request, fund_application_id):
    fund_application = get_object_or_404(FundApplication.objects.select_related('applicant'), id=fund_application_id)
    return render(request, 'applicants/fund_success.html', {'fund_application': fund_application})


@login_required(login_url='staff_login')
@group_required(ROLE_MINISTRY_FUND_REVIEWER, ROLE_MINISTRY_LEADERSHIP_READONLY)
def fund_application_list(request):
    fund_applications = FundApplication.objects.select_related('applicant').order_by('-created_at')
    return render(
        request,
        'applicants/fund_application_list.html',
        {'fund_applications': fund_applications},
    )


@login_required(login_url='staff_login')
@group_required(ROLE_MINISTRY_FUND_REVIEWER)
def fund_application_review(request, fund_application_id):
    fund_application = get_object_or_404(FundApplication.objects.select_related('applicant'), id=fund_application_id)

    if request.method == 'POST':
        form = FundApplicationReviewForm(request.POST, instance=fund_application)
        if form.is_valid():
            reviewed_fund_application = form.save(commit=False)
            reviewed_fund_application.save(update_fields=['review_status', 'review_comment', 'updated_at'])
            return redirect('fund_application_list')
    else:
        form = FundApplicationReviewForm(instance=fund_application)

    return render(
        request,
        'applicants/fund_application_review.html',
        {
            'fund_application': fund_application,
            'form': form,
            'applicant_age': fund_application.applicant.age_in_years(),
            'is_youth_now': fund_application.applicant.is_youth(),
        },
    )


@login_required(login_url='staff_login')
@group_required(ROLE_TCRA_REVIEWER, ROLE_MINISTRY_FUND_REVIEWER, ROLE_MINISTRY_LEADERSHIP_READONLY)
def youth_report(request):
    applicants_with_dob_qs = Applicant.objects.exclude(date_of_birth__isnull=True)
    applicants_with_dob = applicants_with_dob_qs.count()

    youth_applicants = sum(1 for applicant in applicants_with_dob_qs if applicant.is_youth())
    youth_percentage = 0
    if applicants_with_dob > 0:
        youth_percentage = round((youth_applicants / applicants_with_dob) * 100, 1)

    youth_fund_count = FundApplication.objects.filter(is_youth_at_application=True).count()
    non_youth_fund_count = FundApplication.objects.filter(is_youth_at_application=False).count()

    youth_program_breakdown = (
        FundApplication.objects
        .filter(is_youth_at_application=True)
        .values('fund_program')
        .annotate(total=Count('id'))
        .order_by('-total', 'fund_program')
    )

    return render(
        request,
        'applicants/youth_report.html',
        {
            'applicants_with_dob': applicants_with_dob,
            'youth_applicants': youth_applicants,
            'youth_percentage': youth_percentage,
            'youth_fund_count': youth_fund_count,
            'non_youth_fund_count': non_youth_fund_count,
            'youth_program_breakdown': youth_program_breakdown,
            'program_labels': dict(FundApplication.FundProgram.choices),
        },
    )


@login_required(login_url='staff_login')
@group_required(ROLE_TCRA_REVIEWER, ROLE_MINISTRY_LEADERSHIP_READONLY)
def applicant_list(request):
    applicants = Applicant.objects.order_by('-created_at')
    return render(request, 'applicants/applicant_list.html', {'applicants': applicants})


@login_required(login_url='staff_login')
@group_required(ROLE_TCRA_REVIEWER, ROLE_MINISTRY_LEADERSHIP_READONLY)
def application_list(request):
    applications = Application.objects.select_related('applicant', 'licence').order_by('-created_at')
    return render(request, 'applicants/application_list.html', {'applications': applications})


@login_required(login_url='staff_login')
@group_required(ROLE_TCRA_REVIEWER, ROLE_MINISTRY_LEADERSHIP_READONLY)
def licence_certificate(request, licence_id):
    licence = get_object_or_404(Licence.objects.select_related('application__applicant'), id=licence_id)
    return render(request, 'applicants/licence_certificate.html', {'licence': licence})


def fund_stub(request):
    return redirect('fund_apply')


def mentorship_stub(request):
    return render(request, 'applicants/mentorship_stub.html')
