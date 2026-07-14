from agent.graph import graph
from groq_ai import ask_groq
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import engine
from agent.graph import graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Models
# -----------------------------
class Interaction(BaseModel):
    doctor_name: str
    hospital: str
    topics: str
    ai_response: str


class AIRequest(BaseModel):
    text: str


# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {"message": "HCP AI Backend Running Successfully"}


# -----------------------------
# Save Interaction
# -----------------------------
@app.post("/log-interaction")
def log_interaction(data: Interaction):

    query = """
    INSERT INTO interactions
    (doctor_name, hospital, topics, ai_response)
    VALUES (%s, %s, %s, %s)
    """

    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute(
        query,
        (
            data.doctor_name,
            data.hospital,
            data.topics,
            data.ai_response,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Interaction Saved Successfully"}


# -----------------------------
# Ask AI
# -----------------------------
@app.post("/ask-ai")
def ask_ai(data: AIRequest):
    try:
     result = graph.invoke({
       "text": data.text,
       "response": ""
     })

     return {
       "response": result["response"]
     }

    except Exception as e:
        return {"response": str(e)}


# -----------------------------
# Get History
# -----------------------------
@app.get("/interactions")
def get_interactions():

    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            doctor_name,
            hospital,
            topics,
            ai_response,
            created_at
        FROM interactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    history = []

    for row in rows:
        history.append({
            "id": row[0],
            "doctor_name": row[1],
            "hospital": row[2],
            "topics": row[3],
            "ai_response": row[4],
            "created_at": str(row[5])
        })

    cursor.close()
    conn.close()

    return history

@app.put("/edit-interaction/{interaction_id}")
def edit_interaction(interaction_id: int, data: Interaction):

    conn = engine.raw_connection()
    cursor = conn.cursor()

    query = """
    UPDATE interactions
    SET doctor_name=%s,
        hospital=%s,
        topics=%s,
        ai_response=%s
    WHERE id=%s
    """

    cursor.execute(
        query,
        (
            data.doctor_name,
            data.hospital,
            data.topics,
            data.ai_response,
            interaction_id,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Interaction Updated Successfully"}