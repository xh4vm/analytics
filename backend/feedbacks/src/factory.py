
from core.config import SETTINGS
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(
        resource=Resource(attributes={SERVICE_NAME: SETTINGS.tracer.service_name})
    ))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=SETTINGS.tracer.host,
                agent_port=SETTINGS.tracer.port,
            )
        )
    )
