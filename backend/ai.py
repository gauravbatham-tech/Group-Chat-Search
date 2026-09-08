import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(query, results):

    context = ""

    for result in results:

        context += "\n---\n"

        for msg in result["context"]:

            context += (
                f"{msg['timestamp']} | "
                f"{msg['sender']}: "
                f"{msg['message']}\n"
            )

    prompt = f"""
You are a group chat search assistant.

Answer the user's question ONLY using the conversation below.

If the conversation does not contain enough information,
say exactly:

"I couldn't find enough information in the conversation."

Do not invent information.

User question:
{query}

Conversation:
{context}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text