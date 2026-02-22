# Ministry Ownership Realignment (Policy + Technical Baseline)

## 1) Updated Executive Summary (Ministry-owned model)

The **Digital Content Creator Licensing Portal + Payments** is a **Ministry of Information, Culture, Arts and Sports-owned national platform** for creator licensing, compliance, and related public digital services.

The platform operationalizes Government reforms by making creator registration, licensing, and payment follow-up simple, mobile-friendly, and auditable. It is designed to implement reduced fees, support the Amateur category, and establish a trusted digital pathway from onboarding to regulatory compliance.

Under this model:
- The **Ministry** is the platform owner, host authority, and primary public-service sponsor.
- **TCRA** is the licensing authority embedded in the platform, responsible for licensing rules, review workflows, decisions, and registry integrity.
- **NMB** is a payment and distribution partner only, providing payment rails, reconciliation support, and assisted onboarding channels (branches/agents/USSD where policy permits).

The platform is also positioned as the future digital foundation for the Content Creator Empowerment Fund, with policy-led expansion managed by the Ministry and relevant public authorities.

---

## 2) Updated Context (Policy and institutional context)

### Public policy intent
The Government seeks to reduce barriers for creators, improve formal participation, support youth employment, strengthen digital innovation, and improve lawful revenue visibility.

### Institutional delivery model
To achieve those goals at national scale, delivery must be anchored in a clear ownership model:
- The **Ministry** owns and governs the platform as a public digital service.
- **TCRA** operates licensing functions on the platform under its legal mandate.
- **NMB** supports payments and access channels as an integration partner, not as platform owner.

### Why this matters
A Ministry-owned architecture protects accountability, policy continuity, and public trust. It ensures licensing authority remains public-sector controlled while still benefiting from partner payment infrastructure and field distribution channels.

### Future-ready direction
As policy evolves, the same Ministry-owned platform can safely extend into Empowerment Fund workflows (eligibility, applications, review, monitoring), without changing core governance boundaries.

---

## 3) Governance and Ownership Section (authoritative wording)

### 3.1 Ownership and control
- The **Ministry of Information, Culture, Arts and Sports** is the owner of the platform and the lead institution for hosting governance, service policy, and national rollout.
- The Ministry (with TCRA for licensing functions) acts as **data controller** for licensing-related personal and operational data.

### 3.2 Licensing authority operations
- **TCRA** is the licensing authority inside this Ministry-owned platform.
- TCRA defines categories, review criteria, approval workflows, registry status handling, and licensing audit requirements.
- Licensing decisions, reason codes, and registry actions remain under authorized Ministry/TCRA roles.

### 3.3 Payment partner boundary
- **NMB** provides payment collection interfaces, reconciliation collaboration, and assisted onboarding channels.
- NMB is a **data processor for payment events** under contract and approved interfaces.
- NMB is **not** the owner of the platform, **not** the owner of core licensing workflows, and **not** the owner/controller of licensing registry data.

### 3.4 Outsourcing principle
Even when technical services are outsourced, ownership and accountability remain with the Ministry. Vendors and partners operate as processors/service providers under Ministry-defined controls, contracts, and audit terms.

---

## 4) Technical Appendix Corrections (RFP-safe wording)

Use the following baseline wording in technical/RFP sections:

1. **Hosting and control plane**
   - The production platform shall be deployed in a **Ministry-controlled environment** (for example, Government Data Center or approved sovereign/public-sector environment).
   - Operational ownership, security governance, and change authority remain with the Ministry.

2. **Role of TCRA**
   - TCRA services are delivered as licensing modules/workflows within the Ministry-owned platform.
   - TCRA-admin roles manage licensing configuration and decisions under delegated authority.

3. **Role of NMB**
   - NMB integration is limited to payment and distribution interfaces (control number/payment status/reconciliation support and assisted channels).
   - NMB does not host or own the core licensing platform or licensing registry domain.

4. **Processor contracts**
   - Contracts must explicitly define controller/processor obligations, data minimization, retention, and audit rights for each integration or outsourced service.

---

## 5) High-level architecture restated under Ministry ownership

- **Ministry platform (system of ownership):**
  - Web application, workflow logic, licensing modules, reporting, and audit services run in Ministry-controlled infrastructure.
- **TCRA licensing domain (embedded authority):**
  - Categories, checklists, review queues, approvals/rejections, licence issuance, and registry maintenance.
- **Payment integration boundary (NMB + GePG-style rails):**
  - Ministry platform sends required billing/payment references; receives payment confirmations/callbacks.
  - Payment-side systems process only necessary payment data.
- **Data governance boundary:**
  - Ministry/TCRA retain controller visibility over licensing lifecycle data.
  - Partner access is restricted to purpose-specific datasets and interfaces.

---

## 6) Operational implications (short bullets)

### Data flows
- **Ministry/TCRA see:** full applicant/licensing workflow data, review outcomes, registry records, policy and audit outputs.
- **NMB sees:** payment reference data and payment transaction events needed for collections/reconciliation; no broad licensing-domain ownership.

### Contracts
- **Ministry ↔ NMB:** payment provider/data-processor agreement scoped to payment services.
- **Ministry ↔ hosting/IT vendors:** processor agreements for infrastructure/operations under Ministry control and audit.

### Empowerment Fund module
- Future module remains **Ministry-owned and Ministry-run**.
- NMB participation (if any) is policy-scoped (for example disbursement rails or monitoring support), not governance ownership.

---

## 7) Build-mode alignment commitment (for this Django prototype)

From this point onward, all build guidance in `creator-portal-pilot` follows this baseline:
- Treat the portal as a **Ministry system** from day one.
- Model licensing operations around **Ministry/TCRA roles** (reviewer, supervisor, policy/leadership, fund manager, finance/reconciliation).
- Keep NMB-specific logic only at payment integration and assisted channel touchpoints.
- Anchor reporting/admin/fund-related features in: **Ministry-owned platform, TCRA-embedded licensing authority, NMB as payment/distribution partner**.
