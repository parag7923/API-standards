from openai import OpenAI

# Initialize the Sambanova client
SAMBANOVA_API_URL = "https://fast-api.snova.ai/v1"
SAMBANOVA_API_KEY = 'YOUR-KEY-HERE'

client = OpenAI(
    base_url=SAMBANOVA_API_URL,
    api_key=SAMBANOVA_API_KEY,
)

def call_llama(sys_prompt, prompt, **kwargs):
    completion = client.chat.completions.create(
        model="Meta-Llama-3.1-405B-Instruct",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        stream=True,
        **kwargs,
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response


user_prompt = "Where is Sacramento?"
output = call_llama("You are an helpful assistant.",user_prompt)
print(output)