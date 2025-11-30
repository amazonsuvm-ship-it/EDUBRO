import json
from django.shortcuts import render
from ai.local_ai_api import LocalAIApi

def index(request):
    """Render the landing page and handle MCQ generation."""
    context = {}
    if request.method == "POST":
        topic = request.POST.get("topic")
        if topic:
            # This is a simplified example. In a real app, you would have
            # more sophisticated error handling and prompt engineering.
            response = LocalAIApi.create_response(
                {
                    "input": [
                        {'role': 'system', 'content': 'You are an educational content generator. Produce a JSON array of 3 objects, where each object has the following structure: {"question": "...", "options": ["...", "...", "...", "..."], "correct_answer": "...", "explanation": "..."}. The topic is ' + topic + '. Return ONLY valid JSON.'},                        {"role": "user", "content": "Generate 3 MCQs about " + topic},
                    ],
                }
            )

            if response.get("success"):
                # The AI response might be a string that needs to be parsed as JSON.
                # It's important to handle potential JSON parsing errors.
                try:
                    raw_text = LocalAIApi.extract_text(response)
                    mcqs = json.loads(raw_text)
                    # Basic validation to ensure we have a list
                    if isinstance(mcqs, list):
                        context["mcqs"] = mcqs
                    else:
                        context["error"] = "AI returned data in an unexpected format."
                except json.JSONDecodeError:
                    context["error"] = "Failed to parse the response from the AI."
                except Exception as e:
                    context["error"] = f"An unexpected error occurred: {e}"
            else:
                context["error"] = response.get("error", "An unknown error occurred with the AI service.")

    return render(request, "core/index.html", context)
