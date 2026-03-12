import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { useChat } from "../../hooks/useChat";
import { useChatStore } from "../../store/chatStore";
import { IconUpload, IconFolder, IconCheck, IconSpinner } from "../shared/Icons";

export default function UploadPanel() {
  const { uploadProject, project, sessionId } = useChat();
  const { setActivePanel } = useChatStore();
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const onDrop = useCallback(
    async (acceptedFiles, rejectedFiles) => {
      setError(null);
      setSuccess(null);

      if (rejectedFiles.length > 0) {
        setError("Only .rar files are accepted.");
        return;
      }

      const file = acceptedFiles[0];
      if (!file) return;

      setIsUploading(true);
      try {
        await uploadProject(file);
        setSuccess(`"${file.name}" uploaded successfully.`);
        setTimeout(() => setActivePanel("chat"), 1500);
      } catch (err) {
        setError(err.message || "Upload failed. Is the FastAPI server running?");
      } finally {
        setIsUploading(false);
      }
    },
    [uploadProject, setActivePanel]
  );

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: { "application/x-rar-compressed": [".rar"] },
    maxFiles: 1,
    disabled: isUploading,
  });

  const dropBorderColor = isDragReject
    ? "var(--red)"
    : isDragActive
    ? "var(--cyan)"
    : "var(--border-mid)";

  return (
    <div
      className="scroll-container"
      style={{ flex: 1, padding: "40px 32px", maxWidth: "680px" }}
    >
      {/* Title */}
      <div style={{ marginBottom: "32px" }}>
        <h2
          className="font-display"
          style={{ fontSize: "28px", letterSpacing: "0.08em", color: "var(--text-bright)", marginBottom: "8px" }}
        >
          UPLOAD PROJECT
        </h2>
        <p style={{ fontSize: "13px", color: "var(--text-soft)", fontFamily: "var(--font-mono)", lineHeight: 1.7 }}>
          Upload your project as a{" "}
          <code style={{ color: "var(--cyan)" }}>.rar</code> archive to give
          CodeMind full context of your codebase.
        </p>
      </div>

      {/* Dropzone */}
      <div
        {...getRootProps()}
        style={{
          border: `2px dashed ${dropBorderColor}`,
          borderRadius: "6px",
          padding: "48px 32px",
          textAlign: "center",
          cursor: isUploading ? "not-allowed" : "pointer",
          background: isDragActive
            ? "var(--cyan-ghost)"
            : isDragReject
            ? "var(--red-ghost)"
            : "var(--bg-surface)",
          transition: "all 0.2s ease",
          marginBottom: "24px",
        }}
      >
        <input {...getInputProps()} />

        <div
          style={{
            width: "48px",
            height: "48px",
            margin: "0 auto 16px",
            background: isDragActive ? "var(--cyan-ghost)" : "var(--bg-raised)",
            border: `1px solid ${isDragActive ? "var(--cyan)" : "var(--border-mid)"}`,
            borderRadius: "8px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: isDragActive ? "var(--cyan)" : "var(--text-muted)",
            transition: "all 0.2s",
          }}
        >
          {isUploading ? (
            <IconSpinner size={20} />
          ) : (
            <IconUpload size={20} />
          )}
        </div>

        {isUploading ? (
          <div>
            <div style={{ fontSize: "14px", color: "var(--cyan)", fontFamily: "var(--font-mono)", marginBottom: "4px" }}>
              Uploading...
            </div>
            <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>
              Extracting files on server
            </div>
          </div>
        ) : isDragActive ? (
          <div style={{ fontSize: "14px", color: "var(--cyan)", fontFamily: "var(--font-mono)" }}>
            Drop it here
          </div>
        ) : (
          <div>
            <div style={{ fontSize: "14px", color: "var(--text-primary)", marginBottom: "4px", fontWeight: 500 }}>
              Drag &amp; drop your .rar file
            </div>
            <div style={{ fontSize: "12px", color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
              or click to browse — max 50MB
            </div>
          </div>
        )}
      </div>

      {/* Success */}
      {success && (
        <div
          className="anim-fade-in"
          style={{
            padding: "12px 16px",
            background: "var(--green-ghost)",
            border: "1px solid rgba(0,230,118,0.25)",
            borderRadius: "5px",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            marginBottom: "16px",
            fontSize: "13px",
            color: "var(--green)",
            fontFamily: "var(--font-mono)",
          }}
        >
          <IconCheck size={14} />
          {success}
        </div>
      )}

      {/* Error */}
      {error && (
        <div
          className="anim-fade-in"
          style={{
            padding: "12px 16px",
            background: "var(--red-ghost)",
            border: "1px solid rgba(255,61,113,0.25)",
            borderRadius: "5px",
            fontSize: "13px",
            color: "var(--red)",
            fontFamily: "var(--font-mono)",
            marginBottom: "16px",
          }}
        >
          ⚠ {error}
        </div>
      )}

      {/* Session Info */}
      <div
        style={{
          padding: "16px",
          background: "var(--bg-surface)",
          border: "1px solid var(--border-soft)",
          borderRadius: "5px",
        }}
      >
        <div
          style={{
            fontSize: "10px",
            color: "var(--text-muted)",
            fontFamily: "var(--font-mono)",
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            marginBottom: "12px",
          }}
        >
          Session Details
        </div>
        <InfoRow label="Session ID" value={sessionId} />
        <InfoRow
          label="Status"
          value={project ? "Project loaded" : "No project"}
          valueColor={project ? "var(--green)" : "var(--text-muted)"}
        />
        {project && <InfoRow label="Files path" value={project.files_path} />}
      </div>

      {/* Instructions */}
      <div
        style={{
          marginTop: "20px",
          padding: "14px 16px",
          background: "var(--cyan-ghost)",
          border: "1px solid rgba(0,229,255,0.12)",
          borderRadius: "5px",
          fontSize: "12px",
          color: "var(--text-soft)",
          lineHeight: 1.8,
          fontFamily: "var(--font-mono)",
        }}
      >
        <span style={{ color: "var(--cyan)", fontWeight: 600 }}>HOW IT WORKS</span>
        <br />
        1. Archive your project folder as a <code style={{ color: "var(--cyan)" }}>.rar</code> file
        <br />
        2. Drop it here — it gets uploaded and extracted on the server
        <br />
        3. Switch to Chat and ask anything about your codebase
      </div>
    </div>
  );
}

function InfoRow({ label, value, valueColor }) {
  return (
    <div
      style={{
        display: "flex",
        gap: "12px",
        marginBottom: "8px",
        alignItems: "baseline",
      }}
    >
      <span
        style={{
          fontSize: "11px",
          color: "var(--text-muted)",
          fontFamily: "var(--font-mono)",
          minWidth: "90px",
          flexShrink: 0,
        }}
      >
        {label}
      </span>
      <span
        style={{
          fontSize: "11px",
          fontFamily: "var(--font-mono)",
          color: valueColor || "var(--text-primary)",
          wordBreak: "break-all",
        }}
      >
        {value}
      </span>
    </div>
  );
}
