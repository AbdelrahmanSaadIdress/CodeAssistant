import React from "react";
import { INTENT_META } from "../../store/chatStore";
import MarkdownRenderer from "./MarkdownRenderer";
import { IconZap, IconShield } from "../shared/Icons";

export default function Message({ message }) {
  const isUser = message.role === "user";
  const isError = message.role === "error";
  const intent = message.intent ? INTENT_META[message.intent] : null;

  const timeStr = new Date(message.timestamp).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div
      className="anim-fade-up"
      style={{
        display: "flex",
        flexDirection: isUser ? "row-reverse" : "row",
        gap: "10px",
        padding: "6px 0",
        alignItems: "flex-start",
      }}
    >
      {/* Avatar */}
      <div
        style={{
          width: "28px",
          height: "28px",
          minWidth: "28px",
          borderRadius: "4px",
          background: isUser
            ? "var(--bg-overlay)"
            : isError
            ? "var(--red-ghost)"
            : "var(--cyan)",
          border: isUser
            ? "1px solid var(--border-mid)"
            : isError
            ? "1px solid rgba(255,61,113,0.3)"
            : "none",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexShrink: 0,
          marginTop: "2px",
          fontFamily: "var(--font-display)",
          fontSize: "11px",
          letterSpacing: "0.04em",
          color: isUser ? "var(--text-soft)" : isError ? "var(--red)" : "var(--bg-void)",
          fontWeight: 700,
        }}
      >
        {isUser ? "YOU" : isError ? "!" : "CM"}
      </div>

      {/* Content column */}
      <div style={{ maxWidth: "80%", minWidth: 0 }}>
        {/* Message header */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            marginBottom: "5px",
            flexWrap: "wrap",
          }}
        >
          <span
            style={{
              fontSize: "11px",
              fontWeight: 600,
              color: isUser ? "var(--text-soft)" : isError ? "var(--red)" : "var(--text-bright)",
              fontFamily: "var(--font-mono)",
              letterSpacing: "0.04em",
              textTransform: "uppercase",
            }}
          >
            {isUser ? "user" : isError ? "error" : "codemind"}
          </span>

          {intent && (
            <span
              className="chip"
              style={{
                color: intent.color,
                background: intent.bg,
                border: `1px solid ${intent.color}22`,
              }}
            >
              {intent.icon} {intent.label}
            </span>
          )}

          <span
            style={{
              fontSize: "10px",
              color: "var(--text-ghost)",
              fontFamily: "var(--font-mono)",
              marginLeft: "auto",
            }}
          >
            {timeStr}
          </span>
        </div>

        {/* Bubble */}
        <div
          style={{
            padding: "12px 14px",
            background: isUser
              ? "var(--bg-raised)"
              : isError
              ? "var(--red-ghost)"
              : "var(--bg-surface)",
            border: `1px solid ${
              isUser
                ? "var(--border-mid)"
                : isError
                ? "rgba(255,61,113,0.2)"
                : "var(--border-soft)"
            }`,
            borderRadius: isUser ? "6px 2px 6px 6px" : "2px 6px 6px 6px",
          }}
        >
          {isUser ? (
            <p
              style={{
                fontSize: "13px",
                lineHeight: 1.7,
                color: "var(--text-primary)",
                whiteSpace: "pre-wrap",
                fontFamily: "var(--font-mono)",
              }}
            >
              {message.content}
            </p>
          ) : (
            <MarkdownRenderer content={message.content} />
          )}
        </div>
      </div>
    </div>
  );
}
