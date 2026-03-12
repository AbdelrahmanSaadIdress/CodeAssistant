import React, { useState, useRef, useEffect } from "react";
import { IconSend, IconSpinner } from "../shared/Icons";

const QUICK_ACTIONS = [
  { label: "⚡ Generate",  prefix: "Generate a Python function to "  },
  { label: "🔍 Explain",   prefix: "Explain this code:\n\n"          },
  { label: "🐛 Debug",     prefix: "Find and fix bugs in:\n\n"       },
  { label: "→ Complete",   prefix: "// Complete this snippet:\n\n"   },
  { label: "🔐 Audit",     prefix: "Audit this code for security:\n\n" },
  { label: "✨ Refactor",  prefix: "Refactor and improve:\n\n"       },
];

export default function ChatInput({ onSend, isLoading }) {
  const [value, setValue] = useState("");
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 260) + "px";
  }, [value]);

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed || isLoading) return;
    onSend(trimmed);
    setValue("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const applyQuickAction = (prefix) => {
    setValue(prefix);
    textareaRef.current?.focus();
  };

  const canSubmit = value.trim() && !isLoading;

  return (
    <div
      style={{
        borderTop: "1px solid var(--border-soft)",
        padding: "12px 20px 16px",
        background: "var(--bg-panel)",
        flexShrink: 0,
      }}
    >
      {/* Quick Action Pills */}
      <div
        className="stagger"
        style={{
          display: "flex",
          gap: "6px",
          marginBottom: "10px",
          flexWrap: "wrap",
        }}
      >
        {QUICK_ACTIONS.map((a) => (
          <button
            key={a.label}
            className="anim-fade-in"
            onClick={() => applyQuickAction(a.prefix)}
            disabled={isLoading}
            style={{
              padding: "3px 10px",
              background: "var(--bg-raised)",
              border: "1px solid var(--border-soft)",
              borderRadius: "3px",
              color: "var(--text-muted)",
              fontSize: "11px",
              fontFamily: "var(--font-mono)",
              cursor: "pointer",
              transition: "all 0.15s",
              whiteSpace: "nowrap",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = "var(--cyan)";
              e.currentTarget.style.color = "var(--cyan)";
              e.currentTarget.style.background = "var(--cyan-ghost)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = "var(--border-soft)";
              e.currentTarget.style.color = "var(--text-muted)";
              e.currentTarget.style.background = "var(--bg-raised)";
            }}
          >
            {a.label}
          </button>
        ))}
      </div>

      {/* Input container */}
      <div
        style={{
          background: "var(--bg-surface)",
          border: "1px solid var(--border-mid)",
          borderRadius: "5px",
          display: "flex",
          flexDirection: "column",
          transition: "border-color 0.15s, box-shadow 0.15s",
        }}
        onFocusCapture={(e) => {
          e.currentTarget.style.borderColor = "var(--cyan)";
          e.currentTarget.style.boxShadow = "0 0 0 2px var(--cyan-ghost)";
        }}
        onBlurCapture={(e) => {
          e.currentTarget.style.borderColor = "var(--border-mid)";
          e.currentTarget.style.boxShadow = "none";
        }}
      >
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          placeholder="Describe a task, paste code, or ask a question…"
          rows={2}
          style={{
            background: "transparent",
            border: "none",
            outline: "none",
            resize: "none",
            padding: "12px 14px 6px",
            color: "var(--text-primary)",
            fontFamily: "var(--font-mono)",
            fontSize: "13px",
            lineHeight: 1.65,
            minHeight: "52px",
            maxHeight: "260px",
            overflow: "auto",
          }}
        />

        {/* Footer row */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "5px 10px 10px 14px",
          }}
        >
          <span
            style={{
              fontSize: "10px",
              color: "var(--text-ghost)",
              fontFamily: "var(--font-mono)",
            }}
          >
            {value.length > 0 ? `${value.length} chars` : "Enter to send · Shift+Enter for newline"}
          </span>

          <div style={{ display: "flex", gap: "6px", alignItems: "center" }}>
            {value && !isLoading && (
              <button
                className="btn-ghost btn"
                onClick={() => setValue("")}
                style={{ padding: "4px 8px", fontSize: "11px" }}
              >
                Clear
              </button>
            )}
            <button
              className={canSubmit ? "btn-primary btn" : "btn btn"}
              onClick={handleSubmit}
              disabled={!canSubmit}
              style={{
                padding: "6px 14px",
                fontSize: "12px",
                fontFamily: "var(--font-mono)",
                letterSpacing: "0.04em",
              }}
            >
              {isLoading ? <IconSpinner size={13} /> : <IconSend size={12} />}
              {isLoading ? "THINKING" : "SEND"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
