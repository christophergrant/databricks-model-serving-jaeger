import time
import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource

resource = Resource(attributes={
    "service.name": "DatabricksModelServingEndpoint"
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

# Instrument requests
RequestsInstrumentor().instrument()


def preprocess():
     time.sleep(0.015)

def call_endpoint():
    response = requests.get("http://127.0.0.1:8001/endpoint")
    return response

def test_endpoint():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("predict"):
        with tracer.start_as_current_span("preprocess"):
            preprocess()
        with tracer.start_as_current_span("call_endpoint"):
            call_endpoint()

if __name__ == "__main__":
    for _ in range(100): test_endpoint()

    # Export remaining spans
    trace.get_tracer_provider().shutdown()

