import Link from "next/link";
import Navbar from "../components/Navbar";

export default function GuidePage() {
  return (
    <div style={{ minHeight: "100vh", background: "#060d1a", position: "relative", overflowX: "hidden" }}>
      {/* Ambient blob */}
      <div
        style={{
          position: "fixed",
          top: "-10%",
          left: "50%",
          transform: "translateX(-50%)",
          width: "70vw",
          maxWidth: "800px",
          height: "600px",
          background: "radial-gradient(ellipse at center, rgba(16,185,129,0.06) 0%, transparent 70%)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />

      <div style={{ position: "relative", zIndex: 1 }}>
        <Navbar />

        <div className="max-w-3xl mx-auto px-6 py-16">
          {/* Page header */}
          <div className="text-center mb-14">
            <div
              className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-6"
              style={{ background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)" }}
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <span style={{ color: "#6ee7b7", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.07em", textTransform: "uppercase" }}>
                User Guide
              </span>
            </div>
            <h1 style={{ color: "#ecfdf5", fontWeight: 900, fontSize: "clamp(2rem, 4vw, 3rem)", letterSpacing: "-0.04em", marginBottom: "1rem" }}>
              How to use JobFlow
            </h1>
            <p style={{ color: "#6ee7b7", fontSize: "1rem", lineHeight: 1.7, fontWeight: 500 }}>
              Follow these five steps to go from resume to ranked job matches in minutes.
            </p>
          </div>

          {/* Steps */}
          <div className="space-y-5">
            {[
              {
                step: "01",
                title: "Upload Your Resume",
                badge: "Start here",
                badgeColor: "#10b981",
                desc: "Head to the Get Started page and find the Resume panel on the left. Click the upload area or drag and drop your PDF resume directly onto it.",
                details: [
                  "Only PDF files are accepted (max 5 MB)",
                  "Your resume is parsed once and stored for all future searches",
                  "You'll see a confirmation message when parsing is complete",
                ],
                icon: (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8L14 2z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M14 2v6h6M12 15V9M9 12l3-3 3 3" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                ),
              },
              {
                step: "02",
                title: "Extract Resume Data",
                badge: "Automatic",
                badgeColor: "#34d399",
                desc: "After uploading, click Submit Resume. JobFlow sends your PDF to the AI backend which extracts your skills, experience, education, and more.",
                details: [
                  "Parsing takes a few seconds — wait for the 'Parsed' badge to appear",
                  "Your resume ID is saved locally to link with job searches",
                  "You only need to do this once per resume",
                ],
                icon: (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                ),
              },
              {
                step: "03",
                title: "Scrape LinkedIn Jobs",
                badge: "Live data",
                badgeColor: "#10b981",
                desc: "In the Job Search panel, fill in three fields — your target role, preferred location, and the number of listings you want — then click Search Jobs.",
                details: [
                  "Role: e.g. 'Frontend Engineer', 'Product Manager', 'Data Scientist'",
                  "Location: e.g. 'Remote', 'New York', 'London'",
                  "Limit: how many listings to scrape (controls the result count)",
                  "JobFlow polls the backend until scraping is complete — this may take 30–60 seconds",
                ],
                icon: (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <circle cx="11" cy="11" r="8" stroke="white" strokeWidth="2" />
                    <path d="M21 21l-4.35-4.35" stroke="white" strokeWidth="2" strokeLinecap="round" />
                  </svg>
                ),
              },
              {
                step: "04",
                title: "Review Scores & Apply",
                badge: "AI-powered",
                badgeColor: "#34d399",
                desc: "Once scraping finishes, AI scores every job against your parsed resume. Results appear as cards with a match score, reasoning, and a direct Apply link.",
                details: [
                  "Scores range from 1–10 — higher is a better fit",
                  "Expand the reasoning to see exactly why a job matches",
                  "Click Apply on LinkedIn to open the listing in a new tab",
                  "Your resume profile is already stored, so no re-entry needed",
                ],
                icon: (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                ),
              },
              {
                step: "05",
                title: "Auto-Fill Application",
                badge: "One-click",
                badgeColor: "#10b981",
                desc: "Open the JobFiller Chrome extension on the application page and apply in one click. This auto-fills the job application form for you.",
                details: [
                  "Ensure the extension is pinned to your toolbar for easy access",
                  "Click 'Auto fill your job application form' to begin the magic",
                  "It seamlessly maps your parsed resume profile to form fields",
                ],
                icon: (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M13 10V3L4 14h7v7l9-11h-7z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                ),
              },
            ].map((s) => (
              <div
                key={s.step}
                className="rounded-2xl p-7"
                style={{
                  background: "linear-gradient(135deg, #071020 0%, #0a1628 100%)",
                  border: "1px solid rgba(16,185,129,0.14)",
                  boxShadow: "0 4px 24px rgba(0,0,0,0.3)",
                }}
              >
                <div className="flex items-start gap-5">
                  {/* Step number + icon */}
                  <div className="flex-shrink-0">
                    <div
                      className="w-12 h-12 rounded-xl flex items-center justify-center"
                      style={{ background: "linear-gradient(135deg, #065f46, #10b981)", boxShadow: "0 4px 16px rgba(16,185,129,0.3)" }}
                    >
                      {s.icon}
                    </div>
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-1 flex-wrap">
                      <span
                        style={{ color: "#2d5c47", fontSize: "0.6875rem", fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase" }}
                      >
                        Step {s.step}
                      </span>
                      <span
                        className="px-2 py-0.5 rounded-md"
                        style={{ background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.2)", color: s.badgeColor, fontSize: "0.6875rem", fontWeight: 700, letterSpacing: "0.04em", textTransform: "uppercase" }}
                      >
                        {s.badge}
                      </span>
                    </div>

                    <h3 className="mb-2" style={{ color: "#ecfdf5", fontWeight: 700, fontSize: "1.0625rem", letterSpacing: "-0.02em" }}>
                      {s.title}
                    </h3>
                    <p className="mb-4" style={{ color: "#6ee7b7", fontSize: "0.875rem", lineHeight: 1.65, fontWeight: 500 }}>
                      {s.desc}
                    </p>

                    {/* Detail bullets */}
                    <ul className="space-y-2">
                      {s.details.map((d) => (
                        <li key={d} className="flex items-start gap-2.5">
                          <span
                            className="flex-shrink-0 mt-1.5 w-1.5 h-1.5 rounded-full"
                            style={{ background: "#10b981" }}
                          />
                          <span style={{ color: "#a7f3d0", fontSize: "0.8125rem", lineHeight: 1.6, fontWeight: 500 }}>
                            {d}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <footer className="py-8 text-center" style={{ borderTop: "1px solid rgba(16,185,129,0.08)" }}>
          <p style={{ color: "#2d5c47", fontSize: "0.75rem", fontWeight: 500 }}>
            JobFlow · Powered by LinkedIn scraping &amp; Groq AI
          </p>
        </footer>
      </div>
    </div>
  );
}
