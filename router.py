# Add personas
bot_personas = {
    "bot_A": "AI and crypto will solve everything...",
    "bot_B": "Tech is destroying society...",
    "bot_C": "Markets, ROI, trading..."
}

# Setup embeddings
from langchain.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Create vector DB
from langchain.vectorstores import FAISS

texts = list(bot_personas.values())
ids = list(bot_personas.keys())

vectorstore = FAISS.from_texts(
    texts,
    embedding_model,
    metadatas=[{"id": i} for i in ids]
)

# Write routing function
def route_post_to_bots(post, threshold=0.6):
    results = vectorstore.similarity_search_with_score(post, k=3)

    matched = []

    for doc, score in results:
        similarity = 1 / (1 + score)

        if similarity > threshold:
            matched.append(doc.metadata["id"])

    return matched

# Test it
print(route_post_to_bots(
    "OpenAI released a new AI model replacing developers"
))

if __name__ == "__main__":
    post = "OpenAI released a new AI model"

    result = route_post_to_bots(post)

    print("\n📡 ROUTING RESULT:\n")
    print(result)