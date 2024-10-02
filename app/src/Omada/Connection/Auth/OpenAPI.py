import datetime
import requests
from src.Omada.Connection.Auth.BaseAuth import BaseAuth
from src.Observability.Log.logger import logger
import src.Config as Config

class OpenAPI(BaseAuth):
    __client_id: str = Config.OMADA_CLIENT_ID
    __client_secret: str = Config.OMADA_CLIENT_SECRET
    __path_get_token: str = "/openapi/authorize/token?grant_type=client_credentials"
    __path_refresh_token: str = "/openapi/authorize/token?client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token"
    __accessToken: str = None
    __refreshToken: str = None

    expires_at: datetime.datetime = None

    @staticmethod
    def get_token() -> str:
        
        if not OpenAPI.__accessToken:
            logger.warning("Access Token not found")
            OpenAPI.request_token()
            return OpenAPI.__accessToken

        if not OpenAPI.__is_token_expired():
            logger.info("Found valid access token for OpenAPI")
            return OpenAPI.__accessToken

        logger.warning("Access Token is expired")
        OpenAPI.refresh_token()
        return OpenAPI.__accessToken

    @staticmethod
    def __is_token_expired() -> bool:
        return ((OpenAPI.expires_at - datetime.timedelta(seconds=300)) < datetime.datetime.now())

    @staticmethod
    def __set_expiration_time(expires_in: int) -> None:

        OpenAPI.expires_at = (
            datetime.datetime.now() +
            datetime.timedelta(seconds=expires_in)
        )

    @staticmethod
    def request_token() -> None:
        logger.info("Requesting new OpenAPI Access Token")
        url: str = OpenAPI.get_url(OpenAPI.__path_get_token)
        body = {
            "omadacId": OpenAPI.omada_cid,
            "client_id": OpenAPI.__client_id,
            "client_secret": OpenAPI.__client_secret
        }
        try:
            response: requests.Response = requests.post(url=url, json=body)

            code, result, msg = BaseAuth.get_result(response)
        except Exception as e:
            logger.exception(e, exc_info=True)
        
        
        if code != 0:
            logger.exception(msg, exc_info=True)

        OpenAPI.__set_token_details(result)
        logger.info("Access Token requested successfully")

    @staticmethod
    def refresh_token() -> None:
        logger.info("Refreshing OpenAPI Access Token")
        url: str = OpenAPI.get_url(
            OpenAPI.__path_refresh_token,
            {
                "client_id": OpenAPI.__client_id,
                "client_secret": OpenAPI.__client_secret,
                "refresh_token": OpenAPI.__refreshToken
            }
        )
        try:
            response: requests.Request = requests.post(url)

            code, result, msg = BaseAuth.get_result(response)
        except Exception as e:
            logger.exception(e,exc_info=True)

        if code == 0:
            OpenAPI.__set_token_details(result)
            logger.info("OpenAPI token refreshed successfully")
        else:
            logger.warning(msg, exc_info=True)
            OpenAPI.request_token()

    @staticmethod
    def __set_token_details(result: dict):
        OpenAPI.__accessToken = result.get("accessToken")
        OpenAPI.__refreshToken = result.get("refreshToken")
        OpenAPI.__set_expiration_time(result.get("expiresIn"))

    class TokenException(Exception):
        OmadaErrorCodes: list[int] = [
            -44109,
            -44110,
            -44112,
            -44113,
        ]
