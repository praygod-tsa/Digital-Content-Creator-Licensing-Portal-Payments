import re
from django import forms
from .models import Applicant, Application, FundApplication


class SignInForm(forms.Form):
    national_id_number = forms.CharField(label='Namba ya Taifa (NIN)', max_length=30)
    phone = forms.CharField(label='Namba ya Simu', max_length=20)
    email = forms.EmailField(label='Barua Pepe (Email)', required=False)

    def clean_national_id_number(self):
        nin = self.cleaned_data['national_id_number'].strip()
        normalized = re.sub(r'\s+', '', nin)
        if len(normalized) < 8:
            raise forms.ValidationError('NIN lazima iwe na angalau herufi/tarakimu 8.')
        return normalized

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) < 9:
            raise forms.ValidationError('Namba ya simu lazima iwe na angalau tarakimu 9.')
        return phone


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='Weka OTP', max_length=6)

    def clean_otp(self):
        otp = self.cleaned_data['otp'].strip()
        if not otp.isdigit() or len(otp) not in [4, 6]:
            raise forms.ValidationError('OTP lazima iwe namba ya tarakimu 4 au 6.')
        return otp


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'national_id_number',
            'phone',
            'email',
            'date_of_birth',
            'full_name',
            'region',
            'main_content_category',
            'creator_type',
        ]
        labels = {
            'national_id_number': 'Namba ya Taifa (NIN)',
            'phone': 'Namba ya Simu',
            'email': 'Barua Pepe (Email)',
            'date_of_birth': 'Tarehe ya Kuzaliwa',
            'full_name': 'Jina Kamili',
            'region': 'Mkoa',
            'main_content_category': 'Aina Kuu ya Maudhui',
            'creator_type': 'Aina ya Muundaji',
        }
        help_texts = {
            'phone': 'Namba hii imethibitishwa kwa OTP (kwa sasa fake OTP ya majaribio).',
            'national_id_number': 'NIN hii itatumika baadaye kwa uhakiki na vigezo vya mfuko.',
            'date_of_birth': 'Kwa sasa ni taarifa ya kujaza mwenyewe (self-reported) hadi NIDA integration baadaye.',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, locked_identity=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.locked_identity = locked_identity or {}

        if self.locked_identity.get('phone'):
            self.fields['phone'].initial = self.locked_identity['phone']
            self.fields['phone'].widget.attrs['readonly'] = True

        if self.locked_identity.get('national_id_number'):
            self.fields['national_id_number'].initial = self.locked_identity['national_id_number']
            self.fields['national_id_number'].widget.attrs['readonly'] = True

        if self.locked_identity.get('email'):
            self.fields['email'].initial = self.locked_identity['email']

    def clean_national_id_number(self):
        nin = self.cleaned_data['national_id_number'].strip()
        normalized = re.sub(r'\s+', '', nin)
        if len(normalized) < 8:
            raise forms.ValidationError('NIN lazima iwe na angalau herufi/tarakimu 8.')

        locked_nin = self.locked_identity.get('national_id_number')
        if locked_nin and normalized != locked_nin:
            raise forms.ValidationError('NIN haiwezi kubadilishwa baada ya OTP.')

        return normalized

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        digits_only = re.sub(r'\D', '', phone)

        if len(digits_only) < 9:
            raise forms.ValidationError('Namba ya simu lazima iwe na angalau tarakimu 9.')

        locked_phone = self.locked_identity.get('phone')
        if locked_phone and phone != locked_phone:
            raise forms.ValidationError('Namba ya simu haiwezi kubadilishwa baada ya OTP.')

        return phone


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['licence_category', 'is_amateur', 'channel_links']
        labels = {
            'licence_category': 'Kategoria ya Leseni',
            'is_amateur': 'Ninaomba kupitia Amateur category',
            'channel_links': 'Viungo/handles vya channel (weka kila link mstari mpya)',
        }
        widgets = {
            'channel_links': forms.Textarea(attrs={'rows': 6, 'placeholder': 'https://youtube.com/@mfano\nhttps://tiktok.com/@mfano'}),
        }


class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['review_status', 'review_comment']
        labels = {
            'review_status': 'Uamuzi wa Mapitio',
            'review_comment': 'Maoni ya Mkaguzi',
        }
        widgets = {
            'review_status': forms.Select(choices=[
                (Application.ReviewStatus.APPROVED, 'Approved'),
                (Application.ReviewStatus.REJECTED, 'Rejected'),
            ]),
            'review_comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Andika maoni mafupi ya uamuzi...'}),
        }


class FundApplicationForm(forms.ModelForm):
    class Meta:
        model = FundApplication
        fields = ['fund_program', 'requested_amount_tzs', 'summary_of_idea']
        labels = {
            'fund_program': 'Program ya Mfuko',
            'requested_amount_tzs': 'Kiasi kinachoombwa (TZS)',
            'summary_of_idea': 'Muhtasari wa wazo/biashara',
        }
        widgets = {
            'summary_of_idea': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Eleza kwa kifupi wazo lako na jinsi litakavyokua...'}),
        }


class FundApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = FundApplication
        fields = ['review_status', 'review_comment']
        labels = {
            'review_status': 'Uamuzi wa Maombi ya Mfuko',
            'review_comment': 'Maoni ya Mkaguzi wa Mfuko',
        }
        widgets = {
            'review_status': forms.Select(choices=[
                (FundApplication.ReviewStatus.APPROVED, 'Approved'),
                (FundApplication.ReviewStatus.REJECTED, 'Rejected'),
            ]),
            'review_comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Andika maoni ya idhini au kukataa...'}),
        }
