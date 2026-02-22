import { signInWithOtp } from '@/lib/actions';

export default function SignInPage() {
  return (
    <>
      <h1>Sign in (Next.js + Supabase)</h1>
      <p className="muted">
        Supabase Auth uses email OTP/magic link in this starter. You can add NIN + phone
        verification in the next step.
      </p>
      <form action={signInWithOtp}>
        <label>Email</label>
        <input type="email" name="email" placeholder="you@example.com" required />
        <button type="submit">Send OTP / Magic Link</button>
      </form>
    </>
  );
}
