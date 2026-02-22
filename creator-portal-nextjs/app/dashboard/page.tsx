import Link from 'next/link';
import { getMyApplicant, getMyFundApplications, getMyLicenceApplications } from '@/lib/queries';

export default async function DashboardPage() {
  const applicant = await getMyApplicant();
  const licences = await getMyLicenceApplications();
  const funds = await getMyFundApplications();

  return (
    <>
      <h1>Dashibodi ya Mtumiaji</h1>
      <p className="muted">
        Hii ni dashibodi ya mfumo wa Wizara kwa ajili ya kufuatilia maombi ya leseni na mfuko.
      </p>

      <div className="card">
        <h3>Profile</h3>
        {applicant ? (
          <p>
            {applicant.full_name} • {applicant.phone} • {applicant.region}
          </p>
        ) : (
          <p>No applicant profile linked to this account yet.</p>
        )}
      </div>

      <div className="grid">
        <div className="card">
          <h3>Licence Applications</h3>
          <Link href="/licence/apply">Start new</Link>
          <ul>
            {licences.map((item: any) => (
              <li key={item.id}>
                {item.licence_category} • {item.payment_status} • {item.review_status}
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h3>Empowerment Fund</h3>
          <Link href="/fund/apply">Start new</Link>
          <ul>
            {funds.map((item: any) => (
              <li key={item.id}>
                {item.fund_program} • TZS {item.requested_amount_tzs} • {item.review_status}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </>
  );
}
