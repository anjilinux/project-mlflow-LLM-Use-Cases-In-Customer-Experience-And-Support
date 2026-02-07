from fastapi import FastAPI
from schema import SupportRequest, SupportResponse
from llm_client import call_llm
from rag import retrieve_context
from prompts import support_prompt
from logger import get_logger
from monitor import REQUEST_COUNT, RESPONSE_LATENCY
import time
from mlflow_utils import log_llm_call

app = FastAPI(title="LLM Customer Support")

logger = get_logger()

with open("sample_faqs.txt") as f:
    docs = f.read().split("\n\n")

@app.post("/support", response_model=SupportResponse)
def support(req: SupportRequest):
    start = time.time()
    REQUEST_COUNT.inc()

    context = retrieve_context(req.question, docs)
    prompt = support_prompt(context, req.question)
    answer = call_llm(prompt)
  
    latency = time.time() - start
    log_llm_call(prompt, answer, latency)

    RESPONSE_LATENCY.observe(time.time() - start)
    logger.info(f"Question: {req.question}")

    return {"answer": answer}
