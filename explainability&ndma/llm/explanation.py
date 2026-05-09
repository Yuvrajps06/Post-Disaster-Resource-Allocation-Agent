from llm.gemini_client import client

def generate_explanation(data):

    prompt = f"""
    You are an NDMA disaster response assistant.

    Explain this recommendation clearly.

    Data:
    {data}

    Keep response concise and professional.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text