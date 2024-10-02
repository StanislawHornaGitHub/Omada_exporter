import src.Prometheus as Prometheus
import src.Omada as Omada
from src.Observability import *

tracer = trace.get_tracer("PrometheusMetricsController-tracer")


class PrometheusMetrics:

    registry = Prometheus.exporter_registry

    @staticmethod
    @tracer.start_as_current_span("PrometheusMetrics.update")
    def update():

        logger.info("PrometheusMetrics update invoked")

        get_current_span()
        errors: set[bool] = set()

        errors.add(
            not PrometheusMetrics.__update_switch_metrics()
        )
        errors.add(
            not PrometheusMetrics.__update_router_metrics()
        )
        errors.add(
            not PrometheusMetrics.__update_access_point_metrics()
        )

        if False not in errors:
            raise Exception("Failed to update Prometheus metrics")

        set_current_span_status(errors)
        return None

    @staticmethod
    @tracer.start_as_current_span("PrometheusMetrics.__update_switch_metrics")
    def __update_switch_metrics() -> bool:

        get_current_span()
        errors: set[bool] = set()

        try:
            devices = Omada.Controller.Switch.get_info()
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("Switch data fetched successfully")

        try:
            ports = Omada.Controller.Switch.get_port_info()
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("Switch ports data fetched successfully")

        try:
            Prometheus.Switch.update_metrics(devices, ports)
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("Switch metrics updated successfully")

        if False not in errors:
            return False

        set_current_span_status(errors)
        return True

    @staticmethod
    @tracer.start_as_current_span("PrometheusMetrics.__update_router_metrics")
    def __update_router_metrics() -> bool:

        get_current_span()
        errors: set[bool] = set()

        try:
            devices = Omada.Controller.Router.get_info()
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("Router data fetched successfully")

        try:
            ports = Omada.Controller.Router.get_port_info()
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("Router ports data fetched successfully")

        try:
            Prometheus.Router.update_metrics(devices, ports)
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("Router metrics updated successfully")

        if False not in errors:
            return False

        set_current_span_status(errors)
        return True

    @staticmethod
    @tracer.start_as_current_span("PrometheusMetrics.__update_access_point_metrics")
    def __update_access_point_metrics() -> bool:

        get_current_span()
        errors: set[bool] = set()

        try:
            devices = Omada.Controller.AccessPoint.get_info()
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("AccessPoint data fetched successfully")

        try:
            ports = Omada.Controller.AccessPoint.get_port_info()
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("AccessPoint port data fetched successfully")

        try:
            radios = Omada.Controller.AccessPoint.get_radio_info()
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("AccessPoint radio data fetched successfully")

        try:
            Prometheus.AccessPoint.update_metrics(devices, ports, radios)
        except Exception as e:
            errors.add(True)
            logger.exception(e, exc_info=True)
        else:
            errors.add(False)
            logger.info("AccessPoint radio metrics updated successfully")

        if False not in errors:
            return False

        set_current_span_status(errors)
        return True
