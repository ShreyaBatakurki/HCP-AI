from langchain_core.tools import tool
from .llm import llm
from database import engine


@tool
def log_interaction(
    doctor_name: str,
    hospital: str,
    topics: str,
    ai_response: str,
):
    """
    Log a new HCP interaction into the database.
    """

    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interactions
        (doctor_name,hospital,topics,ai_response)
        VALUES (%s,%s,%s,%s)
        """,
        (doctor_name, hospital, topics, ai_response),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return "Interaction Logged Successfully"


@tool
def edit_interaction(
    interaction_id: int,
    doctor_name: str,
    hospital: str,
    topics: str,
    ai_response: str,
):
    """
    Edit an existing interaction.
    """

    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interactions
        SET doctor_name=%s,
            hospital=%s,
            topics=%s,
            ai_response=%s
        WHERE id=%s
        """,
        (
            doctor_name,
            hospital,
            topics,
            ai_response,
            interaction_id,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return "Interaction Updated Successfully"


@tool
def get_history():
    """
    Return all HCP interaction history.
    """

    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               doctor_name,
               hospital,
               topics,
               ai_response
        FROM interactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return str(rows)


@tool
def summarize_interaction(text: str):
    """
    Summarize an HCP interaction.
    """

    return llm.invoke(
        f"Summarize this HCP interaction:\n{text}"
    ).content


@tool
def suggest_followup(text: str):
    """
    Suggest follow-up actions.
    """

    return llm.invoke(
        f"""
You are a pharmaceutical sales assistant.

Suggest the next follow-up action for:

{text}
"""
    ).content


TOOLS = [
    log_interaction,
    edit_interaction,
    get_history,
    summarize_interaction,
    suggest_followup,
]