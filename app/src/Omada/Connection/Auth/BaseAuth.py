import os
from dotenv import load_dotenv

load_dotenv()

class BaseAuth:
    __base_url: str = os.getenv("BASE_URL")
    omada_cid: str = None
    
    @staticmethod
    def get_url(path: str, args: dict ={}) -> str:
        url: str = "{base_url}{path}"
        path: str = path.format(
            **args
        )
        return url.format(
            base_url=BaseAuth.__base_url,
            path=path
        )