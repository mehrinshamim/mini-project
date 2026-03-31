"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav
      className="sticky top-0 z-50"
      style={{
        background: "rgba(6,13,26,0.88)",
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(16,185,129,0.1)",
      }}
    >
      <div className="max-w-[1400px] mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" style={{ textDecoration: "none" }}>
          <div className="flex items-center gap-3 cursor-pointer">
            <div
              className="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0"
              style={{
                background: "linear-gradient(135deg, #065f46, #10b981)",
                boxShadow: "0 3px 12px rgba(16,185,129,0.35)",
              }}
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                <path
                  d="M9 12h6M9 16h6M9 8h3M5 3h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2z"
                  stroke="white"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
                <circle cx="18" cy="18" r="4" fill="#10b981" stroke="white" strokeWidth="1.5" />
                <path
                  d="M16.5 18l1.2 1.2L20 16.5"
                  stroke="white"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <span
              style={{
                color: "#ecfdf5",
                fontWeight: 800,
                fontSize: "1.125rem",
                letterSpacing: "-0.03em",
              }}
            >
              JobFlow
            </span>
          </div>
        </Link>

        {/* Nav links */}
        <div className="flex items-center gap-2">
          <Link
            href="/guide"
            style={{ textDecoration: "none" }}
          >
            <span
              className="px-4 py-2 rounded-xl transition-all duration-200 block"
              style={{
                color: pathname === "/guide" ? "#10b981" : "#6ee7b7",
                fontSize: "0.875rem",
                fontWeight: 600,
                background: pathname === "/guide" ? "rgba(16,185,129,0.1)" : "transparent",
                border: `1px solid ${pathname === "/guide" ? "rgba(16,185,129,0.25)" : "transparent"}`,
              }}
            >
              Guide
            </span>
          </Link>

          <Link href="/dashboard" style={{ textDecoration: "none" }}>
            <span
              className="px-5 py-2 rounded-xl block transition-all duration-200"
              style={{
                background:
                  pathname === "/dashboard"
                    ? "linear-gradient(135deg, #047857, #059669)"
                    : "linear-gradient(135deg, #059669, #10b981)",
                color: "#ecfdf5",
                fontSize: "0.875rem",
                fontWeight: 700,
                letterSpacing: "-0.01em",
                boxShadow: "0 3px 14px rgba(16,185,129,0.3)",
              }}
            >
              Get Started
            </span>
          </Link>
        </div>
      </div>
    </nav>
  );
}
