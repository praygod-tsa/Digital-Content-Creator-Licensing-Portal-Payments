'use server';

import { redirect } from 'next/navigation';
import { createClient } from '@/lib/supabase/server';
import { getMyApplicant } from '@/lib/queries';

export async function signInWithOtp(formData: FormData) {
  const email = String(formData.get('email') ?? '').trim();

  if (!email) {
    return { error: 'Email is required for Supabase OTP sign in.' };
  }

  const supabase = await createClient();
  const { error } = await supabase.auth.signInWithOtp({ email });
  if (error) return { error: error.message };

  return { success: 'Check your email for login link/OTP.' };
}

export async function submitLicence(formData: FormData) {
  const supabase = await createClient();
  const applicant = await getMyApplicant();

  if (!applicant) {
    return { error: 'Please complete applicant profile first.' };
  }

  const payload = {
    applicant_id: applicant.id,
    licence_category: String(formData.get('licence_category') ?? 'HABARI'),
    is_amateur: Boolean(formData.get('is_amateur')),
    channel_links: String(formData.get('channel_links') ?? ''),
    status: 'SUBMITTED',
    payment_status: 'UNPAID',
    review_status: 'PENDING'
  };

  const { error } = await supabase.from('applications').insert(payload);
  if (error) return { error: error.message };

  redirect('/dashboard');
}

export async function submitFund(formData: FormData) {
  const supabase = await createClient();
  const applicant = await getMyApplicant();

  if (!applicant) {
    return { error: 'Please complete applicant profile first.' };
  }

  const payload = {
    applicant_id: applicant.id,
    fund_program: String(formData.get('fund_program') ?? 'GENERAL'),
    requested_amount_tzs: Number(formData.get('requested_amount_tzs') ?? 0),
    summary_of_idea: String(formData.get('summary_of_idea') ?? ''),
    status: 'SUBMITTED',
    review_status: 'PENDING',
    is_youth_at_application: false
  };

  const { error } = await supabase.from('fund_applications').insert(payload);
  if (error) return { error: error.message };

  redirect('/dashboard');
}
