import { useCallback } from "react";
import { useChatStore } from "../store/chatStore";
import { api } from "../utils/api";

export function useChat() {
  const {
    messages,
    isLoading,
    error,
    sessionId,
    project,
    addMessage,
    setLoading,
    setError,
    clearError,
    setProject,
    clearChat,
  } = useChatStore();

  const sendMessage = useCallback(
    async (prompt) => {
      if (!prompt.trim() || isLoading) return;

      clearError();
      addMessage({ role: "user", content: prompt });
      setLoading(true);

      try {
        const data = await api.sendPrompt({
          project_id: sessionId,
          prompt,
          files_path: project?.files_path || "",
        });

        addMessage({
          role: "assistant",
          content: parseResponse(data),
          intent: data?.intent || null,
          rawData: data,
        });
      } catch (err) {
        addMessage({
          role: "error",
          content: err.message || "An unexpected error occurred.",
        });
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [isLoading, sessionId, project, addMessage, setLoading, setError, clearError]
  );

  const uploadProject = useCallback(
    async (file) => {
      const data = await api.uploadProject({ project_id: sessionId, file });
      setProject(data);
      addMessage({
        role: "assistant",
        content: `**Project uploaded successfully.**\n\nFile: \`${file.name}\`\nFiles path: \`${data.files_path}\`\n\nI now have full context of your codebase. Ask me anything about it.`,
        intent: null,
      });
      return data;
    },
    [sessionId, setProject, addMessage]
  );

  return { messages, isLoading, error, sessionId, project, sendMessage, uploadProject, clearChat };
}

// ─── Parse FastAPI response into markdown string ──────────
function parseResponse(data) {
  if (!data) return "_No response from server._";
  if (typeof data === "string") return data;

  // Array of project files
  if (Array.isArray(data)) {
    const lines = data.map((f) => `- \`${f.file_name}\``).join("\n");
    return `Found **${data.length} file(s)** in your project:\n\n${lines}`;
  }

  if (data.result) return data.result;
  if (data.message) return data.message;

  return "```json\n" + JSON.stringify(data, null, 2) + "\n```";
}
