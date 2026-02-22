# Creator Portal (Next.js + Vercel)

This folder is the new stack for deploying the full portal on **Next.js + Vercel + Supabase**.

## 1) Local run

```bash
cd creator-portal-nextjs
npm install
cp .env.example .env.local
npm run dev
```

## 2) Supabase setup

1. Open Supabase SQL editor.
2. Run `supabase/schema.sql`.
3. Set env vars in `.env.local`:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY` (server-only)

## 3) Vercel deploy

1. Import this repository in Vercel.
2. Set **Root Directory** to `creator-portal-nextjs`.
3. Add the same env vars from `.env.local` in Vercel project settings.
4. Deploy.

## Notes

- This is the migration starter for moving away from Django runtime costs/limits.
- Existing Django app remains in `creator-portal-pilot` until full parity is completed.
