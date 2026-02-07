from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "support_requests_total",
    "Total number of support requests"
)

RESPONSE_LATENCY = Histogram(
    "support_response_latency_seconds",
    "Response latency"
)
