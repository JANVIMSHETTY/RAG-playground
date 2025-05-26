import openai

# Using OpenAI as example — you can replace this with Groq, Gemini, OpenRouter
def call_llm(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message["content"]
