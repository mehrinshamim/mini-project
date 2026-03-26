"use client";

import { useState } from "react";
import ResumeSection from "./components/ResumeSection";
import JobCard from "./components/JobCard";
import type { Job } from "./types";
import JobSearchWithResults from "./components/JobSearchWithResults";

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>([]);

  return (
    <div style={{ minHeight: "100vh", background: "#060d1a", position: "relative" }}>
      {/* Background blobs */}
      <div
        style={{
          position: "fixed",
          top: "-20%",
          left: "50%",
          transform: "translateX(-50%)",
          width: "80vw",
          maxWidth: "900px",
          height: "600px",
          background: "radial-gradient(ellipse at center, rgba(16,185,129,0.07) 0%, transparent 70%)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />
      <div
        style={{
          position: "fixed",
          bottom: "10%",
          right: "-10%",
          width: "500px",
          height: "500px",
          background: "radial-gradient(ellipse at center, rgba(6,95,70,0.06) 0%, transparent 70%)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />

      <div style={{ position: "relative", zIndex: 1 }}>
        {/* Nav */}
        <nav
          className="sticky top-0 z-50"
          style={{
            background: "rgba(6,13,26,0.85)",
            backdropFilter: "blur(16px)",
            borderBottom: "1px solid rgba(16,185,129,0.1)",
          }}
        >
          <div className="max-w-5xl mx-auto px-5 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div
                className="w-8 h-8 rounded-xl flex items-center justify-center"
                style={{ background: "linear-gradient(135deg, #065f46, #10b981)", boxShadow: "0 3px 12px rgba(16,185,129,0.35)" }}
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                  <path d="M9 12h6M9 16h6M9 8h3M5 3h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2z" stroke="white" strokeWidth="2" strokeLinecap="round" />
                  <circle cx="18" cy="18" r="4" fill="#10b981" stroke="white" strokeWidth="1.5" />
                  <path d="M16.5 18l1.2 1.2L20 16.5" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <span style={{ color: "#ecfdf5", fontWeight: 800, fontSize: "1.125rem", letterSpacing: "-0.03em" }}>
                JobFlow
              </span>
            </div>
            <div
              className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full"
              style={{ background: "rgba(16,185,129,0.07)", border: "1px solid rgba(16,185,129,0.18)" }}
            >
              <span className="w-1.5 h-1.5 rounded-full glow-pulse" style={{ background: "#10b981" }} />
              <span style={{ color: "#6ee7b7", fontSize: "0.6875rem", fontWeight: 700, letterSpacing: "0.07em", textTransform: "uppercase" }}>
                AI Powered
              </span>
            </div>
          </div>
        </nav>

        {/* Hero */}
        <section className="max-w-5xl mx-auto px-5 pt-16 pb-12 text-center">
          <div
            className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full mb-6"
            style={{ background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)" }}
          >
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none">
              <path d="M13 10V3L4 14h7v7l9-11h-7z" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span style={{ color: "#6ee7b7", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.05em", textTransform: "uppercase" }}>
              Smart Job Search
            </span>
          </div>

          <h1
            className="mb-4 leading-tight"
            style={{ color: "#ecfdf5", fontWeight: 900, fontSize: "clamp(2rem, 5vw, 3.25rem)", letterSpacing: "-0.04em" }}
          >
            Land your next job,{" "}
            <span style={{ color: "#10b981" }}>faster.</span>
          </h1>
          <p
            className="max-w-xl mx-auto"
            style={{ color: "#6ee7b7", fontWeight: 500, fontSize: "1.0625rem", lineHeight: 1.65 }}
          >
            Upload your resume once. Search LinkedIn jobs by role and location.
            Get AI fit scores and apply directly — all in one place.
          </p>
        </section>

        {/* Main panels */}
        <main className="max-w-5xl mx-auto px-5 pb-20">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-8">
            <ResumeSection />
            <JobSearchWithResults onJobsFound={setJobs} />
          </div>

          {/* Results */}
          {jobs.length > 0 && (
            <section className="animate-fade-in">
              <div className="flex items-center gap-3 mb-5">
                <div className="h-px flex-1" style={{ background: "linear-gradient(to right, rgba(16,185,129,0.3), transparent)" }} />
                <span style={{ color: "#6ee7b7", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.07em", textTransform: "uppercase" }}>
                  {jobs.length} Results
                </span>
                <div className="h-px flex-1" style={{ background: "linear-gradient(to left, rgba(16,185,129,0.3), transparent)" }} />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {jobs.map((job, i) => (
                  <JobCard key={job.id} job={job} index={i} />
                ))}
              </div>
            </section>
          )}
        </main>

        {/* Footer */}
        <footer className="text-center pb-8 pt-4" style={{ borderTop: "1px solid rgba(16,185,129,0.08)" }}>
          <p style={{ color: "#2d5c47", fontSize: "0.75rem", fontWeight: 500 }}>
            JobFlow · Powered by LinkedIn scraping &amp; Groq AI
          </p>
        </footer>
      </div>
    </div>
  );
}
