import requests


def get_request_result(url: str, response: requests.Response):

    response: dict = response.json()

    error_code: int = response.get("errorCode")

    if error_code != 0:
        print(
            response
        )
        message = response.get("msg")
        exc_message = "Call to {url} failed with code: {code}. {message}".format(
            url=url,
            code=error_code,
            message=message
        )
        raise Exception(exc_message)

    result = response.get("result")
    
    return result

