from prometheus_client import Gauge, Info
import src.Omada as Omada
from src.Prometheus.BaseClient import BaseDeviceMetrics

router_identity_labels = [
    "name",
    "mac",
    "port",
]
router_port_info = [
    "portName",
    "portDesc",
    "mode",
    "ip",
    "poe",
    "linkStatus",
    "internetState",
    "online",
    "linkSpeed",
    "duplex",
    "protocol",
]


class Router(BaseDeviceMetrics):
    temp: Gauge = Gauge(
        "router_temperature", "Router temperature in Celsius", ["name", "mac"]
    )
    port_rx: Gauge = Gauge(
        "router_port_rx_sum", "Sum of received bytes", router_identity_labels
    )
    port_tx: Gauge = Gauge(
        "router_port_tx_sum", "Sum of transmitted bytes", router_identity_labels
    )
    port_loss: Gauge = Gauge(
        "router_port_loss", "Percentage of packet loss on particular port", router_identity_labels
    )
    port_latency: Gauge = Gauge(
        "router_port_latency", "Latency in ms on particular port", router_identity_labels
    )
    port_info: Info = Info(
        "router_port", "Router port information details", router_identity_labels
    )
    port_ipv4_config: Info = Info(
        "router_port_ipv4_config", "Router port ipv4 config", router_identity_labels
    )
    port_ipv6_config: Info = Info(
        "router_port_ipv6_config", "Router port ipv6 config", router_identity_labels
    )


    @staticmethod
    def update_metrics(
        router_metrics: list[Omada.Model.Router], 
        router_port_metrics: list[Omada.Model.Ports.RouterPort]
        ):
        Router.update_base_metrics(router_metrics)
        Router.__update_temperature(router_metrics)
        Router.__update_port_status(router_port_metrics)

    @staticmethod
    def __update_port_status(port_metrics: list[Omada.Model.Ports.RouterPort]):
        for port in port_metrics:
            port_labels = Router.get_labels(port, router_identity_labels)

            Router.port_rx.labels(**port_labels).set(port.rx)
            Router.port_tx.labels(**port_labels).set(port.tx)
            Router.port_loss.labels(**port_labels).set(port.loss)
            Router.port_latency.labels(**port_labels).set(port.latency)
            Router.port_info.labels(**port_labels).info(Router.get_labels(port, router_port_info))

            if port.wanPortIpv4Config is not None:
                Router.port_ipv4_config.labels(
                    **port_labels).info(port.wanPortIpv4Config.model_dump())

            if port.wanPortIpv6Config is not None:
                Router.port_ipv6_config.labels(
                    **port_labels).info(port.wanPortIpv6Config.model_dump())


    @staticmethod
    def __update_temperature(router_metrics: list[Omada.Model.Router]):
        for router in router_metrics:
            labels = Router.get_labels(router, router_identity_labels)
            Router.temp.labels(**labels).set(router.temp)