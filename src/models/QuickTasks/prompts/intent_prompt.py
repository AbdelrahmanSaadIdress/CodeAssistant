import json
from models.QuickTasks.states import Intent


def build_intent_messages(user_prompt):

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are an AI system responsible for classifying requests for a coding assistant.",
                "",
                "Your job is to analyze the user's input and classify it into ONE intent.",
                "",
                "Available Intents:",
                "",
                "generate_code:",
                "- The user asks to create new code from a description.",
                "- Examples: 'write a function', 'implement', 'create a class'.",
                "",
                "autocomplete:",
                "- The user provides partial code and expects it to be completed.",
                "- The request may contain unfinished code.",
                "- IMPORTANT: If the user input contains ONLY code and no explanation, classify it as 'autocomplete'.",
                "",
                "explain_code:",
                "- The user asks for an explanation of existing code.",
                "- Examples: 'explain this code', 'what does this function do?'.",
                "",
                "bug_detection:",
                "- The user asks to find or fix errors in code.",
                "- Examples: 'why is this not working?', 'find the bug'.",
                "",
                "refactor:",
                "- The user asks to improve or restructure existing code without changing behavior.",
                "- Examples: 'refactor this code', 'make this cleaner', 'optimize structure'.",
                "",
                "Classification Rules:",
                "- Choose exactly ONE intent.",
                "- If the input is ONLY code with no instruction → autocomplete.",
                "- If the user asks to fix an error → bug_detection.",
                "- If the user asks to explain code → explain_code.",
                "- If the user asks to improve code structure → refactor.",
                "- If the user asks to create new code → generate_code.",
                "",
                "Output Rules:",
                "- Return ONLY valid JSON.",
                "- The JSON MUST match the provided schema.",
                "- Do NOT include explanations or markdown."
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                "User Request:",
                user_prompt,
                "",
                "## Output Schema",
                json.dumps(Intent.model_json_schema(), indent=2),
                "",
                "## Output",
                "```json"
            ])
        }
    ]

    return messages