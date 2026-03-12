import React from "react";
import { useChatStore } from "../../store/chatStore";
import { IconMessage, IconUpload, IconClock, IconPlus, IconCode } from "../shared/Icons";

const NAV = [
  { id: "chat",    icon: IconMessage, label: "Chat" },
  { id: "upload",  icon: IconUpload,  label: "Upload" },
  { id: "history", icon: IconClock,   label: "History" },
];

export default function Sidebar() {
  const { activePanel, setActivePanel, clearChat, project, messages, sidebarOpen } = useChatStore();
  const msgCount = messages.filter((m) => m.role === "user").length;

  if (!sidebarOpen) return null;

  return (
    <aside
      className="anim-slide-left"
      style={{
        width: "var(--sidebar-w)",
        minWidth: "var(--sidebar-w)",
        background: "var(--bg-panel)",
        borderRight: "1px solid var(--border-soft)",
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        overflow: "hidden",
        position: "relative",
        zIndex: 10,
      }}
    >
      {/* ── Logo ─────────────────────────────────────────── */}
      <div
        style={{
          padding: "18px 16px 14px",
          borderBottom: "1px solid var(--border-soft)",
          display: "flex",
          alignItems: "center",
          gap: "10px",
        }}
      >
        <div
          className="anim-glow"
          style={{
            width: "30px",
            height: "30px",
            background: "var(--cyan)",
            borderRadius: "6px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
          }}
        >
          <IconCode size={16} style={{ color: "var(--bg-void)" }} />
          <span style={{ color: "var(--bg-void)", fontWeight: 700, fontSize: "13px", fontFamily: "var(--font-display)", letterSpacing: "0" }}>
            CM
          </span>
        </div>
        <div>
          <div
            className="font-display"
            style={{ fontSize: "18px", color: "var(--text-bright)", letterSpacing: "0.08em", lineHeight: 1 }}
          >
            CODEMIND
          </div>
          <div
            style={{
              fontSize: "10px",
              color: "var(--text-muted)",
              fontFamily: "var(--font-mono)",
              letterSpacing: "0.12em",
              marginTop: "2px",
            }}
          >
            AI INTELLIGENCE v1.0
          </div>
        </div>
      </div>

      {/* ── New Chat ──────────────────────────────────────── */}
      <div style={{ padding: "12px" }}>
        <button
          className="btn"
          onClick={clearChat}
          style={{
            width: "100%",
            justifyContent: "center",
            borderStyle: "dashed",
            color: "var(--text-soft)",
          }}
        >
          <IconPlus size={13} />
          New Session
        </button>
      </div>

      {/* ── Navigation ───────────────────────────────────── */}
      <nav style={{ flex: 1, padding: "4px 8px", overflow: "hidden" }}>
        <div
          style={{
            fontSize: "10px",
            color: "var(--text-muted)",
            fontFamily: "var(--font-mono)",
            letterSpacing: "0.12em",
            padding: "6px 8px 8px",
            textTransform: "uppercase",
          }}
        >
          Navigation
        </div>
        {NAV.map((item) => {
          const active = activePanel === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActivePanel(item.id)}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: "10px",
                padding: "9px 10px",
                borderRadius: "4px",
                border: "none",
                background: active ? "var(--bg-overlay)" : "transparent",
                color: active ? "var(--cyan)" : "var(--text-soft)",
                fontFamily: "var(--font-ui)",
                fontSize: "13px",
                fontWeight: active ? 600 : 400,
                cursor: "pointer",
                marginBottom: "2px",
                transition: "all 0.15s",
                textAlign: "left",
                borderLeft: active ? "2px solid var(--cyan)" : "2px solid transparent",
                paddingLeft: active ? "8px" : "10px",
              }}
              onMouseEnter={(e) => { if (!active) e.currentTarget.style.background = "var(--bg-surface)"; }}
              onMouseLeave={(e) => { if (!active) e.currentTarget.style.background = "transparent"; }}
            >
              <item.icon size={14} />
              {item.label}
              {item.id === "chat" && msgCount > 0 && (
                <span
                  style={{
                    marginLeft: "auto",
                    fontSize: "10px",
                    fontFamily: "var(--font-mono)",
                    color: active ? "var(--cyan)" : "var(--text-muted)",
                    background: "var(--bg-raised)",
                    padding: "1px 7px",
                    borderRadius: "10px",
                  }}
                >
                  {msgCount}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* ── Project Status ────────────────────────────────── */}
      <div style={{ padding: "10px 12px", borderTop: "1px solid var(--border-soft)" }}>
        <div
          style={{
            fontSize: "10px",
            color: "var(--text-muted)",
            fontFamily: "var(--font-mono)",
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            marginBottom: "8px",
          }}
        >
          Project Context
        </div>
        {project ? (
          <div
            style={{
              padding: "8px 10px",
              background: "var(--green-ghost)",
              border: "1px solid rgba(0,230,118,0.2)",
              borderRadius: "4px",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "3px" }}>
              <span style={{ fontSize: "10px", color: "var(--green)" }}>◉</span>
              <span style={{ fontSize: "12px", color: "var(--green)", fontWeight: 600 }}>
                Loaded
              </span>
            </div>
            <div
              style={{
                fontSize: "10px",
                color: "var(--text-muted)",
                fontFamily: "var(--font-mono)",
                wordBreak: "break-all",
              }}
            >
              {project.files_path?.split("/").pop() || "project"}
            </div>
          </div>
        ) : (
          <div
            style={{
              padding: "8px 10px",
              background: "var(--bg-surface)",
              border: "1px dashed var(--border-mid)",
              borderRadius: "4px",
              fontSize: "11px",
              color: "var(--text-muted)",
              textAlign: "center",
              cursor: "pointer",
            }}
            onClick={() => setActivePanel("upload")}
          >
            No project loaded
            <div style={{ fontSize: "10px", color: "var(--text-ghost)", marginTop: "2px" }}>
              Click Upload to add one
            </div>
          </div>
        )}
      </div>

      {/* ── Status Bar ───────────────────────────────────── */}
      <div
        style={{
          padding: "8px 12px",
          borderTop: "1px solid var(--border-soft)",
          display: "flex",
          alignItems: "center",
          gap: "6px",
        }}
      >
        <span
          style={{
            width: "6px",
            height: "6px",
            borderRadius: "50%",
            background: "var(--green)",
            boxShadow: "0 0 6px var(--green)",
            display: "inline-block",
          }}
        />
        <span style={{ fontSize: "11px", color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
          gpt-4o-mini · ready
        </span>
      </div>
    </aside>
  );
}
