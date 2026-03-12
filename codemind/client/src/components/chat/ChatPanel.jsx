import React, { useEffect, useRef } from "react";
import { useChat } from "../../hooks/useChat";
import Message from "./Message";
import TypingIndicator from "./TypingIndicator";
import ChatInput from "./ChatInput";

export default function ChatPanel() {
  const { messages, isLoading, sendMessage } = useChat();
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        minHeight: 0,
      }}
    >
      {/* Welcome hero shown only when just the welcome message exists */}
      {messages.length === 1 && !isLoading && <WelcomeHero />}

      {/* Messages */}
      <div
        className="scroll-container"
        style={{
          flex: 1,
          padding: "16px 24px 8px",
          display: "flex",
          flexDirection: "column",
          gap: "2px",
        }}
      >
        {messages.map((msg) => (
          <Message key={msg.id} message={msg} />
        ))}
        {isLoading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      <ChatInput onSend={sendMessage} isLoading={isLoading} />
    </div>
  );
}

// ── Welcome splash shown before first message ─────────────
function WelcomeHero() {
  return (
    <div
      className="anim-fade-up bg-grid"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "60px 40px",
        textAlign: "center",
        gap: "24px",
        flex: 1,
      }}
    >
      {/* Glowing logo mark */}
      <div
        className="anim-glow"
        style={{
          width: "80px",
          height: "80px",
          background: "var(--cyan)",
          borderRadius: "16px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexShrink: 0,
        }}
      >
        <span
          className="font-display"
          style={{
            color: "var(--bg-void)",
            fontSize: "32px",
            letterSpacing: "0.04em",
          }}
        >
          CM
        </span>
      </div>

      <div>
        <h1
          className="font-display"
          style={{
            fontSize: "48px",
            lineHeight: 1,
            letterSpacing: "0.06em",
            marginBottom: "10px",
          }}
        >
          <span className="gradient-cyan">CODE</span>
          <span style={{ color: "var(--text-soft)" }}>MIND</span>
        </h1>
        <p
          style={{
            fontSize: "14px",
            color: "var(--text-soft)",
            maxWidth: "360px",
            lineHeight: 1.65,
            fontFamily: "var(--font-mono)",
          }}
        >
          AI-powered code intelligence. Generate, explain, debug and audit code
          instantly.
        </p>
      </div>

      {/* Capability chips */}
      <div
        className="stagger"
        style={{
          display: "flex",
          gap: "8px",
          flexWrap: "wrap",
          justifyContent: "center",
          maxWidth: "480px",
        }}
      >
        {[
          ["⚡", "Generate", "var(--cyan)"],
          ["🔍", "Explain",  "var(--green)"],
          ["🐛", "Debug",    "var(--red)"],
          ["→",  "Complete", "var(--amber)"],
          ["🔐", "Audit",    "var(--purple)"],
          ["✨", "Refactor", "var(--purple)"],
        ].map(([icon, label, color]) => (
          <span
            key={label}
            className="chip anim-fade-in"
            style={{
              color,
              background: `${color}14`,
              border: `1px solid ${color}22`,
            }}
          >
            {icon} {label}
          </span>
        ))}
      </div>

      <div
        className="terminal-cursor"
        style={{
          fontSize: "12px",
          color: "var(--text-ghost)",
          fontFamily: "var(--font-mono)",
        }}
      >
        Type a message to begin
      </div>
    </div>
  );
}
