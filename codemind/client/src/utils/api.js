const BASE = "/api";

class APIError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function request(url, options = {}) {
  const res = await fetch(`${BASE}${url}`, options);
  const text = await res.text();

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { result: text };
  }

  if (!res.ok) {
    throw new APIError(data?.error || data?.detail || `HTTP ${res.status}`, res.status);
  }

  return data;
}

export const api = {
  /** GET /api/info — Returns app name + version from FastAPI */
  getInfo: () => request("/info"),

  /** POST /api/quick-tasks/help — Main AI pipeline endpoint */
  sendPrompt: ({ project_id, prompt, files_path = "" }) =>
    request("/quick-tasks/help", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id, prompt, files_path }),
    }),

  /** POST /api/projects/upload — Upload .rar project archive */
  uploadProject: ({ project_id, file }) => {
    const formData = new FormData();
    formData.append("project_id", project_id);
    formData.append("file", file);
    return request("/projects/upload", { method: "POST", body: formData });
  },

  /** GET /health — Node server health check */
  healthCheck: () => request("/health"),
};

export { APIError };
