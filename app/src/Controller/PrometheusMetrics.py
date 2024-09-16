import src.Prometheus as Prometheus
import src.Omada as Omada


class PrometheusMetrics:

    @staticmethod
    def update():
        PrometheusMetrics.__update_switch_metrics()
        PrometheusMetrics.__update_router_metrics()
        PrometheusMetrics.__update_access_point_metrics()

    @staticmethod
    def __update_switch_metrics():
        devices = Omada.Controller.Switch.get_info()
        ports = Omada.Controller.Switch.get_port_info()
        Prometheus.Switch.update_metrics(devices, ports)

    @staticmethod
    def __update_router_metrics():
        devices = Omada.Controller.Router.get_info()
        ports = Omada.Controller.Router.get_port_info()
        Prometheus.Router.update_metrics(devices, ports)

    @staticmethod
    def __update_access_point_metrics():
        devices = Omada.Controller.AccessPoint.get_info()
        ports = Omada.Controller.AccessPoint.get_port_info()
        radios = Omada.Controller.AccessPoint.get_radio_info()
        Prometheus.AccessPoint.update_metrics(devices, ports, radios)
