"use client";

import { useState } from "react";
import Navbar from "../components/Navbar";
import ResumeSection from "../components/ResumeSection";
import JobSearchWithResults from "../components/JobSearchWithResults";
import JobCard from "../components/JobCard";
import type { Job } from "../types";

export default function DashboardPage() {
  const [jobs, setJobs] = useState<Job[]>([]);

  return (
    <div style={{ minHeight: "100vh", background: "#060d1a", position: "relative" }}>
      {/* Ambient blobs */}
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
        <Navbar />

        {/* Page header */}
        <div className="max-w-6xl mx-auto px-6 pt-10 pb-6">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1
                style={{ color: "#ecfdf5", fontWeight: 900, fontSize: "clamp(1.5rem, 3vw, 2rem)", letterSpacing: "-0.03em", marginBottom: "0.25rem" }}
              >
                Dashboard
              </h1>
              <p style={{ color: "#6ee7b7", fontSize: "0.9375rem", fontWeight: 500 }}>
                Upload your resume, then search and score LinkedIn jobs.
              </p>
            </div>
            <div
              className="flex items-center gap-2 px-3 py-1.5 rounded-full"
              style={{ background: "rgba(16,185,129,0.07)", border: "1px solid rgba(16,185,129,0.18)" }}
            >
              <span className="w-1.5 h-1.5 rounded-full glow-pulse" style={{ background: "#10b981" }} />
              <span style={{ color: "#6ee7b7", fontSize: "0.6875rem", fontWeight: 700, letterSpacing: "0.07em", textTransform: "uppercase" }}>
                AI Powered
              </span>
            </div>
          </div>
        </div>

        {/* Workflow hint */}
        <div className="max-w-6xl mx-auto px-6 mb-6">
          <div
            className="flex items-center gap-4 flex-wrap px-5 py-3.5 rounded-2xl"
            style={{ background: "rgba(16,185,129,0.04)", border: "1px solid rgba(16,185,129,0.1)" }}
          >
            {[
              { num: "1", label: "Upload Resume" },
              { num: "2", label: "Search Jobs" },
              { num: "3", label: "Review & Apply" },
            ].map((step, i) => (
              <div key={step.num} className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <span
                    className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0"
                    style={{ background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)", color: "#10b981", fontSize: "0.6875rem", fontWeight: 800 }}
                  >
                    {step.num}
                  </span>
                  <span style={{ color: "#6ee7b7", fontSize: "0.8125rem", fontWeight: 600 }}>
                    {step.label}
                  </span>
                </div>
                {i < 2 && (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" className="flex-shrink-0">
                    <path d="M9 18l6-6-6-6" stroke="#2d5c47" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Main panels */}
        <main className="max-w-6xl mx-auto px-6 pb-20">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-8">
            {/* Resume panel */}
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span
                  className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0"
                  style={{ background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)", color: "#10b981", fontSize: "0.6875rem", fontWeight: 800 }}
                >
                  1
                </span>
                <span style={{ color: "#ecfdf5", fontSize: "0.875rem", fontWeight: 700, letterSpacing: "-0.01em" }}>
                  Resume Upload
                </span>
              </div>
              <ResumeSection />
            </div>

            {/* Job search panel */}
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span
                  className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0"
                  style={{ background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)", color: "#10b981", fontSize: "0.6875rem", fontWeight: 800 }}
                >
                  2
                </span>
                <span style={{ color: "#ecfdf5", fontSize: "0.875rem", fontWeight: 700, letterSpacing: "-0.01em" }}>
                  LinkedIn Job Search
                </span>
              </div>
              <JobSearchWithResults onJobsFound={setJobs} />
            </div>
          </div>

          {/* Results */}
          {jobs.length > 0 && (
            <section className="animate-fade-in">
              <div className="flex items-center gap-4 mb-6">
                <div className="flex items-center gap-2 mb-0">
                  <span
                    className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0"
                    style={{ background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)", color: "#10b981", fontSize: "0.6875rem", fontWeight: 800 }}
                  >
                    3
                  </span>
                  <span style={{ color: "#ecfdf5", fontSize: "0.875rem", fontWeight: 700, letterSpacing: "-0.01em" }}>
                    Results
                  </span>
                </div>
                <div className="h-px flex-1" style={{ background: "linear-gradient(to right, rgba(16,185,129,0.25), transparent)" }} />
                <span
                  className="px-3 py-1 rounded-full"
                  style={{ background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.25)", color: "#6ee7b7", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.05em", textTransform: "uppercase" }}
                >
                  {jobs.length} matched
                </span>
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
