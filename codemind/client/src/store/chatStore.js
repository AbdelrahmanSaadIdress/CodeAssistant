import { create } from "zustand";
import { v4 as uuid } from "uuid";

// ─── Intent metadata ──────────────────────────────────────
export const INTENT_META = {
  generate_code: {
    label: "Generate",
    color: "var(--cyan)",
    bg: "var(--cyan-ghost)",
    icon: "⚡",
  },
  explain_code: {
    label: "Explain",
    color: "var(--green)",
    bg: "var(--green-ghost)",
    icon: "🔍",
  },
  bug_detection: {
    label: "Bug Fix",
    color: "var(--red)",
    bg: "var(--red-ghost)",
    icon: "🐛",
  },
  autocomplete: {
    label: "Autocomplete",
    color: "var(--amber)",
    bg: "var(--amber-ghost)",
    icon: "→",
  },
  refactor: {
    label: "Refactor",
    color: "var(--purple)",
    bg: "var(--purple-ghost)",
    icon: "✨",
  },
};

// ─── Chat Store ───────────────────────────────────────────
export const useChatStore = create((set, get) => ({
  // Session
  sessionId: uuid(),
  messages: [makeWelcomeMessage()],
  isLoading: false,
  error: null,

  // Project
  project: null, // { files_path, project_id, message }

  // UI
  activePanel: "chat", // "chat" | "upload" | "history"
  sidebarOpen: true,

  // ── Actions ───────────────────────────────────────────
  setActivePanel: (panel) => set({ activePanel: panel }),
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),

  addMessage: (msg) =>
    set((s) => ({ messages: [...s.messages, { id: uuid(), timestamp: new Date(), ...msg }] })),

  setLoading: (v) => set({ isLoading: v }),
  setError: (e) => set({ error: e }),
  clearError: () => set({ error: null }),

  setProject: (project) => set({ project }),

  clearChat: () =>
    set({
      messages: [makeWelcomeMessage()],
      error: null,
    }),
}));

function makeWelcomeMessage() {
  return {
    id: uuid(),
    role: "assistant",
    timestamp: new Date(),
    content:
      "## Welcome to CodeMind\n\nI'm your AI code intelligence layer. I can:\n\n- **Generate** production-ready code from a description\n- **Explain** any code block line-by-line\n- **Detect & fix** bugs and logic errors\n- **Autocomplete** partial code snippets\n- **Audit** code for security vulnerabilities\n- **Refactor** for clarity and performance\n\nPaste your code or describe what you need.",
    intent: null,
  };
}
