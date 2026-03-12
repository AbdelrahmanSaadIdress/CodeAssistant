import React, { useEffect, useState } from "react";

const THINKING_PHRASES = [
  "Analyzing intent...",
  "Processing code context...",
  "Generating response...",
  "Running pipeline...",
  "Thinking...",
];

export default function TypingIndicator() {
  const [phraseIdx, setPhraseIdx] = useState(0);

  useEffect(() => {
    const t = setInterval(() => {
      setPhraseIdx((p) => (p + 1) % THINKING_PHRASES.length);
    }, 1800);
    return () => clearInterval(t);
  }, []);

  return (
    <div
      className="anim-fade-in"
      style={{ display: "flex", gap: "10px", padding: "6px 0", alignItems: "flex-start" }}
    >
      {/* Avatar */}
      <div
        style={{
          width: "28px",
          height: "28px",
          minWidth: "28px",
          borderRadius: "4px",
          background: "var(--cyan)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "var(--font-display)",
          fontSize: "11px",
          letterSpacing: "0.04em",
          color: "var(--bg-void)",
          fontWeight: 700,
          marginTop: "2px",
        }}
      >
        CM
      </div>

      <div>
        <div
          style={{
            fontSize: "11px",
            fontWeight: 600,
            color: "var(--text-bright)",
            fontFamily: "var(--font-mono)",
            letterSpacing: "0.04em",
            textTransform: "uppercase",
            marginBottom: "5px",
          }}
        >
          codemind
        </div>

        <div
          style={{
            padding: "10px 14px",
            background: "var(--bg-surface)",
            border: "1px solid var(--border-soft)",
            borderRadius: "2px 6px 6px 6px",
            display: "flex",
            alignItems: "center",
            gap: "12px",
          }}
        >
          {/* Animated dots */}
          <div style={{ display: "flex", gap: "4px", alignItems: "center" }}>
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                style={{
                  width: "5px",
                  height: "5px",
                  borderRadius: "50%",
                  background: "var(--cyan)",
                  animation: `pulseDot 1.2s ease infinite`,
                  animationDelay: `${i * 0.18}s`,
                }}
              />
            ))}
          </div>

          {/* Cycling phrase */}
          <span
            key={phraseIdx}
            className="anim-fade-in"
            style={{
              fontSize: "12px",
              color: "var(--text-soft)",
              fontFamily: "var(--font-mono)",
            }}
          >
            {THINKING_PHRASES[phraseIdx]}
          </span>
        </div>
      </div>
    </div>
  );
}
