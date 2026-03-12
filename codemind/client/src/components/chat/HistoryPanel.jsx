import React from "react";
import { useChatStore, INTENT_META } from "../../store/chatStore";
import { IconMessage } from "../shared/Icons";

export default function HistoryPanel() {
  const { messages, setActivePanel } = useChatStore();

  const exchanges = [];
  let i = 0;
  while (i < messages.length) {
    if (messages[i].role === "user") {
      const userMsg = messages[i];
      const assistantMsg = messages[i + 1];
      exchanges.push({ user: userMsg, assistant: assistantMsg });
      i += 2;
    } else {
      i++;
    }
  }

  return (
    <div className="scroll-container" style={{ flex: 1, padding: "32px" }}>
      <div style={{ maxWidth: "720px" }}>
        {/* Header */}
        <div style={{ marginBottom: "28px" }}>
          <h2
            className="font-display"
            style={{ fontSize: "28px", letterSpacing: "0.08em", color: "var(--text-bright)", marginBottom: "6px" }}
          >
            SESSION HISTORY
          </h2>
          <p style={{ fontSize: "12px", color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
            {exchanges.length} exchange{exchanges.length !== 1 ? "s" : ""} in this session
          </p>
        </div>

        {/* Empty state */}
        {exchanges.length === 0 && (
          <div
            style={{
              textAlign: "center",
              padding: "60px 0",
              color: "var(--text-ghost)",
              fontFamily: "var(--font-mono)",
              fontSize: "13px",
            }}
          >
            <IconMessage size={32} style={{ opacity: 0.2, marginBottom: "12px" }} />
            <div>No messages yet.</div>
            <button
              className="btn btn-ghost"
              style={{ marginTop: "12px", fontSize: "12px" }}
              onClick={() => setActivePanel("chat")}
            >
              Start a conversation →
            </button>
          </div>
        )}

        {/* Exchange list */}
        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {exchanges.map(({ user, assistant }, idx) => {
            const intent = assistant?.intent ? INTENT_META[assistant.intent] : null;
            const timeStr = new Date(user.timestamp).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            });

            return (
              <div
                key={user.id}
                className="anim-fade-up"
                style={{
                  background: "var(--bg-surface)",
                  border: "1px solid var(--border-soft)",
                  borderRadius: "5px",
                  overflow: "hidden",
                  animationDelay: `${idx * 0.04}s`,
                }}
              >
                {/* Exchange header */}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    padding: "8px 14px",
                    background: "var(--bg-raised)",
                    borderBottom: "1px solid var(--border-soft)",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span
                      style={{
                        fontSize: "10px",
                        fontFamily: "var(--font-mono)",
                        color: "var(--text-ghost)",
                      }}
                    >
                      #{String(idx + 1).padStart(2, "0")}
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
                  </div>
                  <span
                    style={{
                      fontSize: "10px",
                      color: "var(--text-ghost)",
                      fontFamily: "var(--font-mono)",
                    }}
                  >
                    {timeStr}
                  </span>
                </div>

                {/* Prompt preview */}
                <div style={{ padding: "10px 14px" }}>
                  <div
                    style={{
                      fontSize: "11px",
                      color: "var(--text-muted)",
                      fontFamily: "var(--font-mono)",
                      marginBottom: "4px",
                      textTransform: "uppercase",
                      letterSpacing: "0.06em",
                    }}
                  >
                    Prompt
                  </div>
                  <p
                    style={{
                      fontSize: "13px",
                      color: "var(--text-primary)",
                      fontFamily: "var(--font-mono)",
                      lineHeight: 1.5,
                      overflow: "hidden",
                      display: "-webkit-box",
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: "vertical",
                    }}
                  >
                    {user.content}
                  </p>
                </div>

                {/* Response preview */}
                {assistant && (
                  <div
                    style={{
                      padding: "8px 14px 10px",
                      borderTop: "1px solid var(--border-dim)",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "11px",
                        color: "var(--text-muted)",
                        fontFamily: "var(--font-mono)",
                        marginBottom: "4px",
                        textTransform: "uppercase",
                        letterSpacing: "0.06em",
                      }}
                    >
                      Response
                    </div>
                    <p
                      style={{
                        fontSize: "12px",
                        color: "var(--text-soft)",
                        lineHeight: 1.5,
                        overflow: "hidden",
                        display: "-webkit-box",
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: "vertical",
                      }}
                    >
                      {assistant.content
                        .replace(/```[\s\S]*?```/g, "[code block]")
                        .replace(/\*\*/g, "")
                        .replace(/#+\s/g, "")
                        .slice(0, 160)}
                      {assistant.content.length > 160 ? "…" : ""}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
