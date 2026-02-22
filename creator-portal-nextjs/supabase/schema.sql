-- Minimal schema for Next.js + Supabase migration starter.
-- Run this in Supabase SQL editor.

create extension if not exists pgcrypto;

create table if not exists applicants (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid,
  national_id_number text,
  phone text,
  email text,
  date_of_birth date,
  full_name text,
  region text,
  main_content_category text,
  creator_type text,
  created_at timestamptz not null default now()
);

create table if not exists applications (
  id uuid primary key default gen_random_uuid(),
  applicant_id uuid not null references applicants(id) on delete cascade,
  licence_category text not null,
  is_amateur boolean not null default false,
  channel_links text,
  status text not null default 'SUBMITTED',
  payment_status text not null default 'UNPAID',
  review_status text not null default 'PENDING',
  created_at timestamptz not null default now()
);

create table if not exists fund_applications (
  id uuid primary key default gen_random_uuid(),
  applicant_id uuid not null references applicants(id) on delete cascade,
  fund_program text not null,
  requested_amount_tzs integer not null,
  summary_of_idea text not null,
  status text not null default 'SUBMITTED',
  review_status text not null default 'PENDING',
  is_youth_at_application boolean not null default false,
  created_at timestamptz not null default now()
);

create index if not exists idx_applications_applicant on applications(applicant_id);
create index if not exists idx_fund_applications_applicant on fund_applications(applicant_id);
