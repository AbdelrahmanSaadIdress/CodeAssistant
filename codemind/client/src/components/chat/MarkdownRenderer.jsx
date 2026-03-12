import React from "react";
import CodeBlock from "./CodeBlock";

export default function MarkdownRenderer({ content }) {
  if (!content) return null;

  // Split on fenced code blocks
  const segments = content.split(/(```[\w]*\n[\s\S]*?```)/g);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
      {segments.map((seg, i) => {
        const fenced = seg.match(/^```([\w]*)\n([\s\S]*?)```$/);
        if (fenced) {
          return <CodeBlock key={i} language={fenced[1] || "text"} code={fenced[2].trimEnd()} />;
        }
        return <TextSection key={i} text={seg} />;
      })}
    </div>
  );
}

function TextSection({ text }) {
  if (!text.trim()) return null;

  const lines = text.split("\n");
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // H2 heading (##)
    if (line.startsWith("## ")) {
      elements.push(
        <div
          key={i}
          style={{
            fontFamily: "var(--font-display)",
            fontSize: "16px",
            color: "var(--text-bright)",
            letterSpacing: "0.06em",
            marginTop: "6px",
            marginBottom: "2px",
          }}
        >
          {line.slice(3).toUpperCase()}
        </div>
      );
      i++;
      continue;
    }

    // H3 heading (###)
    if (line.startsWith("### ")) {
      elements.push(
        <div
          key={i}
          style={{
            fontSize: "13px",
            fontWeight: 600,
            color: "var(--cyan)",
            fontFamily: "var(--font-mono)",
            marginTop: "4px",
          }}
        >
          {line.slice(4)}
        </div>
      );
      i++;
      continue;
    }

    // Bullet list item
    if (line.trim().startsWith("- ") || line.trim().startsWith("* ")) {
      const bulletContent = line.replace(/^\s*[-*]\s/, "");
      elements.push(
        <div
          key={i}
          style={{
            display: "flex",
            gap: "8px",
            alignItems: "baseline",
            paddingLeft: "4px",
          }}
        >
          <span style={{ color: "var(--cyan)", fontSize: "10px", flexShrink: 0, marginTop: "3px" }}>▸</span>
          <span style={{ fontSize: "13px", lineHeight: 1.65 }}>{parseInline(bulletContent)}</span>
        </div>
      );
      i++;
      continue;
    }

    // Empty line
    if (!line.trim()) {
      elements.push(<div key={i} style={{ height: "6px" }} />);
      i++;
      continue;
    }

    // Regular paragraph
    elements.push(
      <p key={i} style={{ fontSize: "13px", lineHeight: 1.7, color: "var(--text-primary)" }}>
        {parseInline(line)}
      </p>
    );
    i++;
  }

  return <div>{elements}</div>;
}

// ─── Inline: **bold** and `code` ─────────────────────────
function parseInline(text) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
  return parts.map((part, idx) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return (
        <strong key={idx} style={{ color: "var(--text-bright)", fontWeight: 600 }}>
          {part.slice(2, -2)}
        </strong>
      );
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={idx}
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "11.5px",
            color: "var(--cyan)",
            background: "var(--cyan-ghost)",
            border: "1px solid rgba(0,229,255,0.12)",
            borderRadius: "3px",
            padding: "1px 6px",
          }}
        >
          {part.slice(1, -1)}
        </code>
      );
    }
    return part;
  });
}
