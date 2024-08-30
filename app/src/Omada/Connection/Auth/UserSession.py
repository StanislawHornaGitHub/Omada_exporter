from dataclasses import dataclass, field
import os
import requests
import datetime
from requests.cookies import RequestsCookieJar


@dataclass
class UserSession:
    username: str = field(init=True)
    password: str = field(init=True)
    omada_cid: str = field(init=True)

    session: requests.Session = field(init=False)

    __login_result: str = field(init=False)
    __base_url: str = field(init=False)
    __is_logged_in_endpoint: str = field(
        init=False, default="{base_url}/api/v2/loginStatus"
    )
    __login_endpoint: str = field(
        init=False, default="{base_url}/{omadacId}/api/v2/login"
    )
    __logout_endpoint: str = field(
        init=False, default="{base_url}/{omadacId}/api/v2/logout"
    )

    def __post_init__(self):
        self.session = requests.Session()
        self.session.cookies = RequestsCookieJar()
        self.__base_url = os.getenv("BASE_URL")
        self.login()

    def __del__(self):
        self.__logout()

    def is_logged_in(self):
        url = self.__is_logged_in_endpoint.format(
            base_url=self.__base_url
        )
        try:
            response: dict = self.session.get(
                url=url,
                params={
                    "_t": int(datetime.datetime.now().timestamp() * 1000)
                }
            ).json()
        except:
            return False

        result: dict = response.get("result")

        return result.get("login")

    def login(self):
        url = self.__login_endpoint.format(
            base_url=self.__base_url,
            omadacId=self.omada_cid
        )

        response = self.session.post(
            url,
            json={'username': self.username, 'password': self.password}
        )
        self.__login_result = response.json()
        self.session.headers.update(
            {
                "Csrf-Token":  self.__login_result["result"]['token'],
            }
        )

    def __logout(self):
        url = self.__logout_endpoint.format(
            base_url=self.__base_url,
            omadacId=self.omada_cid
        )
        t = self.session.post(
            url
        )

        result = t.json()
        return result

    def get_session(self) -> requests.Session:
        if self.is_logged_in() is not True:
            self.login()
        return self.session
