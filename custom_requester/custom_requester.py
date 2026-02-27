import json
import logging
import os

import requests

from constants.api_constants import HEADERS


class UnexpectedStatusCode(Exception):
    """Выбрасывается, когда статус ответа не совпадает с ожидаемым."""
    pass


class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    Инкапсулирует работу с requests, логирование и проверку статус-кодов.
    """

    def __init__(self, session: requests.Session, base_url: str):
        """
       Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
       Инкапсулирует работу с requests, логирование и проверку статус-кодов.
       """
        self.session = session
        self.base_url = base_url.rstrip('/')
        self.session.headers.update(HEADERS)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
            self,
            method: str,
            endpoint: str,
            data=None,
            params=None,
            expected_status=200,
            need_logging: bool = True,
            timeout: int = 15,
    ) -> requests.Response:
        """
        Универсальный метод для отправки запросов.

        :param method: HTTP метод (GET, POST, PUT, DELETE и т.д.).
        :param endpoint: Эндпоинт (например, "/login").
        :param data: Тело запроса (JSON).
        :param params: Query-параметры.
        :param expected_status: Ожидаемый статус-код или набор кодов.
        :param need_logging: Логировать ли запрос и ответ.
        :param timeout: Таймаут запроса в секундах.
        :return: requests.Response
        """

        url = f'{self.base_url}{endpoint}'
        response = self.session.request(
            method=method.upper(),
            url=url,
            json=data,
            params=params,
            timeout=timeout,
        )

        if need_logging:
            self.log_request_and_response(response)

        if isinstance(expected_status, (list, tuple, set)):
            ok = response.status_code in expected_status
        else:
            ok = response.status_code == expected_status

        if not ok:
            raise UnexpectedStatusCode(
                f"{method.upper()} {url} -> {response.status_code}, "
                f"expected {expected_status}\n{response.text}"
            )

        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.send_request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.send_request('POST', endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self.send_request('PATCH', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.send_request('DELETE', endpoint, **kwargs)

    def log_request_and_response(self, response: requests.Response):
        """
        Логирование запросов и ответов в формате, близком к curl.
        """
        try:
            request = response.request

            GREEN = "\033[32m"
            RED = "\033[31m"
            RESET = "\033[0m"

            headers = " \\\n".join(
                [f"-H '{h}: {v}'" for h, v in request.headers.items()]
            )

            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, "body") and request.body:
                if isinstance(request.body, bytes):
                    body_str = request.body.decode("utf-8")
                else:
                    body_str = str(request.body)

                if body_str != "{}":
                    body = f"-d '{body_str}' \n"

            # REQUEST
            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            # RESPONSE
            response_status = response.status_code
            is_success = response.ok
            response_data = response.text

            try:
                response_data = json.dumps(
                    json.loads(response.text),
                    indent=4,
                    ensure_ascii=False,
                )
            except json.JSONDecodeError:
                pass

            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not is_success:
                self.logger.info(
                    f"\tSTATUS_CODE: {RED}{response_status}{RESET}\n"
                    f"\tDATA: {RED}{response_data}{RESET}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {GREEN}{response_status}{RESET}\n"
                    f"\tDATA:\n{response_data}"
                )

            self.logger.info(f"{'=' * 80}\n")

        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")
