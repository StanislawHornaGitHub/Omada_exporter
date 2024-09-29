import os
import atexit
from dotenv import load_dotenv
import requests
import datetime
import src.Omada.Connection.Auth as Auth

load_dotenv()


class Request:

    site_id: str = None
    omada_cid: str = None
    controller_version: str = None
    api_version: str = None

    __user_session: Auth.UserSession = None

    __base_url: str = os.getenv("BASE_URL")
    __verify_certificate: bool = os.getenv("VERIFY_CERTIFICATE")

    __page_size: int = 100
    __web_api_retry_limit: int = 2
    __open_api_retry_limit: int = 2

    @staticmethod
    def get(path: str, arguments: dict = {}, include_auth: bool = True, include_params: bool = True, page: int = 1):
        url = Request.__get_url(path, arguments)

        if path.startswith("/api/") and path != "/api/info":
            return Request.get_method_web_api(url)
        elif path.startswith("/openapi/") or path == "/api/info":
            return Request.get_method_openapi(url, include_auth, include_params)

    @staticmethod
    def get_method_web_api(url: str) -> requests.Response:

        retry_counter: int = 0

        while (retry_counter < Request.__web_api_retry_limit):
            retry_counter = retry_counter + 1
            session = Request.__user_session.get_session()
            response = session.get(
                url=url,
                params={
                    "_t": Request.__get_timestamp()
                }
            )

            code, result, msg = Request.__get_result(response)
            if code == 0:
                break

            if code == -1:
                Request.__user_session.login()

        if code != 0:
            raise Exception(msg)

        return result

    @staticmethod
    def get_method_openapi(
        url: str, include_auth: bool = True, include_params: bool = True, page: int = 1
    ) -> dict:

        retry_counter: int = 0
        while (retry_counter < Request.__open_api_retry_limit):
            retry_counter = retry_counter + 1

            headers = Request.__get_headers(include_auth)
            params = Request.__get_params(page, include_params)

            response = requests.get(
                url,
                headers=headers,
                params=params,
                verify=Request.__verify_certificate
            )

            code, result, msg = Request.__get_result(response)

            if code == 0:
                break
            elif code in Auth.OpenAPI.TokenException.OmadaErrorCodes:
                Auth.OpenAPI.request_token()

        if code != 0:
            raise Exception(msg)

        if Request.__has_data(result):
            if not Request.__has_more_data_to_fetch(result):
                return result.get("data")

            result = result.get("data")
            result += Request.get(
                url, include_auth, include_params, page+1
            )

        return result

    @staticmethod
    def post(path: str, arguments: dict = {}, body: dict = None):
        url = Request.__get_url(path, arguments)

        if path.startswith("/api/") and path != "/api/info":
            return Request.__post_method_web_api(url, body)
        elif path.startswith("/openapi/") or path == "/api/info":
            return Request.__post_method_openapi(url, body)

    @staticmethod
    def __post_method_openapi(url: str, body: dict = None):
        if body is not None:
            response = requests.post(
                url=url, json=body, verify=Request.__verify_certificate
            )
        else:
            response = requests.post(
                url=url, verify=Request.__verify_certificate
            )

        code, result, msg = Request.__get_result(response)

        if code != 0:
            raise Exception(msg)

        return result

    @staticmethod
    def __post_method_web_api(url, body):

        session = Request.__user_session.get_session()
        response = session.post(
            url=url,
            json=body
        )

        code, result, msg = Request.__get_result(response)

        if code != 0:
            raise Exception(msg)

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
    def init() -> None:
        api_info = Request.get(
            "/api/info", include_auth=False, include_params=False
        )
        Request.controller_version = api_info.get("controllerVer")
        Request.api_version = api_info.get("apiVer")
        Request.omada_cid = api_info.get("omadacId")
        Auth.OpenAPI.omada_cid = api_info.get("omadacId")

        Request.__user_session = Auth.UserSession(
            username=os.getenv("OMADA_USER"),
            password=os.getenv("OMADA_USER_PASSWORD"),
            omada_cid=Request.omada_cid
        )

        site = Request.get("/openapi/v1/{omadacId}/sites")
        Request.site_id = [
            entry.get("siteId")
            for entry in site
            if entry.get("name") == os.getenv("SITE_NAME")
        ][0]

    @staticmethod
    def close():
        del Request.__user_session


Request.init()
atexit.register(Request.close)
