
from fastapi import FastAPI
import time
import random
import threading
import requests
from uvicorn import Config, Server
import asyncio
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


resource = Resource(attributes={
    "service.name": "SomeAPIEndpoint"
})

# Initialize tracing
trace.set_tracer_provider(TracerProvider(resource=resource))

# Configure the OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="localhost:4317",  # Update with your collector endpoint
    insecure=True,
)

# Use the OTLP exporter
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/endpoint")
async def read_endpoint():
    if random.randint(1, 100) <= 5:
        time.sleep(10)
    return {"message": "Request processed"}

# NOTE: STARTING A FASTAPI APP LIKE THIS IS NOT RECOMMENDED FOR PRODUCTION USAGE. This is because we are trying to be minimal, not robust, with this code.
def run_server():
    config = Config(app=app, host="0.0.0.0", port=8001, log_level="info")
    server = Server(config=config)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server.serve())

def test_endpoint():
    start_time = time.time()
    response = requests.get("http://localhost:8001/endpoint")
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Response status code: {response.status_code}")
    print(f"Response time: {elapsed_time} seconds")

if __name__ == "__main__":
    # Start the server in a new thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    time.sleep(2)  # Give the server a bit of time to actually start

    test_endpoint()

    # Once tests are done, you might want to stop the server
    # This can be tricky depending on your exact requirements and setup


