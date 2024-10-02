import atexit
import requests
import datetime
import src.Omada.Connection.Auth as Auth
import src.Config as Config
from src.Observability import *


tracer = trace.get_tracer("Request-tracer")


class Request:

    site_id: str = None
    omada_cid: str = None
    controller_version: str = None
    api_version: str = None

    __user_session: Auth.UserSession = None

    __base_url: str = Config.BASE_URL
    __verify_certificate: bool = Config.VERIFY_CERTIFICATE

    __page_size: int = 100
    __web_api_retry_limit: int = 2
    __open_api_retry_limit: int = 2

    @staticmethod
    @tracer.start_as_current_span("Request.get")
    def get(path: str, arguments: dict = {}, include_auth: bool = True, include_params: bool = True, page: int = 1):
        extra_data = {
            "path": path,
            "arguments": arguments,
            "include_auth": include_auth,
            "include_params": include_params,
            "page": page
        }

        current_span = get_current_span()

        logger.info("Get method invoked", extra=extra_data)

        current_span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
        current_span.set_attribute(SpanAttributes.URL_PATH, path)

        url = Request.__get_url(path, arguments)
        extra_data["url"] = url

        logger.info("Url generated", extra=extra_data)
        current_span.set_attribute(SpanAttributes.URL_FULL, url)

        if path.startswith("/api/") and path != "/api/info":

            response = Request.get_method_web_api(url)
        elif path.startswith("/openapi/") or path == "/api/info":
            response = Request.get_method_openapi(
                url, include_auth, include_params
            )

        set_current_span_status()
        return response

    @staticmethod
    @tracer.start_as_current_span("Request.get_method_web_api")
    def get_method_web_api(url: str) -> requests.Response:
        extra_data = {
            "url": url
        }
        logger.info("Get method on Web API invoked", extra=extra_data)

        current_span = get_current_span()
        current_span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
        current_span.set_attribute(SpanAttributes.URL_FULL, url)

        retry_counter: int = 0

        while (retry_counter < Request.__web_api_retry_limit):
            current_span.set_attribute(
                SpanAttributes.HTTP_RETRY_COUNT, retry_counter
            )

            retry_counter = retry_counter + 1
            session = Request.__user_session.get_session()
            try:
                response = session.get(
                    url=url,
                    params={
                        "_t": Request.__get_timestamp()
                    }
                )
            except Exception as e:
                logger.exception(e, exc_info=True, extra=extra_data)
            else:
                current_span.set_attribute(
                    SpanAttributes.HTTP_STATUS_CODE, response.status_code
                )

            code, result, msg = Request.__get_result(response)
            if code == 0:
                logger.info("Web API called successfully", extra=extra_data)
                break

            if code == -1:
                logger.warning(
                    "Web API call was not successful, trying to re-login", extra=extra_data
                )
                Request.__user_session.login()

        if code != 0:
            logger.exception(msg, exc_info=True, extra=extra_data)
            return None

        set_current_span_status()
        return result

    @staticmethod
    @tracer.start_as_current_span("Request.get_method_openapi")
    def get_method_openapi(
        url: str, include_auth: bool = True, include_params: bool = True, page: int = 1
    ) -> dict:
        extra_data = {
            "url": url,
            "include_auth": include_auth,
            "include_params": include_params,
            "page": page
        }
        logger.info("Get method on Open API invoked", extra=extra_data)

        current_span = get_current_span()
        current_span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
        current_span.set_attribute(SpanAttributes.URL_FULL, url)

        retry_counter: int = 0
        while (retry_counter < Request.__open_api_retry_limit):
            current_span.set_attribute(
                SpanAttributes.HTTP_RETRY_COUNT, retry_counter
            )

            retry_counter = retry_counter + 1

            headers = Request.__get_headers(include_auth)
            params = Request.__get_params(page, include_params)

            try:
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    verify=Request.__verify_certificate
                )
            except Exception as e:
                logger.exception(e, exc_info=True, extra=extra_data)
            else:
                current_span.set_attribute(
                    SpanAttributes.HTTP_STATUS_CODE, response.status_code
                )

            code, result, msg = Request.__get_result(response)

            if code == 0:
                logger.info("Open API called successfully", extra=extra_data)
                break
            elif code in Auth.OpenAPI.TokenException.OmadaErrorCodes:
                logger.warning(
                    "Open API call was not successful ({errCode}), trying, to request new token".format(
                        errCode=code
                    ),
                    extra=extra_data
                )
                Auth.OpenAPI.request_token()

        if code != 0:
            logger.exception(msg, exc_info=True, extra=extra_data)
            return None

        if Request.__has_data(result):
            logger.info("Result contains data", extra=extra_data)
            if not Request.__has_more_data_to_fetch(result):
                logger.info(
                    "Result has no more data to download, returning the result", extra=extra_data
                )
                current_span.set_status(status=trace.StatusCode(1))
                return result.get("data")

            logger.info("Result has more data to download", extra=extra_data)
            result = result.get("data")
            result += Request.get(
                url, include_auth, include_params, page+1
            )

        set_current_span_status()
        return result

    @staticmethod
    @tracer.start_as_current_span("Request.post")
    def post(path: str, arguments: dict = {}, body: dict = None):
        extra_data = {
            "path": path,
            "arguments": arguments,
            "body": body
        }
        logger.info("Post method invoked", extra=extra_data)
        current_span = get_current_span()
        current_span.set_attribute(SpanAttributes.HTTP_METHOD, "POST")
        current_span.set_attribute(SpanAttributes.URL_PATH, path)

        try:
            url = Request.__get_url(path, arguments)
            extra_data["url"] = url
            logger.info("Url generated", extra=extra_data)
        except Exception as e:
            logger.exception(e, exc_info=True, extra=extra_data)

        current_span.set_attribute(SpanAttributes.URL_FULL, url)

        if path.startswith("/api/") and path != "/api/info":
            logger.info("Web API selected", exc_info=extra_data)
            response = Request.post_method_web_api(url, body)
        elif path.startswith("/openapi/") or path == "/api/info":
            logger.info("Open API selected", exc_info=extra_data)
            response = Request.post_method_openapi(url, body)

        set_current_span_status()
        return response

    @staticmethod
    @tracer.start_as_current_span("Request.post_method_openapi")
    def post_method_openapi(url: str, body: dict = None):
        extra_data = {
            "url": url,
            "body": body
        }
        logger.info("Post method on Open API invoked", extra=extra_data)
        current_span = get_current_span()
        current_span.set_attribute(SpanAttributes.HTTP_METHOD, "POST")
        current_span.set_attribute(SpanAttributes.URL_FULL, url)

        if body is not None:
            response = requests.post(
                url=url, json=body, verify=Request.__verify_certificate
            )
        else:
            response = requests.post(
                url=url, verify=Request.__verify_certificate
            )

        current_span.set_attribute(
            SpanAttributes.HTTP_STATUS_CODE, response.status_code
        )

        code, result, msg = Request.__get_result(response)

        if code != 0:
            logger.exception(msg, exc_info=True, extra=extra_data)
            return None

        set_current_span_status()
        return result

    @staticmethod
    @tracer.start_as_current_span("Request.post_method_web_api")
    def post_method_web_api(url, body):
        extra_data = {
            "url": url,
            "body": body
        }
        logger.info("Post method on Web API invoked", extra=extra_data)
        current_span = get_current_span()
        current_span.set_attribute(SpanAttributes.HTTP_METHOD, "POST")
        current_span.set_attribute(SpanAttributes.URL_FULL, url)

        session = Request.__user_session.get_session()
        response = session.post(
            url=url,
            json=body
        )

        current_span.set_attribute(
            SpanAttributes.HTTP_STATUS_CODE, response.status_code
        )

        code, result, msg = Request.__get_result(response)

        if code != 0:
            logger.exception(msg, exc_info=True, extra=extra_data)

        set_current_span_status()
        return result

    @staticmethod
    def __get_url(path: str, arguments: dict = {}) -> str:
        if path.startswith("/api/") and path != "/api/info":
            path = "/{omadacId}" + path

        arguments = {
            "omadacId": Request.omada_cid,
            "siteId": Request.site_id,
            **arguments
        }
        path: str = path.format(
            **arguments
        )
        return "{base}{endpoint_path}".format(
            base=Request.__base_url,
            endpoint_path=path
        )

    @staticmethod
    def __get_headers(include_auth_headers: bool = True) -> dict:
        if include_auth_headers:
            return {
                "Authorization": "AccessToken={token}".format(
                    token=Auth.OpenAPI.get_token()
                ),
                "content-type": "application/json"
            }
        return None

    @staticmethod
    def __get_params(page: int = 1, include_params: bool = True) -> dict:
        if include_params:
            return {
                "pageSize": Request.__page_size,
                "page": page
            }
        return None

    @staticmethod
    def __get_timestamp() -> int:
        return int(datetime.datetime.now().timestamp() * 1000)

    @staticmethod
    def __get_fetched_rows(result: dict) -> int:
        return result.get("currentPage") * result.get("currentSize")

    @staticmethod
    def __has_more_data_to_fetch(result: dict) -> bool:
        return (Request.__get_fetched_rows(result) < result.get("totalRows"))

    @staticmethod
    def __has_data(result: dict) -> bool:
        try:
            return ('data' in list(result.keys()))
        except:
            return False

    @staticmethod
    def __get_result(response: requests.Response) -> tuple[str, dict]:
        try:
            response_json: dict = response.json()
        except:
            response_json: dict = {}
            response_json["errorCode"] = -1
            response_json["msg"] = "Failed to parse JSON"

        status_code: int = response_json.get("errorCode", 1)

        return status_code, response_json.get("result", None), response_json.get("msg", None)

    @staticmethod
    @tracer.start_as_current_span("Request.init")
    def init() -> None:
        logger.info(
            "Requests module initialization started"
        )
        get_current_span()
        error: bool = False

        try:
            api_info = Request.get(
                "/api/info", include_auth=False, include_params=False
            )

        except Exception as e:
            error = True
            logger.exception(e, exc_info=True)
        else:
            logger.info(
                "Omada API info fetched successfully",
                exc_info={
                    "api_info": api_info
                }
            )

        try:
            Request.controller_version = api_info.get("controllerVer")
            Request.api_version = api_info.get("apiVer")
            Request.omada_cid = api_info.get("omadacId")
            Auth.OpenAPI.omada_cid = api_info.get("omadacId")
        except Exception as e:
            error = True
            logger.exception(e, exc_info=True)
        else:
            logger.info("Controller related data set")

        with tracer.start_as_current_span("UserSession.init"):
            try:
                Request.__user_session = Auth.UserSession(
                    username=Config.OMADA_USER,
                    password=Config.OMADA_USER_PASSWORD,
                    omada_cid=Request.omada_cid
                )
            except Exception as e:
                error = True
                logger.exception(e, exc_info=True)
            else:
                logger.info("UserSession created successfully")

        try:
            site = Request.get("/openapi/v1/{omadacId}/sites")
            Request.site_id = [
                entry.get("siteId")
                for entry in site
                if entry.get("name") == Config.SITE_NAME
            ][0]
        except Exception as e:
            error = True
            logger.exception(e, exc_info=True)
        else:
            logger.info(
                "Site {name} selected successfully ({site_id})".format(
                    name=Config.SITE_NAME,
                    site_id=Request.site_id
                ),
                exc_info={
                    "available_sites": site
                }
            )

        set_current_span_status(error)

    @staticmethod
    def close():
        del Request.__user_session


Request.init()
atexit.register(Request.close)
