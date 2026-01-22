from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client
import os

load_dotenv()

SUPABASE_URL=os.environ.get("FIRST_SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY=os.environ.get("FIRST_SUPABASE_SERVICE_ROLE_KEY")
sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

app = Flask(__name__, static_folder="public", static_url_path="")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT_ONE = {
    "role": "system",
    "content": (
        "Keep it short, 5 sentences non_nagotiable."
        "Use simple vocabulary."
        "You are an expert on all things related to programming."
        "You have deep knowledge of programming languages, eartquakes, floods, global warming, general knowledgr of geography, politics, "
        "law, culture, mental health, climate, universities, technology, and local customs. "
        "When answering questions, prioritize programming-specific context, "
        "examples, and accuracy."

       "- Speak like a human, not a chatbot."
       "- Never reference being an AI or a chatbot"
       "- Respond directly to what the other person said."
       "- Do not repeat information the other person already knows."
       "- Avoid over-explaining or lecturing."

       "- If you answer a question, you may ask at most one follow-up question."
       "- If the other person asked a question, answer it before introducing anything new."
       "- Ask a follow-up question only if it genuinely advances the conversation."

       "Build a natural, flowing conversation that feels mutual and evolving rather than scripted."
       
    )
}

# takes in the string and outputs a vector
def embed_query(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

# takes as input a query, conducts the search, returns context
def semantic_search(query_text: str) -> list[dict]:
    emb_q = embed_query(query_text)
    res = sb.rpc("match_chunks", {"query_embedding": emb_q, "match_count" : 5}).execute()
    rows = res.data or []
    # for easier debugging
    print("RAG OUTPUT:", rows)
    return rows

@app.get("/")
def index():
    return send_from_directory("public", "index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")

    # conduct semantic search
    rag_rows = semantic_search(user_message)

    # fixes our formatting
    context = "\n\n".join(
        f"[Source {i+1} | sim={row.get('similarity'):.3f}]\n{row.get('content','')}"
        for i, row in enumerate(rag_rows)
    )

    # create the rag prompt
    rag_message = {
        "role": "system",
        "content": (
            "Use the retrieved context below to answer. If it doesn't contain the answer, say so. \n\n"
            f"RETRIEVED CONTEXT:\n{context if context else '(no matches)'}"
        )
    }

    full_user_message = {
        "role": "user",
        "content": user_message,
    }

    full_message = [rag_message, full_user_message, SYSTEM_PROMPT_ONE]

    resp = client.responses.create(
        model="gpt-5-nano",
        input=full_message
    )
    return jsonify({"text": resp.output_text})

# Serves /styles.css, /app.js, etc.
@app.get("/<path:path>")
def static_files(path):
    return send_from_directory("public", path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)