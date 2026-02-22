import Link from 'next/link';

export default function HomePage() {
  return (
    <>
      <h1>Karibu kwenye Digital Content Creator Program Portal</h1>
      <p className="muted">
        Huu ni mfumo wa Wizara wa kusajili waundaji wa maudhui, kuendesha maombi ya leseni,
        na maombi ya Mfuko wa Uwezeshaji (Empowerment Fund).
      </p>
      <div className="grid">
        <div className="card">
          <h3>Applicant Journey</h3>
          <p>Sign in kwa NIN + OTP na simamia maombi yako.</p>
          <Link href="/signin">Anza Sign in</Link>
        </div>
        <div className="card">
          <h3>Licence</h3>
          <p>Omba leseni, fuatilia invoice na review status.</p>
          <Link href="/licence/apply">Omba Leseni</Link>
        </div>
        <div className="card">
          <h3>Empowerment Fund</h3>
          <p>Tuma ombi la mfuko kwa programu mbalimbali.</p>
          <Link href="/fund/apply">Omba Fund</Link>
        </div>
      </div>
    </>
  );
}
