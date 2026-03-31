import Link from "next/link";
import Navbar from "./components/Navbar";

export default function LandingPage() {
  return (
    <div style={{ minHeight: "100vh", background: "#060d1a", position: "relative", overflowX: "hidden" }}>
      {/* Ambient blobs */}
      <div
        style={{
          position: "fixed",
          top: "-15%",
          left: "50%",
          transform: "translateX(-50%)",
          width: "80vw",
          maxWidth: "900px",
          height: "700px",
          background: "radial-gradient(ellipse at center, rgba(16,185,129,0.07) 0%, transparent 70%)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />
      <div
        style={{
          position: "fixed",
          bottom: "0%",
          right: "-15%",
          width: "600px",
          height: "600px",
          background: "radial-gradient(ellipse at center, rgba(6,95,70,0.06) 0%, transparent 70%)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />

      <div style={{ position: "relative", zIndex: 1 }}>
        <Navbar />

        {/* ── HERO ── */}
        <section className="max-w-6xl mx-auto px-6 pt-24 pb-20 text-center">
          <div
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-8"
            style={{ background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)" }}
          >
            <span className="w-1.5 h-1.5 rounded-full glow-pulse" style={{ background: "#10b981" }} />
            <span style={{ color: "#6ee7b7", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.07em", textTransform: "uppercase" }}>
              AI-Powered Job Search
            </span>
          </div>

          <h1
            className="mb-6 leading-tight"
            style={{ color: "#ecfdf5", fontWeight: 900, fontSize: "clamp(2.5rem, 6vw, 4.25rem)", letterSpacing: "-0.04em", lineHeight: 1.1 }}
          >
            Your resume.{" "}
            <span style={{ color: "#10b981" }}>Your dream job.</span>
            <br />
            On autopilot.
          </h1>

          <p
            className="max-w-2xl mx-auto mb-10"
            style={{ color: "#a7f3d0", fontWeight: 500, fontSize: "1.125rem", lineHeight: 1.7 }}
          >
            Upload your resume once. JobFlow scrapes LinkedIn for the best matching roles,
            scores them with AI, and shows you exactly why each job fits — so you apply
            smarter, not harder.
          </p>

          {/* CTA Buttons */}
          <div className="flex items-center justify-center gap-4 flex-wrap">
            <Link href="/dashboard" style={{ textDecoration: "none" }}>
              <span
                className="inline-flex items-center gap-2.5 px-7 py-3.5 rounded-2xl font-bold"
                style={{
                  background: "linear-gradient(135deg, #059669, #10b981)",
                  color: "#ecfdf5",
                  fontSize: "1rem",
                  letterSpacing: "-0.01em",
                  boxShadow: "0 6px 24px rgba(16,185,129,0.4)",
                }}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M13 10V3L4 14h7v7l9-11h-7z" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                Get Started
              </span>
            </Link>

            <Link href="/guide" style={{ textDecoration: "none" }}>
              <span
                className="inline-flex items-center gap-2.5 px-7 py-3.5 rounded-2xl font-bold"
                style={{
                  background: "rgba(16,185,129,0.07)",
                  color: "#6ee7b7",
                  fontSize: "1rem",
                  letterSpacing: "-0.01em",
                  border: "1px solid rgba(16,185,129,0.22)",
                }}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                View Guide
              </span>
            </Link>
          </div>

          {/* Feature badges */}
          <div className="mt-14 flex items-center justify-center gap-4 flex-wrap">
            {[
              { label: "Resume Parsing", icon: "📄" },
              { label: "LinkedIn Scraping", icon: "🔍" },
              { label: "AI Fit Scoring", icon: "🤖" },
            ].map((item) => (
              <div
                key={item.label}
                className="flex items-center gap-2 px-4 py-2 rounded-full"
                style={{ background: "rgba(16,185,129,0.05)", border: "1px solid rgba(16,185,129,0.12)" }}
              >
                <span style={{ fontSize: "0.875rem" }}>{item.icon}</span>
                <span style={{ color: "#6ee7b7", fontSize: "0.8125rem", fontWeight: 600 }}>{item.label}</span>
              </div>
            ))}
          </div>
        </section>

        {/* ── WHAT IS JOBFLOW ── */}
        <section className="py-20" style={{ borderTop: "1px solid rgba(16,185,129,0.07)" }}>
          <div className="max-w-6xl mx-auto px-6">
            <div className="text-center mb-14">
              <p style={{ color: "#10b981", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "0.75rem" }}>
                About
              </p>
              <h2 style={{ color: "#ecfdf5", fontWeight: 800, fontSize: "clamp(1.75rem, 3.5vw, 2.5rem)", letterSpacing: "-0.03em" }}>
                What is JobFlow?
              </h2>
              <p className="mt-4 max-w-2xl mx-auto" style={{ color: "#6ee7b7", fontSize: "1rem", lineHeight: 1.7, fontWeight: 500 }}>
                JobFlow combines resume intelligence with live job discovery. Instead of manually
                searching and re-entering your details into dozens of forms, let AI handle the
                heavy lifting — from extraction to evaluation to application.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {[
                {
                  icon: (
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8L14 2z" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      <path d="M14 2v6h6M9 13h6M9 17h4" stroke="#10b981" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                  ),
                  title: "Resume Parsing",
                  desc: "Upload your PDF resume once. We extract your skills, experience, and background using AI — no manual input required.",
                },
                {
                  icon: (
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                      <circle cx="11" cy="11" r="8" stroke="#10b981" strokeWidth="2" />
                      <path d="M21 21l-4.35-4.35" stroke="#10b981" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                  ),
                  title: "Job Scraping",
                  desc: "We scrape LinkedIn in real time for jobs matching your role, location, and desired count — no stale listings, no subscription needed.",
                },
                {
                  icon: (
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                      <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  ),
                  title: "AI Fit Scoring",
                  desc: "Groq AI evaluates each job against your resume and gives a 1–10 fit score with a plain-English explanation of why it matches.",
                },
              ].map((item) => (
                <div
                  key={item.title}
                  className="rounded-2xl p-6"
                  style={{ background: "linear-gradient(135deg, #071020 0%, #0a1628 100%)", border: "1px solid rgba(16,185,129,0.14)", boxShadow: "0 4px 24px rgba(0,0,0,0.3)" }}
                >
                  <div
                    className="w-11 h-11 rounded-xl flex items-center justify-center mb-4"
                    style={{ background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.18)" }}
                  >
                    {item.icon}
                  </div>
                  <h3 className="mb-2" style={{ color: "#ecfdf5", fontWeight: 700, fontSize: "1rem", letterSpacing: "-0.02em" }}>
                    {item.title}
                  </h3>
                  <p style={{ color: "#6ee7b7", fontSize: "0.875rem", lineHeight: 1.65, fontWeight: 500 }}>
                    {item.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── FEATURES ── */}
        <section className="py-20" style={{ borderTop: "1px solid rgba(16,185,129,0.07)" }}>
          <div className="max-w-6xl mx-auto px-6">
            <div className="text-center mb-14">
              <p style={{ color: "#10b981", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "0.75rem" }}>
                Features
              </p>
              <h2 style={{ color: "#ecfdf5", fontWeight: 800, fontSize: "clamp(1.75rem, 3.5vw, 2.5rem)", letterSpacing: "-0.03em" }}>
                Everything you need to land faster
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {[
                {
                  tag: "Upload",
                  title: "One-click Resume Upload",
                  desc: "Drag and drop your PDF resume. We parse, store, and link it to every job search you run — automatically.",
                },
                {
                  tag: "Scrape",
                  title: "Real-time LinkedIn Scraping",
                  desc: "Enter a role, location, and limit. JobFlow pulls fresh listings from LinkedIn and returns exactly as many as you need.",
                },
                {
                  tag: "Score",
                  title: "AI Match Scoring",
                  desc: "Every job is scored 1–10 against your resume, with a detailed explanation so you can prioritize confidently.",
                },
                {
                  tag: "Apply",
                  title: "Direct Application Links",
                  desc: "Each result links straight to LinkedIn. One click and your profile does the talking — no re-entering details.",
                },
              ].map((f) => (
                <div
                  key={f.title}
                  className="rounded-2xl p-7 flex gap-5"
                  style={{ background: "linear-gradient(135deg, #071020 0%, #0a1628 100%)", border: "1px solid rgba(16,185,129,0.13)", boxShadow: "0 4px 24px rgba(0,0,0,0.3)" }}
                >
                  <div className="flex-shrink-0 pt-0.5">
                    <span
                      className="inline-block px-2.5 py-1 rounded-lg"
                      style={{ background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.2)", color: "#10b981", fontSize: "0.6875rem", fontWeight: 700, letterSpacing: "0.05em", textTransform: "uppercase" }}
                    >
                      {f.tag}
                    </span>
                  </div>
                  <div>
                    <h3 className="mb-2" style={{ color: "#ecfdf5", fontWeight: 700, fontSize: "1rem", letterSpacing: "-0.02em" }}>
                      {f.title}
                    </h3>
                    <p style={{ color: "#6ee7b7", fontSize: "0.875rem", lineHeight: 1.65, fontWeight: 500 }}>
                      {f.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── HOW IT WORKS ── */}
        <section className="py-20" style={{ borderTop: "1px solid rgba(16,185,129,0.07)" }}>
          <div className="max-w-6xl mx-auto px-6">
            <div className="text-center mb-14">
              <p style={{ color: "#10b981", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "0.75rem" }}>
                How it Works
              </p>
              <h2 style={{ color: "#ecfdf5", fontWeight: 800, fontSize: "clamp(1.75rem, 3.5vw, 2.5rem)", letterSpacing: "-0.03em" }}>
                Three steps to your next role
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                {
                  step: "01",
                  title: "Upload Resume",
                  desc: "Drag and drop your PDF. We parse it instantly and store your profile — once, for all future searches.",
                },
                {
                  step: "02",
                  title: "Search & Extract",
                  desc: "Enter your target role, location, and how many listings you want. We scrape and rank results in real time.",
                },
                {
                  step: "03",
                  title: "Review & Apply",
                  desc: "AI scores every job against your resume. See the reasoning, then apply directly on LinkedIn in one click.",
                },
              ].map((s) => (
                <div
                  key={s.step}
                  className="rounded-2xl p-7 text-center"
                  style={{ background: "linear-gradient(135deg, #071020 0%, #0a1628 100%)", border: "1px solid rgba(16,185,129,0.14)", boxShadow: "0 4px 24px rgba(0,0,0,0.3)" }}
                >
                  <div
                    className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-5"
                    style={{ background: "linear-gradient(135deg, #065f46, #10b981)", boxShadow: "0 6px 20px rgba(16,185,129,0.3)" }}
                  >
                    <span style={{ color: "#ecfdf5", fontWeight: 900, fontSize: "1rem", letterSpacing: "-0.02em" }}>
                      {s.step}
                    </span>
                  </div>
                  <h3 className="mb-2" style={{ color: "#ecfdf5", fontWeight: 700, fontSize: "1.0625rem", letterSpacing: "-0.02em" }}>
                    {s.title}
                  </h3>
                  <p style={{ color: "#6ee7b7", fontSize: "0.875rem", lineHeight: 1.65, fontWeight: 500 }}>
                    {s.desc}
                  </p>
                </div>
              ))}
            </div>

            {/* CTA */}
            <div className="text-center mt-14">
              <Link href="/dashboard" style={{ textDecoration: "none" }}>
                <span
                  className="inline-flex items-center gap-2.5 px-8 py-4 rounded-2xl font-bold"
                  style={{ background: "linear-gradient(135deg, #059669, #10b981)", color: "#ecfdf5", fontSize: "1rem", letterSpacing: "-0.01em", boxShadow: "0 6px 28px rgba(16,185,129,0.4)" }}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M13 10V3L4 14h7v7l9-11h-7z" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  Start for free — no account needed
                </span>
              </Link>
            </div>
          </div>
        </section>

        {/* ── FOOTER ── */}
        <footer className="py-8 text-center" style={{ borderTop: "1px solid rgba(16,185,129,0.08)" }}>
          <div className="flex items-center justify-center gap-2 mb-2">
            <div
              className="w-5 h-5 rounded-md flex items-center justify-center"
              style={{ background: "linear-gradient(135deg, #065f46, #10b981)" }}
            >
              <svg width="9" height="9" viewBox="0 0 24 24" fill="none">
                <path d="M9 12h6M9 16h6M9 8h3M5 3h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2z" stroke="white" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </div>
            <span style={{ color: "#2d5c47", fontSize: "0.875rem", fontWeight: 700 }}>JobFlow</span>
          </div>
          <p style={{ color: "#2d5c47", fontSize: "0.75rem", fontWeight: 500 }}>
            Powered by LinkedIn scraping &amp; Groq AI
          </p>
        </footer>
      </div>
    </div>
  );
}
