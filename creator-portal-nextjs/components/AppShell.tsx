import Link from 'next/link';
import { ReactNode } from 'react';

export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <>
      <header className="header">
        <div className="logo-box">[Nembo Rasmi ya Serikali ya Tanzania]</div>
        <div>
          <strong>Ministry of Information, Culture, Arts and Sports</strong>
          <div className="muted" style={{ color: '#e5e7eb' }}>
            Digital Content Creator Program Portal
          </div>
        </div>
        <div className="logo-box">[Digital Content Creator Program Logo]</div>
      </header>
      <nav className="nav">
        <Link href="/">Home</Link>
        <Link href="/signin">Sign in</Link>
        <Link href="/dashboard">Dashboard</Link>
        <Link href="/licence/apply">Licence</Link>
        <Link href="/fund/apply">Fund</Link>
      </nav>
      <main className="container">{children}</main>
    </>
  );
}
