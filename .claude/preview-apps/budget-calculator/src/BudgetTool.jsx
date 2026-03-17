import { useState } from "react";

const PINK = "#EC1662";
const BLACK = "#000000";
const INK = "#333333";
const MID = "#666666";
const MUTED = "#999999";
const RULE = "#DDDDDD";
const BG = "#F5F5F5";
const PINK_LIGHT = "#FBD1E0";
const PINK_XLIGHT = "#FEF0F5";
const GRAY_CARD = "#F0F0F0";

function fmt(n) {
  if (n < 0) return "-$" + Math.round(-n).toLocaleString("en-US");
  return "$" + Math.round(n).toLocaleString("en-US");
}

function NumInput({ label, value, onChange, prefix, suffix, min = 0, max = 999999, step = 1, note, wide }) {
  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ fontSize: 12, color: MID, width: wide ? 180 : 150, flexShrink: 0 }}>{label}</span>
        <div style={{ display: "flex", alignItems: "center", background: "#fff", border: `1px solid ${RULE}`, borderRadius: 4, overflow: "hidden" }}>
          {prefix && <span style={{ padding: "5px 8px", background: BG, borderRight: `1px solid ${RULE}`, fontSize: 12, color: MUTED }}>{prefix}</span>}
          <input type="number" value={value} min={min} max={max} step={step}
            onChange={e => onChange(Number(e.target.value))}
            style={{ width: 72, padding: "5px 8px", border: "none", outline: "none", fontSize: 13, color: INK, fontFamily: "inherit" }} />
          {suffix && <span style={{ padding: "5px 8px", background: BG, borderLeft: `1px solid ${RULE}`, fontSize: 12, color: MUTED }}>{suffix}</span>}
        </div>
      </div>
      {note && <div style={{ fontSize: 11, color: MUTED, marginTop: 2, paddingLeft: wide ? 188 : 158, lineHeight: 1.4 }}>{note}</div>}
    </div>
  );
}

function StatBox({ label, value, sub, highlight, dim }) {
  return (
    <div style={{
      background: highlight ? PINK_LIGHT : dim ? GRAY_CARD : BG,
      borderRadius: 6, padding: "12px 14px",
      border: `1px solid ${highlight ? "#F7A3C0" : RULE}`
    }}>
      <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: highlight ? PINK : MUTED, marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 20, fontWeight: 700, color: highlight ? PINK : dim ? MUTED : BLACK }}>{value}</div>
      {sub && <div style={{ fontSize: 11, color: MUTED, marginTop: 2 }}>{sub}</div>}
    </div>
  );
}

function SectionHead({ children }) {
  return (
    <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", color: MUTED, marginBottom: 14, paddingBottom: 8, borderBottom: `1px solid ${RULE}` }}>
      {children}
    </div>
  );
}

function Tag({ color = PINK, children }) {
  return (
    <span style={{ display: "inline-block", fontSize: 10, fontWeight: 700, letterSpacing: "0.07em", textTransform: "uppercase", color, border: `1.5px solid ${color}`, borderRadius: 9999, padding: "2px 10px" }}>
      {children}
    </span>
  );
}

function RoleBadge({ label, sub, color }) {
  return (
    <div style={{ display: "inline-flex", flexDirection: "column", background: color + "18", border: `1px solid ${color}40`, borderRadius: 6, padding: "6px 12px", marginBottom: 10 }}>
      <span style={{ fontSize: 11, fontWeight: 700, color, letterSpacing: "0.05em" }}>{label}</span>
      <span style={{ fontSize: 10, color: MID, marginTop: 1 }}>{sub}</span>
    </div>
  );
}

const TRADEOFFS = {
  A: [
    { icon: "✓", col: PINK, text: "Submersive owns AI infrastructure — CRM, analytics, automation — built to last beyond the engagement" },
    { icon: "✓", col: PINK, text: "Data architecture built with Layer 2/3 biometric vision in mind from day one" },
    { icon: "✓", col: PINK, text: "Highest personalization at scale — Klaviyo behavioral journeys, anomaly detection, SEO programmatic layer" },
    { icon: "~", col: "#888", text: "Front-loaded investment — BUILD sprint is capital intensive by design" },
    { icon: "~", col: "#888", text: "Requires more coordination between Submersive and Amuse in BUILD phase" },
  ],
  B: [
    { icon: "✓", col: PINK, text: "Lower total cost — Jee delivers at base scope, Kam in background supporting her efficiency" },
    { icon: "✓", col: PINK, text: "Content + brand foundations same pace — Jee's 3-task/week execution unchanged" },
    { icon: "✓", col: PINK, text: "AI advantage baked in internally — Jee produces faster/better without client needing to own the tooling" },
    { icon: "↓", col: "#bbb", text: "No client-owned AI infrastructure — Submersive doesn't get the tech layer for their own team post-engagement" },
    { icon: "↓", col: "#bbb", text: "Reduced depth in SELL automation — Klaviyo journeys, analytics dashboards less customized" },
  ]
};

const OPEN_QS = [
  { n: 1, q: "Will Submersive bring any tech stack ops in-house post-BUILD?", impact: "Yes → Option B is clearly right. They don't need Kam building infra they'll eventually own. No → Option A's AI infrastructure has lasting ROI even after engagement ends.", affects: "Option A vs B decision" },
  { n: 2, q: "Target content volume in SELL — frequency + channel mix?", impact: "Jee's $5K base covers 3 tasks/week (copy + image + minimal responses, no video). More volume — newsletter, email flows, 5x/week — adds scope above base. This is the biggest Jee retainer lever.", affects: "Jee scope above base" },
  { n: 3, q: "Paid ads budget — are they running Meta/Google/TikTok ads?", impact: "Ad management is budget-based: industry standard 15–20% of monthly ad spend, or min ~$1K/mo. Completely separate from retainer. Submersive pays ad spend directly to platforms.", affects: "Ad management fee line" },
  { n: 4, q: "Total budget ceiling — what are Chris and Corvas working with?", impact: "Determines whether BUILD sprint is flat-fee or hourly, how much equity bridges the gap, and which option is even viable without restructuring the deal.", affects: "Deal structure / equity %" },
  { n: 5, q: "Timeline for member billing, portal, and checkin systems?", impact: "These are outside the retainer scope — they require Kam in a partner capacity (paid + equity), similar to Machina. If Submersive needs this before soft launch (March 2027), a separate partner deal should be scoped now alongside the retainer.", affects: "Partner scope / separate deal" },
];

const SCOPE_ITEMS = {
  jeeBase: [
    "Brand voice & messaging guidelines",
    "Brand identity direction (not design execution)",
    "Content strategy + editorial calendar",
    "Social media execution — 3 tasks/week (copy + image + minimal responses)",
    "Community management basics",
    "Waitlist + presale copywriting",
    "SXSW activation creative concepts",
    "Influencer seeding strategy",
  ],
  jeeAbove: [
    "Additional posts beyond 3/week",
    "Email sequences and newsletter flows",
    "Expanded community management",
    "Influencer coordination and outreach execution",
    "Event copywriting and production briefs",
  ],
  kamRetainer: [
    "Tech stack architecture + setup (Beehiiv, Klaviyo, GA4, Segment)",
    "CRM build + behavioral automation journeys",
    "Analytics dashboards + conversion tracking",
    "AI tooling for content + operations",
    "Simple landing pages (waitlist, presale)",
    "Stripe + Memberful integration for presale (Option A)",
    "Tock admissions setup",
    "Geneva community platform setup",
    "Ongoing orchestration + AI systems oversight",
  ],
  addOn: [
    { item: "Website management + feature buildout", note: "Full Webflow ongoing — beyond simple LP" },
    { item: "Video shoots + production", note: "Requires separate crew/production budget" },
    { item: "Sales system integration (complex CRM→POS flows)", note: "Beyond standard Klaviyo automation" },
    { item: "Member billing + portal system", note: "Machina model — Kam as partner (paid + equity)" },
    { item: "Physical venue checkin + access systems", note: "Machina model — hardware + software integration" },
    { item: "Wearable integrations + biometric data layer", note: "Layer 2/3 — separate partner scope" },
    { item: "Health app or branded consumer app", note: "Machina model — product partnership, not retainer" },
  ],
};

export default function BudgetTool() {
  const [tab, setTab] = useState("A");

  // ── Rates ──
  const [kamStd, setKamStd] = useState(500);
  const [kamStartup, setKamStartup] = useState(250);
  const [jeeBaseRate, setJeeBaseRate] = useState(175);       // hourly above the $5K base
  const [equityPct, setEquityPct] = useState(1.0);

  // ── Ad management ──
  const [adSpend, setAdSpend] = useState(3000);
  const [adMgmtPct, setAdMgmtPct] = useState(15);
  const adMgmtFee = Math.max(adSpend * (adMgmtPct / 100), 1000);

  // ── Option A BUILD ──
  const [aKamBuildWk, setAKamBuildWk] = useState(25);
  const [aJeeBuildWk, setAJeeBuildWk] = useState(20);
  const [aBuildWks, setABuildWks] = useState(6);

  // ── Option A Retainer ──
  const [aKamRetMo, setAKamRetMo] = useState(20);
  const [aJeeAboveBase, setAJeeAboveBase] = useState(15);  // hrs above $5K base/mo

  // ── Option B BUILD ──
  const [bKamBuildWk, setBKamBuildWk] = useState(8);   // advisory / background
  const [bJeeBuildWk, setBJeeBuildWk] = useState(20);
  const [bBuildWks, setBBuildWks] = useState(6);

  // ── Option B Retainer ──
  const [bKamBgMo, setBKamBgMo] = useState(8);          // background support hrs
  const [bJeeAboveBase, setBJeeAboveBase] = useState(5); // smaller additional scope

  // ── Derived: A ──
  const aKamBuildHrs = aKamBuildWk * aBuildWks;
  const aJeeBuildHrs = aJeeBuildWk * aBuildWks;
  const aBuildStd = aKamBuildHrs * kamStd + aJeeBuildHrs * jeeBaseRate;
  const aBuildStartup = aKamBuildHrs * kamStartup + aJeeBuildHrs * jeeBaseRate;
  const aBuildDelta = aBuildStd - aBuildStartup;
  const aKamRetCost = Math.max(aKamRetMo * kamStartup, 5000);
  const aJeeRetCost = 5000 + aJeeAboveBase * jeeBaseRate; // $5K base + additional scope
  const aRetMoTotal = aKamRetCost + aJeeRetCost;
  const aRetMoWithAds = aRetMoTotal + adMgmtFee;
  const aY1Startup = aBuildStartup + aRetMoWithAds * 10;

  // ── Derived: B ──
  const bKamBuildHrs = bKamBuildWk * bBuildWks;
  const bJeeBuildHrs = bJeeBuildWk * bBuildWks;
  const bBuildStd = bKamBuildHrs * kamStd + bJeeBuildHrs * jeeBaseRate;
  const bBuildStartup = bKamBuildHrs * kamStartup + bJeeBuildHrs * jeeBaseRate;
  const bBuildDelta = bBuildStd - bBuildStartup;
  const bKamBgCost = Math.max(bKamBgMo * kamStartup, 5000); // floor still applies
  const bJeeRetCost = 5000 + bJeeAboveBase * jeeBaseRate;
  const bRetMoTotal = bKamBgCost + bJeeRetCost;
  const bRetMoWithAds = bRetMoTotal + adMgmtFee;
  const bY1Startup = bBuildStartup + bRetMoWithAds * 10;

  const card = { background: "#fff", border: `1px solid ${RULE}`, borderRadius: 8, padding: "20px 22px", marginBottom: 14, boxShadow: "0 1px 4px rgba(0,0,0,0.04)" };
  const tabStyle = (t) => ({
    padding: "7px 16px", borderRadius: 20, cursor: "pointer", fontSize: 11,
    fontWeight: 700, letterSpacing: "0.07em", textTransform: "uppercase",
    border: `1.5px solid ${tab === t ? PINK : RULE}`,
    background: tab === t ? PINK : "#fff",
    color: tab === t ? "#fff" : MUTED,
  });

  return (
    <div style={{ fontFamily: "'Nunito Sans', -apple-system, Helvetica, Arial, sans-serif", background: BG, minHeight: "100vh", padding: "32px 18px 60px" }}>
      <div style={{ maxWidth: 800, margin: "0 auto" }}>

        {/* Header */}
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 22 }}>
          <div>
            <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", color: MUTED }}>Budget Planning Tool · Working Draft</div>
            <h1 style={{ fontSize: 24, fontWeight: 400, color: BLACK, marginTop: 4, letterSpacing: "-0.01em" }}>
              Amuse × <span style={{ color: PINK }}>Submersive</span>
            </h1>
            <div style={{ fontSize: 12, color: MUTED, marginTop: 2 }}>ROM planning — Option A (Full Build) vs Option B (Agency Execution)</div>
          </div>
          <div style={{ textAlign: "right", fontSize: 11, color: MUTED }}>
            <div>March 10, 2026</div>
            <div style={{ marginTop: 2 }}>Confidential working draft</div>
          </div>
        </div>

        {/* ── RATE CONFIG ── */}
        <div style={{ ...card, borderTop: `3px solid ${PINK}` }}>
          <SectionHead>Rate Configuration — adjust to update all figures</SectionHead>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 24 }}>

            <div>
              <RoleBadge label="Kam" sub="Strategy + Systems + AI" color={PINK} />
              <NumInput label="Standard rate" value={kamStd} onChange={setKamStd} prefix="$" suffix="/hr" />
              <NumInput label="Startup rate" value={kamStartup} onChange={setKamStartup} prefix="$" suffix="/hr" note="Delta bridged by equity/deal" />
              <div style={{ fontSize: 11, color: MUTED, marginTop: 4, lineHeight: 1.5 }}>Floor: $5K/20hrs on retainer. Both options.</div>
            </div>

            <div>
              <RoleBadge label="Jee" sub="Brand Voice + Execution" color="#9B5DE5" />
              <NumInput label="Hourly (above base)" value={jeeBaseRate} onChange={setJeeBaseRate} prefix="$" suffix="/hr"
                note="Base $5K/mo = strategy + 3 tasks/wk (copy + image + minimal responses, no video). Hours above this billed at hourly." />
            </div>

            <div>
              <RoleBadge label="Deal structure" sub="Equity / startup terms" color="#0D6EFD" />
              <NumInput label="Equity offset %" value={equityPct} onChange={setEquityPct} suffix="%" min={0} max={10} step={0.25}
                note="% of cap table bridging rate delta to standard" />
              <div style={{ marginTop: 10, padding: "8px 10px", background: PINK_XLIGHT, borderRadius: 4, border: `1px solid #F7A3C0`, fontSize: 11, color: MID, lineHeight: 1.5 }}>
                Amuse works within client budget + manages it. Delta to minimums → equity or rev-share deal.
              </div>
            </div>
          </div>
        </div>

        {/* ── AD MANAGEMENT ── */}
        <div style={{ ...card, borderLeft: `3px solid #F7A800` }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
            <SectionHead>Ad Management — separate budget line (industry standard)</SectionHead>
            <Tag color="#F7A800">Always separate from retainer</Tag>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 20 }}>
            <div>
              <NumInput label="Monthly ad spend" value={adSpend} onChange={setAdSpend} prefix="$" wide
                note="Client pays this directly to Meta/Google/etc. Not Amuse revenue." />
            </div>
            <div>
              <NumInput label="Mgmt fee %" value={adMgmtPct} onChange={setAdMgmtPct} suffix="%" min={10} max={25} step={1} wide
                note="Industry standard: 15–20% of ad spend. Min floor ~$1K/mo." />
            </div>
            <div>
              <StatBox label="Ad mgmt fee/mo" value={fmt(adMgmtFee)} highlight sub={adSpend * adMgmtPct / 100 < 1000 ? "Floor applied at $1K/mo" : `${adMgmtPct}% of spend`} />
            </div>
          </div>
          <div style={{ marginTop: 12, fontSize: 12, color: MID, lineHeight: 1.6, background: "#FFFBEF", padding: "10px 12px", borderRadius: 4, border: "1px solid #F7E4A0" }}>
            <strong style={{ color: INK }}>Pricing note:</strong> Industry standard is 15–20% of monthly ad spend, with a minimum flat fee (typically $1–1.5K/month). For smaller budgets (&lt;$5K/mo spend), a flat fee is often cleaner. Client pays platform spend directly — mgmt fee is billed separately on top.
          </div>
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
          {[["A", "Option A — Full Build"], ["B", "Option B — Agency Exec"], ["compare", "Compare"], ["scope", "Scope Map"], ["questions", "Open Qs"]].map(([t, label]) => (
            <button key={t} style={tabStyle(t)} onClick={() => setTab(t)}>{label}</button>
          ))}
        </div>

        {/* ── OPTION A ── */}
        {tab === "A" && (<>
          <div style={{ ...card, borderTop: `2px solid ${PINK}` }}>
            <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 6 }}>
              <div>
                <div style={{ fontSize: 15, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Option A — Integrated Launch Partner</div>
                <div style={{ fontSize: 12, color: MID, marginBottom: 14 }}>Kam builds AI infrastructure <em>for Submersive</em> — client owns the tech layer. Jee at expanded scope.</div>
              </div>
              <Tag color={PINK}>Front-loaded by design</Tag>
            </div>
            <SectionHead>BUILD Sprint · 6-Week Infrastructure + Brand Foundation</SectionHead>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginBottom: 16 }}>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Kam — Systems + AI Infra Build</div>
                <div style={{ fontSize: 11, color: MID, marginBottom: 10, lineHeight: 1.5 }}>CRM architecture, landing page, analytics, AI tooling built for Submersive's team. Near-full capacity by design.</div>
                <NumInput label="Hrs/week" value={aKamBuildWk} onChange={setAKamBuildWk} suffix="hrs" max={40} />
                <NumInput label="Sprint length" value={aBuildWks} onChange={setABuildWks} suffix="wks" min={4} max={12} />
                <div style={{ fontSize: 12, color: MID, marginTop: 4 }}>
                  Total: <strong>{aKamBuildHrs} hrs</strong> · Std: <span style={{ color: PINK }}>{fmt(aKamBuildHrs * kamStd)}</span> · Startup: {fmt(aKamBuildHrs * kamStartup)}
                </div>
              </div>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Jee — Brand Voice + Content Foundations</div>
                <div style={{ fontSize: 11, color: MID, marginBottom: 10, lineHeight: 1.5 }}>Brand voice guidelines, content calendar, social strategy, newsletter framework. Same delivery pace as Option B.</div>
                <NumInput label="Hrs/week" value={aJeeBuildWk} onChange={setAJeeBuildWk} suffix="hrs" max={40} />
                <div style={{ marginTop: 28 }} />
                <div style={{ fontSize: 12, color: MID, marginTop: 4 }}>
                  Total: <strong>{aJeeBuildHrs} hrs</strong> · Cost: {fmt(aJeeBuildHrs * jeeBaseRate)}
                </div>
              </div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
              <StatBox label="BUILD · Standard rate" value={fmt(aBuildStd)} sub={`${aKamBuildHrs + aJeeBuildHrs} total hrs`} />
              <StatBox label="BUILD · Startup rate" value={fmt(aBuildStartup)} highlight />
              <StatBox label="Delta → equity bridge" value={fmt(aBuildDelta)} sub={`≈ ${equityPct}% equity offset`} />
            </div>
          </div>

          <div style={card}>
            <SectionHead>SELL / OPEN Retainer · Option A (per month, ongoing)</SectionHead>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginBottom: 16 }}>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Kam — Orchestration + AI Systems Oversight</div>
                <div style={{ fontSize: 11, color: MID, marginBottom: 10 }}>Maintains + evolves the AI layer built in BUILD. Analytics oversight, automation tuning.</div>
                <NumInput label="Hrs/month" value={aKamRetMo} onChange={setAKamRetMo} suffix="hrs" note="Floor: $5K/mo regardless of hours" />
                <div style={{ fontSize: 12, color: MID, marginTop: 2 }}>Cost: {fmt(aKamRetCost)}/mo {aKamRetMo * kamStartup < 5000 ? "⚠ floor" : ""}</div>
              </div>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Jee — Ongoing Execution</div>
                <div style={{ fontSize: 11, color: MID, marginBottom: 10 }}>$5K base = strategy + 3 tasks/wk. Additional scope (newsletter, email flows, 5x/wk, etc.) billed hourly.</div>
                <NumInput label="Hours above base" value={aJeeAboveBase} onChange={setAJeeAboveBase} suffix="hrs" note="Base $5K always applies. These are additional." />
                <div style={{ fontSize: 12, color: MID, marginTop: 2 }}>Cost: $5,000 base + {fmt(aJeeAboveBase * jeeBaseRate)} = {fmt(aJeeRetCost)}/mo</div>
              </div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 10 }}>
              <StatBox label="Kam/mo" value={fmt(aKamRetCost)} />
              <StatBox label="Jee/mo" value={fmt(aJeeRetCost)} />
              <StatBox label="+ Ad mgmt" value={fmt(adMgmtFee)} />
              <StatBox label="Total/mo" value={fmt(aRetMoWithAds)} highlight />
            </div>
            <div style={{ marginTop: 14, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
              <StatBox label="Retainer only (no ads)" value={fmt(aRetMoTotal)} sub="Kam + Jee" />
              <StatBox label="Year 1 total (BUILD + 10mo)" value={fmt(aY1Startup)} sub="Startup rates + ad mgmt" highlight />
            </div>
          </div>

          <div style={{ ...card, borderLeft: `3px solid ${PINK}` }}>
            <SectionHead>Option A — Strategic tradeoffs</SectionHead>
            {TRADEOFFS.A.map(({ icon, col, text }, i) => (
              <div key={i} style={{ display: "flex", gap: 10, marginBottom: 8, fontSize: 13, color: INK }}>
                <span style={{ color: col, fontWeight: 700, flexShrink: 0, width: 16 }}>{icon}</span>
                {text}
              </div>
            ))}
          </div>
        </>)}

        {/* ── OPTION B ── */}
        {tab === "B" && (<>
          <div style={{ ...card, borderTop: `2px solid ${MID}` }}>
            <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 6 }}>
              <div>
                <div style={{ fontSize: 15, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Option B — Agency Execution Model</div>
                <div style={{ fontSize: 12, color: MID, marginBottom: 14 }}>Jee delivers at $5K base scope. Kam works in the background — AI is <em>agency-internal</em> to make Jee more efficient. Submersive doesn't own the AI layer.</div>
              </div>
              <Tag color={MID}>Kam in background</Tag>
            </div>
            <SectionHead>BUILD Sprint · Brand + Content Foundation (Jee-led)</SectionHead>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginBottom: 16 }}>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Kam — Advisory + Internal AI Support</div>
                <div style={{ fontSize: 11, color: MID, marginBottom: 10, lineHeight: 1.5 }}>Sets up agency-internal AI tools to power Jee's delivery. Strategic oversight. Not building client-owned infra. Light touch.</div>
                <NumInput label="Hrs/week" value={bKamBuildWk} onChange={setBKamBuildWk} suffix="hrs" max={20} />
                <NumInput label="Sprint length" value={bBuildWks} onChange={setBBuildWks} suffix="wks" min={4} max={12} />
                <div style={{ fontSize: 12, color: MID, marginTop: 4 }}>
                  Total: <strong>{bKamBuildHrs} hrs</strong> · Std: <span style={{ color: PINK }}>{fmt(bKamBuildHrs * kamStd)}</span> · Startup: {fmt(bKamBuildHrs * kamStartup)}
                </div>
              </div>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Jee — Brand Voice + Content Foundations</div>
                <div style={{ fontSize: 11, color: MID, marginBottom: 10, lineHeight: 1.5 }}>Same deliverables as Option A — brand voice, content calendar, social strategy. AI-powered internally for efficiency.</div>
                <NumInput label="Hrs/week" value={bJeeBuildWk} onChange={setBJeeBuildWk} suffix="hrs" max={40} />
                <div style={{ marginTop: 28 }} />
                <div style={{ fontSize: 12, color: MID, marginTop: 4 }}>
                  Total: <strong>{bJeeBuildHrs} hrs</strong> · Cost: {fmt(bJeeBuildHrs * jeeBaseRate)}
                </div>
              </div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
              <StatBox label="BUILD · Standard" value={fmt(bBuildStd)} sub={`${bKamBuildHrs + bJeeBuildHrs} total hrs`} dim />
              <StatBox label="BUILD · Startup rate" value={fmt(bBuildStartup)} highlight />
              <StatBox label="Delta → equity bridge" value={fmt(bBuildDelta)} sub={`≈ ${equityPct}% equity`} dim />
            </div>
          </div>

          <div style={card}>
            <SectionHead>SELL Retainer · Option B (per month, ongoing)</SectionHead>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginBottom: 16 }}>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Kam — Background Support</div>
                <div style={{ fontSize: 11, color: MID, marginBottom: 10 }}>Agency-internal AI maintenance, occasional strategic input. Floor still applies.</div>
                <NumInput label="Hrs/month" value={bKamBgMo} onChange={setBKamBgMo} suffix="hrs" note="Floor: $5K/mo regardless. At 8 hrs, floor kicks in." />
                <div style={{ fontSize: 12, color: MID, marginTop: 2 }}>
                  Cost: {fmt(bKamBgCost)}/mo {bKamBgMo * kamStartup < 5000 ? <span style={{ color: "#F7A800" }}>⚠ floor at $5K</span> : ""}
                </div>
              </div>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: BLACK, marginBottom: 4 }}>Jee — Base Execution</div>
                <div style={{ fontSize: 11, color: MID, marginBottom: 10 }}>$5K base: strategy + 3 tasks/wk. Limited additional scope in this option.</div>
                <NumInput label="Hours above base" value={bJeeAboveBase} onChange={setBJeeAboveBase} suffix="hrs" note="Smaller additional scope vs Option A" />
                <div style={{ fontSize: 12, color: MID, marginTop: 2 }}>Cost: $5,000 base + {fmt(bJeeAboveBase * jeeBaseRate)} = {fmt(bJeeRetCost)}/mo</div>
              </div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 10 }}>
              <StatBox label="Kam/mo" value={fmt(bKamBgCost)} dim />
              <StatBox label="Jee/mo" value={fmt(bJeeRetCost)} />
              <StatBox label="+ Ad mgmt" value={fmt(adMgmtFee)} />
              <StatBox label="Total/mo" value={fmt(bRetMoWithAds)} highlight />
            </div>
            <div style={{ marginTop: 14, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
              <StatBox label="Retainer only (no ads)" value={fmt(bRetMoTotal)} sub="Kam + Jee" dim />
              <StatBox label="Year 1 total (BUILD + 10mo)" value={fmt(bY1Startup)} sub="Startup rates + ad mgmt" highlight />
            </div>
          </div>

          <div style={{ ...card, borderLeft: `3px solid ${MUTED}` }}>
            <SectionHead>Option B — Strategic tradeoffs</SectionHead>
            {TRADEOFFS.B.map(({ icon, col, text }, i) => (
              <div key={i} style={{ display: "flex", gap: 10, marginBottom: 8, fontSize: 13, color: INK }}>
                <span style={{ color: col, fontWeight: 700, flexShrink: 0, width: 16 }}>{icon}</span>
                {text}
              </div>
            ))}
          </div>
        </>)}

        {/* ── COMPARE ── */}
        {tab === "compare" && (
          <div style={card}>
            <SectionHead>Side-by-Side Comparison</SectionHead>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
              <thead>
                <tr>
                  <th style={{ textAlign: "left", padding: "8px 12px", borderBottom: `2px solid ${RULE}`, fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.07em", color: MUTED, width: "40%" }}>Item</th>
                  <th style={{ textAlign: "right", padding: "8px 12px", borderBottom: `2px solid ${RULE}`, fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.07em", color: PINK }}>Option A<br /><span style={{ fontWeight: 400, fontSize: 10, color: MUTED }}>Integrated Build</span></th>
                  <th style={{ textAlign: "right", padding: "8px 12px", borderBottom: `2px solid ${RULE}`, fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.07em", color: MID }}>Option B<br /><span style={{ fontWeight: 400, fontSize: 10 }}>Agency Execution</span></th>
                  <th style={{ textAlign: "right", padding: "8px 12px", borderBottom: `2px solid ${RULE}`, fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.07em", color: MUTED }}>Delta</th>
                </tr>
              </thead>
              <tbody>
                {[
                  ["BUILD total hours", `${aKamBuildHrs + aJeeBuildHrs} hrs`, `${bKamBuildHrs + bJeeBuildHrs} hrs`, `${(aKamBuildHrs + aJeeBuildHrs) - (bKamBuildHrs + bJeeBuildHrs)} hrs`],
                  ["BUILD · Startup rate", fmt(aBuildStartup), fmt(bBuildStartup), fmt(aBuildStartup - bBuildStartup)],
                  ["BUILD · Equity delta", fmt(aBuildDelta), fmt(bBuildDelta), fmt(aBuildDelta - bBuildDelta)],
                  ["Kam retainer/mo", fmt(aKamRetCost), fmt(bKamBgCost), fmt(aKamRetCost - bKamBgCost)],
                  ["Jee retainer/mo", fmt(aJeeRetCost), fmt(bJeeRetCost), fmt(aJeeRetCost - bJeeRetCost)],
                  ["Ad mgmt fee/mo", fmt(adMgmtFee), fmt(adMgmtFee), "$0"],
                  ["Total monthly (with ads)", fmt(aRetMoWithAds), fmt(bRetMoWithAds), fmt(aRetMoWithAds - bRetMoWithAds)],
                  ["Year 1 total · Startup", fmt(aY1Startup), fmt(bY1Startup), fmt(aY1Startup - bY1Startup)],
                ].map(([label, a, b, delta], i) => (
                  <tr key={i} style={{ background: i % 2 === 0 ? "#fafafa" : "#fff" }}>
                    <td style={{ padding: "10px 12px", color: INK, borderBottom: `1px solid ${RULE}` }}>{label}</td>
                    <td style={{ padding: "10px 12px", textAlign: "right", fontWeight: 700, color: PINK, borderBottom: `1px solid ${RULE}` }}>{a}</td>
                    <td style={{ padding: "10px 12px", textAlign: "right", fontWeight: 600, color: INK, borderBottom: `1px solid ${RULE}` }}>{b}</td>
                    <td style={{ padding: "10px 12px", textAlign: "right", fontWeight: 500, color: MUTED, borderBottom: `1px solid ${RULE}`, fontSize: 12 }}>{delta}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{ marginTop: 16, padding: "14px 16px", background: PINK_XLIGHT, borderRadius: 6, border: `1px solid #F7A3C0`, fontSize: 13, color: INK, lineHeight: 1.7 }}>
              <strong>Key distinction:</strong> Option A costs more in BUILD because Kam is building client-owned AI infrastructure — CRM architecture, analytics, automation — that Submersive keeps long-term. Option B's savings come from Kam staying in the background. The ongoing retainer delta is mainly Kam's scope; Jee's $5K base is the floor in both options. Ad management is identical — separate budget in both.
            </div>
            <div style={{ marginTop: 10, padding: "12px 14px", background: "#FFFBEF", borderRadius: 6, border: "1px solid #F7E4A0", fontSize: 12, color: INK, lineHeight: 1.7 }}>
              <strong>What's not in either option:</strong> Website management, video shoots, sales system integration, member billing/portal, checkin systems, and wearable integrations are all add-on or partner scope — see the <strong>Scope Map</strong> tab. These require a separate deal structure (Machina model for deep tech).
            </div>
          </div>
        )}

        {/* ── SCOPE MAP ── */}
        {tab === "scope" && (
          <div>
            <div style={{ ...card, borderTop: `3px solid ${PINK}` }}>
              <SectionHead>What's included in the engagement</SectionHead>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 700, color: "#9B5DE5", marginBottom: 10, display: "flex", alignItems: "center", gap: 6 }}>
                    <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: "50%", background: "#9B5DE5" }} />
                    Jee — Base retainer ($5K/mo)
                  </div>
                  {SCOPE_ITEMS.jeeBase.map((s, i) => (
                    <div key={i} style={{ display: "flex", gap: 8, fontSize: 12, color: INK, marginBottom: 6, alignItems: "flex-start" }}>
                      <span style={{ color: "#9B5DE5", fontWeight: 700, flexShrink: 0 }}>✓</span>{s}
                    </div>
                  ))}
                  <div style={{ marginTop: 12, padding: "8px 10px", background: "#F5EEFF", borderRadius: 4, border: "1px solid #D4AAFF", fontSize: 11, color: MID, lineHeight: 1.5 }}>
                    Base covers strategy + 3 tasks/week. No video, shoots, or production.
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 700, color: "#9B5DE5", marginBottom: 10, display: "flex", alignItems: "center", gap: 6 }}>
                    <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: "50%", background: "#c8a0f5" }} />
                    Jee — Above base (hourly at ~$175/hr)
                  </div>
                  {SCOPE_ITEMS.jeeAbove.map((s, i) => (
                    <div key={i} style={{ display: "flex", gap: 8, fontSize: 12, color: INK, marginBottom: 6, alignItems: "flex-start" }}>
                      <span style={{ color: "#c8a0f5", fontWeight: 700, flexShrink: 0 }}>+</span>{s}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div style={{ ...card, borderTop: `3px solid ${PINK}` }}>
              <div style={{ fontSize: 12, fontWeight: 700, color: PINK, marginBottom: 12, display: "flex", alignItems: "center", gap: 6 }}>
                <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: "50%", background: PINK }} />
                Kam — Retainer scope (Option A: client-owned infra / Option B: agency-internal)
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                {SCOPE_ITEMS.kamRetainer.map((s, i) => (
                  <div key={i} style={{ display: "flex", gap: 8, fontSize: 12, color: INK, alignItems: "flex-start" }}>
                    <span style={{ color: PINK, fontWeight: 700, flexShrink: 0 }}>✓</span>{s}
                  </div>
                ))}
              </div>
              <div style={{ marginTop: 12, padding: "8px 10px", background: PINK_XLIGHT, borderRadius: 4, border: `1px solid #F7A3C0`, fontSize: 11, color: MID, lineHeight: 1.5 }}>
                <strong>Option A:</strong> Submersive owns all tooling built. <strong>Option B:</strong> Same outputs, but tooling stays agency-internal — Submersive gets the content/strategy, not the infrastructure.
              </div>
            </div>

            <div style={{ ...card, borderTop: `3px solid #F7A800` }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#C47F00", display: "flex", alignItems: "center", gap: 6 }}>
                  <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: "50%", background: "#F7A800" }} />
                  Add-on / Partner scope — outside base engagement
                </div>
                <Tag color="#F7A800">Separate deal required</Tag>
              </div>
              <div style={{ marginBottom: 12, fontSize: 12, color: MID, lineHeight: 1.6 }}>
                These require a separate scope + deal structure. Deep tech items (billing, portal, wearables) follow the <strong>Machina model</strong>: Kam engages as a paid partner with equity, not an hourly retainer. Think of it as Kam joining as a co-founder for that product layer, not a contractor.
              </div>
              {SCOPE_ITEMS.addOn.map(({ item, note }, i) => (
                <div key={i} style={{ display: "flex", gap: 12, marginBottom: 10, padding: "10px 12px", background: "#FFFBEF", borderRadius: 4, border: "1px solid #F7E4A0", alignItems: "flex-start" }}>
                  <span style={{ color: "#F7A800", fontWeight: 700, flexShrink: 0, marginTop: 1 }}>◦</span>
                  <div>
                    <div style={{ fontSize: 12, fontWeight: 700, color: INK }}>{item}</div>
                    <div style={{ fontSize: 11, color: MID, marginTop: 2 }}>{note}</div>
                  </div>
                </div>
              ))}
              <div style={{ marginTop: 14, padding: "12px 14px", background: "#FFF8E6", borderRadius: 6, border: "1px solid #F7E4A0", fontSize: 12, color: INK, lineHeight: 1.7 }}>
                <strong>Machina precedent:</strong> Kam built the member billing + portal, everything physical in the health-location, wearable integrations, and health-plan apps as a Machina partner (paid + equity). Jee handled social, digital, and marketing. Same model applies if Submersive needs these layers — scope them separately before the BUILD sprint locks in.
              </div>
            </div>
          </div>
        )}

        {/* ── OPEN QUESTIONS ── */}
        {tab === "questions" && (
          <div style={card}>
            <SectionHead>Open Questions for Chris — answers change these numbers materially</SectionHead>
            {OPEN_QS.map(({ n, q, impact, affects }) => (
              <div key={n} style={{ display: "grid", gridTemplateColumns: "32px 1fr", gap: 14, padding: "16px 0", borderBottom: n < OPEN_QS.length ? `1px solid ${RULE}` : "none" }}>
                <div style={{ width: 28, height: 28, borderRadius: "50%", background: PINK, color: "#fff", fontSize: 12, fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{n}</div>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 700, color: BLACK, marginBottom: 4 }}>{q}</div>
                  <div style={{ fontSize: 12, color: MID, lineHeight: 1.65, marginBottom: 6 }}>{impact}</div>
                  <Tag color={PINK}>{affects}</Tag>
                </div>
              </div>
            ))}
            <div style={{ marginTop: 16, padding: "12px 14px", background: BG, borderRadius: 6, fontSize: 12, color: MID, lineHeight: 1.6 }}>
              <strong style={{ color: INK }}>Next step:</strong> Once Chris answers Q1 (in-house tech?) and Q3 (ad budget?), adjust the rate config + ad spend above → the Compare tab becomes the sendable ROM. Q4 (budget ceiling) determines whether the equity bridge even needs to be in the reply or handled on a call.
            </div>
          </div>
        )}

        <div style={{ textAlign: "center", fontSize: 11, color: MUTED, marginTop: 10 }}>
          Working draft · adjust any input above to update all figures · rates, hours, and ad spend are all live
        </div>
      </div>
    </div>
  );
}
