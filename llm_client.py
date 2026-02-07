import os
from config import Config

USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"

if USE_LOCAL_LLM:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch

    MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto"
    )

def call_llm(prompt: str) -> str:
    if USE_LOCAL_LLM:
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.2
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Cloud fallback
    from openai import OpenAI
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=Config.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
