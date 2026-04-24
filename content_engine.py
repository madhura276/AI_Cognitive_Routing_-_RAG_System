from dotenv import load_dotenv
import os
import json
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- MOCK SEARCH TOOL ---------------- #
def mock_searxng_search(query: str):
    query = query.lower()

    if "ai" in query:
        return "OpenAI releases new model that may replace junior developers"
    elif "crypto" in query:
        return "Bitcoin hits new all-time high amid ETF approvals"
    elif "market" in query or "finance" in query:
        return "Stock markets show volatility due to interest rate uncertainty"
    else:
        return "Global tech trends are evolving rapidly"


# ---------------- SAFE JSON PARSER ---------------- #
def safe_json_parse(text: str):
    try:
        return json.loads(text)
    except:
        return {
            "error": "Invalid JSON",
            "raw_output": text
        }


# ---------------- DECIDE TOPIC ---------------- #
def decide_topic(persona: str):

    prompt = f"""
You are this persona:
{persona}

Decide ONE specific topic this persona would post about today.

RULES:
- Max 5 words
- No explanation
- Only return topic text
"""

    response = llm.invoke(prompt).content.strip()
    return response


# ---------------- GENERATE POST ---------------- #
def generate_post(bot_id: str, persona: str, context: str):

    prompt = f"""
You are an AI bot with this personality:
{persona}

Context:
{context}

TASK:
Write a VERY opinionated, bold post under 280 characters.

STYLE RULES:
- Strong tone
- Confident
- Not generic
- Reflect persona clearly

STRICT OUTPUT:
Return ONLY valid JSON:

{{
  "bot_id": "{bot_id}",
  "topic": "{context}",
  "post_content": "your post here"
}}
"""

    response = llm.invoke(prompt).content

    return safe_json_parse(response)


# ---------------- MAIN FLOW ---------------- #
def run_content_engine(bot_id: str, persona: str):

    topic = decide_topic(persona)
    context = mock_searxng_search(topic)

    result = generate_post(bot_id, persona, context)

    return result


# ---------------- TEST ---------------- #
if __name__ == "__main__":

    persona = """I believe AI and crypto will solve all human problems.
I am highly optimistic about technology, Elon Musk, and space exploration.
I dismiss regulatory concerns."""

    output = run_content_engine("bot_A", persona)

    print("\n🚀 GENERATED POST:\n")
    print(json.dumps(output, indent=2))