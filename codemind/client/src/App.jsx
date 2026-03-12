import React from "react";
import { useChatStore } from "./store/chatStore";
import Sidebar from "./components/layout/Sidebar";
import Header from "./components/layout/Header";
import ChatPanel from "./components/chat/ChatPanel";
import UploadPanel from "./components/upload/UploadPanel";
import HistoryPanel from "./components/chat/HistoryPanel";

export default function App() {
  const { activePanel } = useChatStore();

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        overflow: "hidden",
        background: "var(--bg-void)",
        position: "relative",
      }}
    >
      {/* Ambient background glows */}
      <AmbientGlow
        top="-15%"
        left="-5%"
        color="rgba(0, 229, 255, 0.03)"
        size="600px"
      />
      <AmbientGlow
        bottom="-20%"
        right="-10%"
        color="rgba(179, 136, 255, 0.025)"
        size="500px"
      />

      {/* Sidebar */}
      <Sidebar />

      {/* Main area */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          minWidth: 0,
          position: "relative",
          zIndex: 1,
        }}
      >
        <Header />

        {/* Panel content */}
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
            minHeight: 0,
          }}
        >
          {activePanel === "chat" && <ChatPanel />}
          {activePanel === "upload" && <UploadPanel />}
          {activePanel === "history" && <HistoryPanel />}
        </div>
      </div>
    </div>
  );
}

function AmbientGlow({ top, bottom, left, right, color, size }) {
  return (
    <div
      style={{
        position: "fixed",
        top,
        bottom,
        left,
        right,
        width: size,
        height: size,
        background: `radial-gradient(ellipse at center, ${color} 0%, transparent 70%)`,
        pointerEvents: "none",
        zIndex: 0,
      }}
    />
  );
}
