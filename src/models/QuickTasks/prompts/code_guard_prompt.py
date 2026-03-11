import json
from models.QuickTasks.states import CodeAuditResult

def build_detailed_audit_messages(state):
    
    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are a senior software security engineer.",
                "",
                "Your task is to audit the provided code for security issues, authentication problems, and potential vulnerabilities.",
                "",
                "Guidelines:",
                "- Detect authentication or authorization problems",
                "- Detect SQL injection, XSS, command injection, or unsafe functions",
                "- Detect hard-coded credentials, secrets, or tokens",
                "- Detect weak password handling or unsafe storage",
                "- Detect unsafe external dependencies or imports",
                "- Rate the severity of each issue: low, medium, high",
                "- Suggest safer alternatives or fixes when possible",
                "",
                "Output Rules:",
                "- Return ONLY valid JSON matching the schema",
                "- Do NOT include explanations outside JSON",
                "- Preserve code formatting if returning 'fixed_code'"
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"Code to audit:\n{state.code_context.code or ''}",
                "",
                "## Output Schema",
                json.dumps(CodeAuditResult.model_json_schema(), indent=2),
                "",
                "## Output",
                "```json"
            ])
        }
    ]
    
    return messages


import json
from models.QuickTasks.states import CodeAuditResult

def build_short_audit_messages(state):
    
    messages = [
        {
            "role": "system",
            "content": "You are an AI that audits code for security issues. Detect vulnerabilities and suggest fixes. Return JSON only."
        },
        {
            "role": "user",
            "content": "\n".join([
                f"Code:\n{state.code_context.code or ''}",
                "",
                "## Output Schema",
                json.dumps(CodeAuditResult.model_json_schema(), indent=2),
                "",
                "## Output",
                "```json"
            ])
        }
    ]
    
    return messages