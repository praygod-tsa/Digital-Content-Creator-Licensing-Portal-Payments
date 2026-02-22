import { submitFund } from '@/lib/actions';

export default function FundApplyPage() {
  return (
    <>
      <h1>Omba Empowerment Fund</h1>
      <p className="muted">MVP flow ya maombi ya mfuko kwa Next.js + Supabase.</p>
      <form action={submitFund}>
        <label>Program</label>
        <select name="fund_program" defaultValue="GENERAL">
          <option value="GENERAL">General</option>
          <option value="TOURISM">Tourism</option>
          <option value="SPORTS">Sports</option>
          <option value="MUSIC">Music</option>
          <option value="FILM">Film</option>
        </select>

        <label>Requested amount (TZS)</label>
        <input type="number" name="requested_amount_tzs" min={1} required />

        <label>Summary of idea</label>
        <textarea name="summary_of_idea" rows={6} required />

        <button type="submit">Submit fund application</button>
      </form>
    </>
  );
}
