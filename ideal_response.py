from prometheus_api_client import PrometheusConnect
import requests


# Connect to the Prometheus server
prometheus = PrometheusConnect(url="http://prometheus-server:9090", disable_ssl=True)

# Function to query Prometheus metrics for a specific service
def get_service_metrics(service_name):
    try:
        query = f'http_requests_total{{service="{service_name}"}}'
        metrics = prometheus.custom_query(query)
        print(f"Metrics for {service_name}: {metrics}")
        return metrics
    except Exception as e:
        print(f"Error retrieving metrics for {service_name}: {e}")
        return []

# Query the Jaeger API for traces of a specific service
def get_service_traces(service_name):
    try:
        jaeger_url = "http://jaeger-query:16686/api/traces"
        params = {"service": service_name}
        response = requests.get(jaeger_url, params=params)

        if response.status_code == 200:
            traces = response.json()
            print(f"Traces for {service_name}: {traces}")
            return traces
        else:
            print(f"Failed to retrieve traces. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error retrieving traces for {service_name}: {e}")
        return None

# Analyze the metrics and provide scaling recommendations
def analyze_metrics(metrics):
    try:
        # Example: Extract response times from the metrics
        response_times = [float(metric['value'][1]) for metric in metrics if 'value' in metric]
        
        if not response_times:
            print("No response time data available.")
            return
        
        avg_response_time = sum(response_times) / len(response_times)
        print(f"Average response time: {avg_response_time:.2f}ms")

        # Check if scaling is needed
        if avg_response_time > 1000:  # Example threshold
            print("Recommendation: Scale up the service to handle the load.")
        else:
            print("Recommendation: Current scaling level is adequate.")
    except Exception as e:
        print(f"Error analyzing metrics: {e}")

# Main execution
if __name__ == "__main__":
    # Service name to query
    service_name = "my-service"

    # Retrieve metrics
    service_metrics = get_service_metrics(service_name)

    # Analyze metrics if available
    if service_metrics:
        analyze_metrics(service_metrics)

    # Retrieve traces
    service_traces = get_service_traces(service_name)
