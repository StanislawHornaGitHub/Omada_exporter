from src.Prometheus.AccessPoint import AccessPoint
from src.Prometheus.Switch import Switch
from src.Prometheus.Router import Router
from prometheus_client import Gauge, Info

MD_FILE_PATH = "./metrics.md"
MD_TABLE_HEADERS = "|Device|Metric|Description|\n|-|-|-|\n"
MD_TABLE_LINE = "|{device_type}|{metric_name}|{metric_description}|\n"

def get_metric_descriptions(cls, type_name: str) -> list[str]:
    
    result: list[str] = []
    
    for attribute_name in dir(cls):
        attribute = getattr(cls, attribute_name)
        # Check if the attribute is a Gauge or Info instance
        if isinstance(attribute, (Gauge, Info)):
            # Print the metric name and description
            result.append(
                MD_TABLE_LINE.format(
                    device_type=type_name,
                    metric_name=attribute._name,
                    metric_description=attribute._documentation
                )
            )
    
    return result


def main():
    ap_metrics = get_metric_descriptions(AccessPoint, "AccessPoint")
    gw_metrics = get_metric_descriptions(Router, "Router")
    sw_metrics = get_metric_descriptions(Switch, "Switch")
    
    with open(MD_FILE_PATH, "w") as file:
        file.write(MD_TABLE_HEADERS)
        file.writelines(ap_metrics)
        file.writelines(gw_metrics)
        file.writelines(sw_metrics)
        

if __name__ == "__main__":
    main()