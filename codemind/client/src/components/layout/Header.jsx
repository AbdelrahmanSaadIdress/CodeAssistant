import React from "react";
import { useChatStore, INTENT_META } from "../../store/chatStore";
import { IconMenu, IconTrash, IconCode } from "../shared/Icons";

export default function Header() {
  const { activePanel, toggleSidebar, clearChat, project, messages } = useChatStore();
  const msgCount = messages.filter((m) => m.role === "user").length;

  const PANEL_LABELS = {
    chat:    { title: "Chat Interface", sub: "AI code conversation" },
    upload:  { title: "Project Upload",  sub: "Upload .rar archive" },
    history: { title: "Session History", sub: `${msgCount} prompt${msgCount !== 1 ? "s" : ""}` },
  };

  const { title, sub } = PANEL_LABELS[activePanel] || PANEL_LABELS.chat;

  return (
    <header
      style={{
        height: "var(--header-h)",
        borderBottom: "1px solid var(--border-soft)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 20px",
        background: "rgba(9,9,16,0.9)",
        backdropFilter: "blur(10px)",
        flexShrink: 0,
        gap: "12px",
      }}
    >
      {/* Left */}
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <button
          className="btn-ghost btn"
          onClick={toggleSidebar}
          style={{ padding: "6px", borderRadius: "4px" }}
          title="Toggle sidebar"
        >
          <IconMenu size={15} />
        </button>

        <div
          style={{
            width: "1px",
            height: "20px",
            background: "var(--border-soft)",
          }}
        />

        <div>
          <div
            className="font-display"
            style={{ fontSize: "15px", color: "var(--text-bright)", letterSpacing: "0.06em", lineHeight: 1 }}
          >
            {title.toUpperCase()}
          </div>
          <div style={{ fontSize: "10px", color: "var(--text-muted)", fontFamily: "var(--font-mono)", marginTop: "2px" }}>
            {sub}
          </div>
        </div>
      </div>

      {/* Right */}
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        {project && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "5px",
              padding: "3px 10px",
              background: "var(--green-ghost)",
              border: "1px solid rgba(0,230,118,0.2)",
              borderRadius: "3px",
              fontSize: "11px",
              color: "var(--green)",
              fontFamily: "var(--font-mono)",
            }}
          >
            <span>◉</span>
            Project loaded
          </div>
        )}

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "5px",
            padding: "3px 10px",
            background: "var(--bg-raised)",
            border: "1px solid var(--border-mid)",
            borderRadius: "3px",
            fontSize: "11px",
            color: "var(--text-muted)",
            fontFamily: "var(--font-mono)",
          }}
        >
          <IconCode size={11} />
          gpt-4o-mini
        </div>

        {activePanel === "chat" && msgCount > 0 && (
          <button
            className="btn-ghost btn"
            onClick={clearChat}
            style={{ padding: "6px 10px", fontSize: "12px", gap: "5px" }}
            title="Clear chat"
          >
            <IconTrash size={13} />
          </button>
        )}
      </div>
    </header>
  );
}
