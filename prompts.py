def support_prompt(context, question):
    return f"""
You are a customer support agent.

Context:
{context}

Customer Question:
{question}

Provide a clear and polite response.
"""
