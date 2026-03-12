require("dotenv").config();
const express = require("express");
const cors = require("cors");
const multer = require("multer");
const fetch = require("node-fetch");
const FormData = require("form-data");

const app = express();
const PORT = process.env.PORT || 4000;
const FASTAPI_BASE = process.env.FASTAPI_BASE_URL || "http://localhost:8000";

// ─── Middleware ────────────────────────────────────────────────────────────────
app.use(cors({ origin: process.env.CLIENT_ORIGIN || "http://localhost:5173" }));
app.use(express.json({ limit: "10mb" }));

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 50 * 1024 * 1024 }, // 50MB
});

// ─── Request Logger ────────────────────────────────────────────────────────────
app.use((req, _res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// ─── Health Check ──────────────────────────────────────────────────────────────
app.get("/health", (_req, res) => {
  res.json({
    status: "ok",
    timestamp: new Date().toISOString(),
    backend: FASTAPI_BASE,
  });
});

// ─── Proxy: App Info ───────────────────────────────────────────────────────────
app.get("/api/info", async (_req, res) => {
  try {
    const response = await fetch(`${FASTAPI_BASE}/api/v1/`);
    if (!response.ok) throw new Error(`Backend returned ${response.status}`);
    res.json(await response.json());
  } catch (err) {
    res.status(502).json({ error: "Backend unreachable", detail: err.message });
  }
});

// ─── Proxy: Quick Tasks ────────────────────────────────────────────────────────
app.post("/api/quick-tasks/help", async (req, res) => {
  try {
    const { project_id, prompt, files_path } = req.body;

    if (!project_id?.trim() || !prompt?.trim()) {
      return res
        .status(400)
        .json({ error: "project_id and prompt are required" });
    }

    const response = await fetch(`${FASTAPI_BASE}/api/v1/quick-tasks/help`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project_id,
        prompt,
        files_path: files_path || "",
      }),
    });

    const text = await response.text();
    if (!response.ok) {
      return res
        .status(response.status)
        .json({ error: `Backend error: ${text}` });
    }

    try {
      res.json(JSON.parse(text));
    } catch {
      res.json({ result: text });
    }
  } catch (err) {
    res
      .status(502)
      .json({ error: "Failed to reach backend", detail: err.message });
  }
});

// ─── Proxy: Upload Project ─────────────────────────────────────────────────────
app.post("/api/projects/upload", upload.single("file"), async (req, res) => {
  try {
    const { project_id } = req.body;

    if (!project_id?.trim()) {
      return res.status(400).json({ error: "project_id is required" });
    }

    if (!req.file) {
      return res.status(400).json({ error: "No file provided" });
    }

    const formData = new FormData();
    formData.append("project_id", project_id);
    formData.append("file", req.file.buffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype,
    });

    const response = await fetch(`${FASTAPI_BASE}/api/v1/projects/upload`, {
      method: "POST",
      body: formData,
      headers: formData.getHeaders(),
    });

    const text = await response.text();
    if (!response.ok) {
      return res
        .status(response.status)
        .json({ error: `Upload failed: ${text}` });
    }

    res.json(JSON.parse(text));
  } catch (err) {
    res.status(502).json({ error: "Upload failed", detail: err.message });
  }
});

// ─── 404 Catch ─────────────────────────────────────────────────────────────────
app.use((_req, res) => {
  res.status(404).json({ error: "Route not found" });
});

// ─── Start ─────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`\n┌─────────────────────────────────────────┐`);
  console.log(`│  CodeMind Server  →  http://localhost:${PORT}  │`);
  console.log(`│  FastAPI Backend  →  ${FASTAPI_BASE}  │`);
  console.log(`└─────────────────────────────────────────┘\n`);
});
