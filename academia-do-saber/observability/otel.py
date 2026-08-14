from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import os


resource = Resource.create({"service.name": "academia-do-saber"})

provider = TracerProvider(resource=resource)

processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=f"{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4318')}/v1/traces")
)

provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

print("ACADEMIA observability runtime iniciado")