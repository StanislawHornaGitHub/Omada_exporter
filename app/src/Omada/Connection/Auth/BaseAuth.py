import requests
import src.Config as Config


class BaseAuth:
    __base_url: str = Config.BASE_URL
    omada_cid: str = None

    @staticmethod
    def get_url(path: str, args: dict = {}) -> str:
        url: str = "{base_url}{path}"
        path: str = path.format(**args)
        return url.format(base_url=BaseAuth.__base_url, path=path)

    @staticmethod
    def get_result(response: requests.Response) -> tuple[str, dict]:
        try:
            response_json: dict = response.json()
        except:
            response_json: dict = {}
            response_json["errorCode"] = -1
            response_json["msg"] = "Failed to parse JSON"

        status_code: int = response_json.get("errorCode", 1)

        return (
            status_code,
            response_json.get("result", None),
            response_json.get("msg", None),
        )
