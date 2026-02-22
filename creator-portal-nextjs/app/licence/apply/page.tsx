import { submitLicence } from '@/lib/actions';

export default function LicenceApplyPage() {
  return (
    <>
      <h1>Omba Leseni</h1>
      <p className="muted">MVP flow ya maombi ya leseni kwa Next.js + Supabase.</p>
      <form action={submitLicence}>
        <label>Kategoria ya Leseni</label>
        <select name="licence_category" defaultValue="HABARI">
          <option value="HABARI">Habari</option>
          <option value="BURUDANI">Burudani</option>
          <option value="ELIMU">Elimu</option>
          <option value="SIMULCASTING">Simulcasting</option>
        </select>

        <label>
          <input type="checkbox" name="is_amateur" /> Amateur category
        </label>

        <label>Channel links / handles</label>
        <textarea name="channel_links" rows={6} />

        <button type="submit">Submit application</button>
      </form>
    </>
  );
}
