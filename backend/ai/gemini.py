import google.generativeai as genai
import os
import json
import re
from typing import List, Dict

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = genai.GenerationConfig(
    response_mime_type="application/json",
    temperature=0.6,
)

model = genai.GenerativeModel(
    "models/gemini-flash-latest",
    generation_config=generation_config,
)
async def get_ai_summary(progress_data: List) -> Dict:
    if not progress_data:
        return {
            "summary": "No progress data available.",
            "suggestions": [],
            "progress_distribution": {},
        }

    formatted_entries = "\n".join([
        f"- Date: {entry.date}, Subject: {entry.subject}, Time: {entry.time_spent_minutes} mins, Marks: {entry.marks or 'N/A'}, Notes: {entry.notes or 'None'}"
        for entry in progress_data
    ])

    prompt = f"""
    You are an expert academic performance analyst and productivity coach.
    A student has submitted their recent study progress logs below:

    {formatted_entries}

    Your task:
    1. Analyze the student's learning habits, consistency, and subjects studied.
    2. Identify improvement patterns and weak spots.
    3. Estimate subject-wise effort distribution (as percentages summing to 100).
    4. Provide 3–5 specific improvement suggestions.
    5. Keep the tone motivating but concise.

    ⚠️ Respond ONLY with a valid JSON object in this format:
    {{
        "summary": "A concise yet insightful analysis (max 4 sentences).",
        "suggestions": ["list", "of", "improvement", "tips"],
        "progress_distribution": {{
            "Python": 45,
            "Math": 25,
            "DSA": 30
        }}
    }}
    Ensure percentages roughly sum to 100. 
    Do NOT include any explanations, markdown, or text outside JSON.
    """

    try:
        response = await model.generate_content_async(prompt)
        response_text = response.text.strip()
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            response_text = match.group(0)

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            print("⚠️ JSON parsing failed. Raw response:", response_text)
            return {
                "summary": "Error: Could not parse AI response.",
                "suggestions": [],
                "progress_distribution": {},
            }
        summary = data.get("summary", "No summary provided.")
        suggestions = data.get("suggestions", [])
        progress_distribution = data.get("progress_distribution", {})

        if not isinstance(suggestions, list):
            suggestions = [str(suggestions)]

        if not isinstance(progress_distribution, dict):
            progress_distribution = {}

        return {
            "summary": summary,
            "suggestions": suggestions,
            "progress_distribution": progress_distribution,
        }

    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        return {
            "summary": "Error generating summary.",
            "suggestions": [],
            "progress_distribution": {},
        }
