from prometheus_client import Gauge, Info
import src.Omada as Omada
from src.Prometheus.BaseClient import BaseDeviceMetrics

switch_identity_labels = [
    "name",
    "mac",
    "port"
]
switch_port_info = [
    "portName",
    "disable",
    "profileName",
    "operation",
    "linkStatus",
    "linkSpeed",
    "duplex",
    "poe"
]


class Switch(BaseDeviceMetrics):
    port_rx: Gauge = Gauge(
        "switch_port_rx_sum", "Sum of received bytes", switch_identity_labels
    )
    port_tx: Gauge = Gauge(
        "switch_port_tx_sum", "Sum of transmitted bytes", switch_identity_labels
    )
    port_rx_rate: Gauge = Gauge(
        "switch_port_rx_rate", "Received bytes per second", switch_identity_labels
    )
    port_tx_rate: Gauge = Gauge(
        "switch_port_tx_rate", "Transmitted bytes per second", switch_identity_labels
    )
    port_info: Info = Info(
        "switch_port", "Switch port information details", switch_identity_labels
    )
    port_rx_pkts: Gauge = Gauge(
        "switch_port_rx_pkts", "Received packets", switch_identity_labels
    )
    port_tx_pkts: Gauge = Gauge(
        "switch_port_tx_pkts", "Transmitted packets", switch_identity_labels
    )
    port_rx_err_pkts: Gauge = Gauge(
        "switch_port_rx_err_pkts", "Received packets errors", switch_identity_labels
    )
    port_tx_err_pkts: Gauge = Gauge(
        "switch_port_tx_err_pkts", "Transmitted packets errors", switch_identity_labels
    )
    port_drop_pkts: Gauge = Gauge(
        "switch_drop_pkts", "Dropped packets", switch_identity_labels
    )

    @staticmethod
    def update_metrics(
        switch_metrics: list[Omada.Model.Switch],
        switch_port_metrics: list[Omada.Model.Ports.SwitchPort],
        switch_port_stats: list[Omada.Model.Ports.SwitchPortStats]
    ):
        Switch.update_base_metrics(switch_metrics)
        Switch.__update_port_status(switch_port_metrics)
        Switch.__update_port_statistics(switch_port_stats)

    @staticmethod
    def __update_port_status(switch_port_metrics: list[Omada.Model.Ports.SwitchPort]):
        for port in switch_port_metrics:
            port_labels: dict[str, str] = Switch.get_labels(
                port, switch_identity_labels)

            Switch.port_rx.labels(**(port_labels)).set(port.rx)
            Switch.port_tx.labels(**(port_labels)).set(port.tx)
            Switch.port_info.labels(
                **(port_labels)).info(Switch.get_labels(port, switch_port_info))

    @staticmethod
    def __update_port_statistics(switch_port_stats: list[Omada.Model.Ports.SwitchPortStats]):
        for port in switch_port_stats:
            port_labels: dict[str, str] = Switch.get_labels(
                port, switch_identity_labels)

            Switch.port_rx_rate.labels(**(port_labels)).set(port.rxRate)
            Switch.port_tx_rate.labels(**(port_labels)).set(port.txRate)
            Switch.port_rx_pkts.labels(**(port_labels)).set(port.rxPkts)
            Switch.port_tx_pkts.labels(**(port_labels)).set(port.txPkts)
            Switch.port_rx_err_pkts.labels(**(port_labels)).set(port.rxErrPkts)
            Switch.port_tx_err_pkts.labels(**(port_labels)).set(port.dropPkts)
            Switch.port_drop_pkts.labels(**(port_labels)).set(port.txErrPkts)
