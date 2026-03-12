import React, { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { IconCopy, IconCheck } from "../shared/Icons";

// Custom terminal-dark theme
const terminalTheme = {
  'code[class*="language-"]': {
    color: "#cdd9e5",
    fontFamily: "var(--font-mono)",
    fontSize: "12.5px",
    lineHeight: "1.65",
    background: "none",
  },
  'pre[class*="language-"]': {
    background: "#090912",
    margin: 0,
    padding: 0,
    overflow: "auto",
  },
  comment:    { color: "#636e7b", fontStyle: "italic" },
  prolog:     { color: "#636e7b" },
  doctype:    { color: "#636e7b" },
  cdata:      { color: "#636e7b" },
  punctuation:{ color: "#8094a8" },
  property:   { color: "#79c0ff" },
  keyword:    { color: "#ff7b72" },
  tag:        { color: "#7ee787" },
  "class-name":{ color: "#ffa657" },
  boolean:    { color: "#79c0ff" },
  number:     { color: "#79c0ff" },
  function:   { color: "#d2a8ff" },
  string:     { color: "#a5d6ff" },
  char:       { color: "#a5d6ff" },
  regex:      { color: "#7ee787" },
  operator:   { color: "#cdd9e5" },
  variable:   { color: "#cdd9e5" },
  parameter:  { color: "#cdd9e5" },
  "attr-name":{ color: "#ffa657" },
  "attr-value":{ color: "#a5d6ff" },
  builtin:    { color: "#ffa657" },
  selector:   { color: "#7ee787" },
  important:  { color: "#ff7b72", fontWeight: "bold" },
  bold:       { fontWeight: "bold" },
  italic:     { fontStyle: "italic" },
};

export default function CodeBlock({ code, language = "text" }) {
  const [copied, setCopied] = useState(false);
  const lineCount = code.split("\n").length;

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      style={{
        borderRadius: "4px",
        overflow: "hidden",
        border: "1px solid var(--border-soft)",
        margin: "8px 0",
        background: "#090912",
      }}
    >
      {/* Header bar */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "7px 12px",
          background: "var(--bg-overlay)",
          borderBottom: "1px solid var(--border-soft)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          {/* Traffic light dots */}
          <div style={{ display: "flex", gap: "5px" }}>
            {["#ff5f57", "#febc2e", "#28c840"].map((c, i) => (
              <span
                key={i}
                style={{ width: "9px", height: "9px", borderRadius: "50%", background: c, opacity: 0.6 }}
              />
            ))}
          </div>
          <span
            style={{
              fontSize: "10px",
              fontFamily: "var(--font-mono)",
              color: "var(--text-muted)",
              letterSpacing: "0.08em",
              textTransform: "uppercase",
            }}
          >
            {language}
          </span>
          <span
            style={{
              fontSize: "10px",
              fontFamily: "var(--font-mono)",
              color: "var(--text-ghost)",
            }}
          >
            {lineCount} line{lineCount !== 1 ? "s" : ""}
          </span>
        </div>

        <button
          onClick={handleCopy}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "4px",
            background: "transparent",
            border: "none",
            color: copied ? "var(--green)" : "var(--text-muted)",
            fontSize: "11px",
            fontFamily: "var(--font-mono)",
            cursor: "pointer",
            padding: "2px 6px",
            borderRadius: "3px",
            transition: "color 0.15s",
          }}
          onMouseEnter={(e) => { if (!copied) e.currentTarget.style.color = "var(--text-primary)"; }}
          onMouseLeave={(e) => { if (!copied) e.currentTarget.style.color = "var(--text-muted)"; }}
        >
          {copied ? <IconCheck /> : <IconCopy />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>

      {/* Code */}
      <div style={{ overflowX: "auto" }}>
        <SyntaxHighlighter
          language={language}
          style={terminalTheme}
          customStyle={{
            margin: 0,
            padding: "14px 16px",
            background: "transparent",
          }}
          showLineNumbers={lineCount > 4}
          lineNumberStyle={{
            color: "var(--text-ghost)",
            minWidth: "3em",
            paddingRight: "16px",
            textAlign: "right",
            userSelect: "none",
            fontSize: "11px",
          }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
