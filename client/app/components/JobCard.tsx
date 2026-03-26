"use client";

import { useState } from "react";
import type { Job } from "../types";

interface JobCardProps {
  job: Job;
  index: number;
}

function ScoreBadge({ score }: { score: number | null }) {
  if (score === null) return null;

  const color =
    score >= 8 ? "#10b981"
    : score >= 6 ? "#f59e0b"
    : "#ef4444";

  const trackColor =
    score >= 8 ? "rgba(16,185,129,0.12)"
    : score >= 6 ? "rgba(245,158,11,0.12)"
    : "rgba(239,68,68,0.12)";

  const fillGradient =
    score >= 8 ? "linear-gradient(90deg, #059669, #34d399)"
    : score >= 6 ? "linear-gradient(90deg, #d97706, #fbbf24)"
    : "linear-gradient(90deg, #dc2626, #f87171)";

  const label =
    score >= 9 ? "Excellent fit"
    : score >= 7 ? "Strong fit"
    : score >= 5 ? "Good fit"
    : score >= 3 ? "Partial fit"
    : "Low fit";

  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-baseline justify-between">
        <span style={{ color: "#2d5c47", fontSize: "0.6875rem", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em" }}>
          Match Score
        </span>
        <span style={{ color, fontSize: "1.25rem", fontWeight: 800, lineHeight: 1 }}>
          {score}/10
        </span>
      </div>
      <div className="h-1.5 rounded-full overflow-hidden" style={{ background: trackColor }}>
        <div
          className="h-full rounded-full score-bar"
          style={{ width: `${(score / 10) * 100}%`, background: fillGradient }}
        />
      </div>
      <span style={{ color, fontSize: "0.7rem", fontWeight: 600 }}>{label}</span>
    </div>
  );
}

export default function JobCard({ job, index }: JobCardProps) {
  const [expanded, setExpanded] = useState(false);

  const delay = `${index * 60}ms`;

  return (
    <div
      className="rounded-2xl overflow-hidden transition-all duration-300 animate-slide-up"
      style={{
        background: "linear-gradient(135deg, rgba(6,18,32,0.9) 0%, rgba(10,22,40,0.9) 100%)",
        border: "1px solid rgba(16,185,129,0.15)",
        boxShadow: "0 2px 16px rgba(0,0,0,0.3)",
        animationDelay: delay,
        opacity: 0,
      }}
    >
      <div className="p-5">
        <div className="flex items-start justify-between gap-4">
          {/* Job Info */}
          <div className="flex-1 min-w-0">
            <h3
              className="font-bold leading-snug mb-1 truncate"
              style={{ color: "#ecfdf5", fontSize: "0.9375rem", letterSpacing: "-0.01em" }}
            >
              {job.title}
            </h3>
            <div className="flex items-center gap-2 flex-wrap">
              <span
                className="px-2.5 py-0.5 rounded-full"
                style={{
                  background: "rgba(16,185,129,0.1)",
                  border: "1px solid rgba(16,185,129,0.2)",
                  color: "#6ee7b7",
                  fontSize: "0.75rem",
                  fontWeight: 600,
                }}
              >
                {job.company}
              </span>
              <span style={{ color: "#2d5c47", fontSize: "0.75rem", fontWeight: 500 }}>
                {new Date(job.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
              </span>
            </div>
          </div>

          {/* Score */}
          {job.score !== null && (
            <div className="flex-shrink-0 w-28">
              <ScoreBadge score={job.score} />
            </div>
          )}
        </div>

        {/* Fit Reasoning */}
        {job.fit_reasoning && (
          <div
            className="mt-3 rounded-xl px-3.5 py-2.5"
            style={{ background: "rgba(16,185,129,0.05)", border: "1px solid rgba(16,185,129,0.1)" }}
          >
            <p style={{ color: "#6ee7b7", fontSize: "0.78125rem", fontWeight: 500, lineHeight: 1.55 }}>
              {job.fit_reasoning.length > 160 && !expanded
                ? job.fit_reasoning.slice(0, 160) + "…"
                : job.fit_reasoning}
              {job.fit_reasoning.length > 160 && (
                <button
                  onClick={() => setExpanded(!expanded)}
                  className="ml-1.5"
                  style={{ color: "#10b981", fontWeight: 600, background: "none", border: "none", cursor: "pointer", fontSize: "inherit" }}
                >
                  {expanded ? "less" : "more"}
                </button>
              )}
            </p>
          </div>
        )}

        <div className="mt-4 flex items-center gap-3">
          {job.url ? (
            <a
              href={job.url}
              onClick={() => localStorage.setItem("job_id", job.id.toString())}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl font-bold transition-all duration-200"
              style={{
                background: "linear-gradient(135deg, #059669, #10b981)",
                color: "#ecfdf5",
                fontSize: "0.875rem",
                fontFamily: "inherit",
                letterSpacing: "-0.01em",
                textDecoration: "none",
                boxShadow: "0 3px 14px rgba(16,185,129,0.28)",
              }}
              onMouseEnter={e => {
                (e.currentTarget as HTMLAnchorElement).style.background = "linear-gradient(135deg, #047857, #059669)";
                (e.currentTarget as HTMLAnchorElement).style.boxShadow = "0 5px 20px rgba(16,185,129,0.42)";
                (e.currentTarget as HTMLAnchorElement).style.transform = "translateY(-1px)";
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLAnchorElement).style.background = "linear-gradient(135deg, #059669, #10b981)";
                (e.currentTarget as HTMLAnchorElement).style.boxShadow = "0 3px 14px rgba(16,185,129,0.28)";
                (e.currentTarget as HTMLAnchorElement).style.transform = "translateY(0)";
              }}
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <path d="M15 3h6v6M10 14L21 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Apply on LinkedIn
            </a>
          ) : (
            <div
              className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl"
              style={{
                background: "rgba(16,185,129,0.06)",
                border: "1px solid rgba(16,185,129,0.15)",
                color: "#2d5c47",
                fontSize: "0.875rem",
                fontWeight: 600,
              }}
            >
              No link available
            </div>
          )}

          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center justify-center w-10 h-10 rounded-xl transition-all duration-200"
            style={{
              background: "rgba(16,185,129,0.07)",
              border: "1px solid rgba(16,185,129,0.18)",
              color: "#6ee7b7",
              cursor: "pointer",
            }}
            onMouseEnter={e => (e.currentTarget.style.background = "rgba(16,185,129,0.14)")}
            onMouseLeave={e => (e.currentTarget.style.background = "rgba(16,185,129,0.07)")}
            title={expanded ? "Collapse" : "Expand description"}
          >
            <svg
              width="13" height="13" viewBox="0 0 24 24" fill="none"
              style={{ transition: "transform 0.2s", transform: expanded ? "rotate(180deg)" : "rotate(0deg)" }}
            >
              <path d="M6 9l6 6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>

        {/* Full Description */}
        {expanded && job.description && (
          <div
            className="mt-3 rounded-xl p-3.5 animate-slide-up"
            style={{ background: "rgba(6,13,26,0.7)", border: "1px solid rgba(16,185,129,0.1)" }}
          >
            <p
              style={{
                color: "#a7f3d0",
                fontSize: "0.78125rem",
                fontWeight: 400,
                lineHeight: 1.7,
                whiteSpace: "pre-line",
                maxHeight: "240px",
                overflowY: "auto",
              }}
            >
              {job.description.slice(0, 1200)}{job.description.length > 1200 ? "…" : ""}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
