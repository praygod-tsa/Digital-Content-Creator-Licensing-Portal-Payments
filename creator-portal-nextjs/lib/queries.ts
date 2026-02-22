import { createClient } from '@/lib/supabase/server';

export async function getMyApplicant() {
  const supabase = await createClient();
  const {
    data: { user }
  } = await supabase.auth.getUser();

  if (!user) return null;

  const { data } = await supabase
    .from('applicants')
    .select('*')
    .eq('auth_user_id', user.id)
    .order('created_at', { ascending: false })
    .limit(1)
    .maybeSingle();

  return data;
}

export async function getMyLicenceApplications() {
  const applicant = await getMyApplicant();
  if (!applicant) return [];

  const supabase = await createClient();
  const { data } = await supabase
    .from('applications')
    .select('*')
    .eq('applicant_id', applicant.id)
    .order('created_at', { ascending: false })
    .limit(5);

  return data ?? [];
}

export async function getMyFundApplications() {
  const applicant = await getMyApplicant();
  if (!applicant) return [];

  const supabase = await createClient();
  const { data } = await supabase
    .from('fund_applications')
    .select('*')
    .eq('applicant_id', applicant.id)
    .order('created_at', { ascending: false })
    .limit(5);

  return data ?? [];
}
