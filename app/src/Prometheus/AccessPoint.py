from prometheus_client import Gauge, Info
import src.Omada as Omada
from src.Prometheus.BaseClient import BaseDeviceMetrics

access_point_port_identity_labels = [
    "name",
    "mac",
]

access_point_port_labels = [
    "name",
    "mac",
    "uplinkMac",
    "uplinkDeviceType",
    "linkSpeed",
    "duplex",
]
access_point_radio_labels = [
    "name",
    "mac",
    "frequency",
]

access_point_radio_info =[
    "actualChannel",
    "maxTxRate",
    "region",
    "bandWidth",
    "mode",
]


class AccessPoint(BaseDeviceMetrics):
    port_rx: Gauge = Gauge(
        "access_point_port_rx_sum", "Sum of received bytes", access_point_port_identity_labels
    )
    port_tx: Gauge = Gauge(
        "access_point_port_tx_sum", "Sum of transmitted bytes", access_point_port_identity_labels
    )
    port_info: Info = Info(
        "access_point_port", "Access point port info", access_point_port_identity_labels
    )
    radio_rx: Gauge = Gauge(
        "radio_rx_sum", "Sum of received bytes", access_point_radio_labels
    )
    radio_tx: Gauge = Gauge(
        "radio_tx_sum", "Sum of transmitted bytes", access_point_radio_labels
    )
    radio_info: Info = Info(
        "radio", "Access point radio details", access_point_radio_labels
    )
    radio_rx_util: Gauge = Gauge(
        "radio_rx_util", "Percentage of receive channel bandwidth usage", access_point_radio_labels
    )
    radio_tx_util: Gauge = Gauge(
        "radio_tx_util", "Percentage of transmit channel bandwidth usage", access_point_radio_labels
    )
    radio_rx_rate: Gauge = Gauge(
        "radio_rx_rate", "Received bits per second", access_point_radio_labels
    )
    radio_tx_rate: Gauge = Gauge(
        "radio_tx_rate", "Transmitted bits per second", access_point_radio_labels
    )
    radio_rx_retry_pkts_rate: Gauge = Gauge(
        "radio_rx_retry_pkts_rate", "Received packets retry", access_point_radio_labels
    )
    radio_tx_retry_pkts_rate: Gauge = Gauge(
        "radio_tx_retry_pkts_rate", "Transmitted packets retry", access_point_radio_labels
    )
    radio_rx_pkts: Gauge = Gauge(
        "radio_rx_pkts_sum", "Sum of received packets", access_point_radio_labels
    )
    radio_tx_pkts: Gauge = Gauge(
        "radio_tx_pkts_sum", "Sum of transmitted packets", access_point_radio_labels
    )
    radio_rx_pkts_dropped: Gauge = Gauge(
        "radio_rx_pkts_dropped_sum", "Sum of dropped rx packets", access_point_radio_labels
    )
    radio_tx_pkts_dropped: Gauge = Gauge(
        "radio_tx_pkts_dropped_sum", "Sum of dropped tx packets", access_point_radio_labels
    )
    radio_rx_pkts_error: Gauge = Gauge(
        "radio_rx_pkts_error_sum", "Sum of error rx packets", access_point_radio_labels
    )
    radio_tx_pkts_error: Gauge = Gauge(
        "radio_tx_pkts_error_sum", "Sum of error tx packets", access_point_radio_labels
    )
    radio_rx_pkts_retry: Gauge = Gauge(
        "radio_rx_pkts_retry_sum", "Sum of retry rx packets", access_point_radio_labels
    )
    radio_tx_pkts_retry: Gauge = Gauge(
        "radio_tx_pkts_retry_sum", "Sum of retry tx packets", access_point_radio_labels
    )

    @staticmethod
    def update_metrics(
        access_point_metrics: list[Omada.Model.AccessPoint],
        access_point_port_metrics: list[Omada.Model.Ports.AccessPointPort],
        access_point_radio_metrics: list[Omada.Model.Ports.AccessPointRadio],
        access_point_radio_stats: list[Omada.Model.Ports.AccessPointRadioStats]
    ):
        AccessPoint.update_base_metrics(access_point_metrics)
        AccessPoint.__update_port_status(access_point_port_metrics)
        AccessPoint.__update_radio_traffic_stats(access_point_radio_metrics)
        AccessPoint.__update_radio_stats(access_point_radio_stats)

    @staticmethod
    def __update_port_status(port_metrics: list[Omada.Model.Ports.AccessPointPort]):
        for port in port_metrics:
            port_labels = AccessPoint.get_labels(port, access_point_port_identity_labels)
            
            AccessPoint.port_rx.labels(**port_labels).set(port.rx)
            AccessPoint.port_tx.labels(**port_labels).set(port.tx)
            

    @staticmethod
    def __update_radio_traffic_stats(radio_metrics: list[Omada.Model.Ports.AccessPointRadio]):
        for device in radio_metrics:
            for field_name, value in device:
                if field_name in ["radioConfig24GHz","radioConfig50GHz"]:
                    radio_config_labels = AccessPoint.get_labels(value,access_point_radio_labels)
                    
                    AccessPoint.radio_rx_util.labels(**radio_config_labels).set(value.rxUtil)
                    AccessPoint.radio_tx_util.labels(**radio_config_labels).set(value.txUtil)
                    AccessPoint.radio_info.labels(**radio_config_labels).info(
                        AccessPoint.get_labels(value, access_point_radio_info)
                    )
                    
                
                if field_name in ["radioTraffic24GHz","radioTraffic50GHz"]:
                    radio_traffic_labels = AccessPoint.get_labels(value,access_point_radio_labels)
                    AccessPoint.radio_rx.labels(**radio_traffic_labels).set(value.rx)
                    AccessPoint.radio_tx.labels(**radio_traffic_labels).set(value.tx)
                    AccessPoint.radio_rx_pkts.labels(**radio_traffic_labels).set(value.rxPkts)
                    AccessPoint.radio_tx_pkts.labels(**radio_traffic_labels).set(value.txPkts)
                    AccessPoint.radio_rx_pkts_dropped.labels(**radio_traffic_labels).set(value.rxDropPkts)
                    AccessPoint.radio_tx_pkts_dropped.labels(**radio_traffic_labels).set(value.txDropPkts)
                    AccessPoint.radio_rx_pkts_error.labels(**radio_traffic_labels).set(value.rxErrPkts)
                    AccessPoint.radio_tx_pkts_error.labels(**radio_traffic_labels).set(value.txErrPkts)
                    AccessPoint.radio_rx_pkts_retry.labels(**radio_traffic_labels).set(value.rxRetryPkts)
                    AccessPoint.radio_tx_pkts_retry.labels(**radio_traffic_labels).set(value.txRetryPkts)
                    
            
    @staticmethod
    def __update_radio_stats(radio_stats: list[Omada.Model.Ports.AccessPointRadioStats]):
        for radio in radio_stats:
            radio_labels = AccessPoint.get_labels(radio,access_point_radio_labels)
            AccessPoint.radio_rx_rate.labels(**radio_labels).set(radio.rx)
            AccessPoint.radio_tx_rate.labels(**radio_labels).set(radio.tx)
            AccessPoint.radio_rx_retry_pkts_rate.labels(**radio_labels).set(radio.rxRetryPkts)
            AccessPoint.radio_tx_retry_pkts_rate.labels(**radio_labels).set(radio.txRetryPkts)