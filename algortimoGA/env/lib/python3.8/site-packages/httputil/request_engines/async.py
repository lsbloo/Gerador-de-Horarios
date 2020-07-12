"""Asynchronous request engine."""

__author__ = 'vovanec@gmail.com'


from tornado import curl_httpclient
from tornado import gen
from tornado import httpclient

from .base import BaseRequestEngine
from .errors import ClientError
from .errors import CommunicationError
from .errors import MalformedResponse
from .errors import ServerError


# Configure async engine to use CURL client whenever possible.
httpclient.AsyncHTTPClient.configure(curl_httpclient.CurlAsyncHTTPClient)


class AsyncRequestEngine(BaseRequestEngine):

    """Asynchronous request engine.

    Uses Tornado asynchronous client to make HTTP requests.

    """

    def __init__(self, api_base_url, connect_timeout, request_timeout,
                 conn_retries, username=None, password=None,
                 client_cert=None, client_key=None, verify_cert=True,
                 ca_certs=None):
        """Constructor.

        :param str api_base_url: API base URL.
        :param int connect_timeout: connection timeout.
        :param int request_timeout: request timeout.
        :param int|None conn_retries: The number of retries on connection
               error. If None - no retries.
        :param str|None username: auth username.
        :param str|None password: auth password.
        :param str|None client_cert: client certificate.
        :param str|None client_key: client key.
        :param bool verify_cert: whether to verify server cert.
        :param str|None ca_certs: path to CA certificate chain.
        """

        super().__init__(
            api_base_url, connect_timeout, request_timeout, conn_retries,
            username=username, password=password,
            client_cert=client_cert, client_key=client_key,
            verify_cert=verify_cert, ca_certs=ca_certs)

        self._client = httpclient.AsyncHTTPClient()

    def _request(self, url, *,
                 method='GET', headers=None, data=None, result_callback=None):
        """Perform asynchronous request.

        :param str url: request URL.
        :param str method: request method.
        :param dict headers: request headers.
        :param object data: JSON-encodable object.
        :param object -> object result_callback: result callback.

        :rtype: dict
        :raise: APIError
        """

        request = self._prepare_request(url, method, headers, data)

        retries_left = self._conn_retries

        while True:
            try:
                response = yield self._client.fetch(request)
                try:
                    if result_callback:
                        return result_callback(response.body)
                except (ValueError, TypeError) as err:
                    raise MalformedResponse(err) from None

                return response.body

            except httpclient.HTTPError as err:
                resp_body = err.response.body \
                    if err.response is not None else None
                if err.code == 599:
                    if self._conn_retries is None or retries_left <= 0:
                        raise CommunicationError(err) from None
                    else:
                        retries_left -= 1
                        retry_in = (self._conn_retries - retries_left) * 2
                        self._log.warning('Server communication error: %s. '
                                          'Retrying in %s seconds.', err,
                                          retry_in)
                        yield gen.sleep(retry_in)
                        continue
                elif 400 <= err.code < 500:
                    raise ClientError(err.code, resp_body) from None

                raise ServerError(err.code, resp_body) from None

    def _prepare_request(self, url, method, headers, data):
        """Prepare HTTP request.

        :param str url: request URL.
        :param str method: request method.
        :param dict headers: request headers.
        :param object data: JSON-encodable object.

        :rtype: httpclient.HTTPRequest

        """

        request = httpclient.HTTPRequest(
            url=url, method=method, headers=headers, body=data,
            connect_timeout=self._connect_timeout,
            request_timeout=self._request_timeout,
            auth_username=self._username, auth_password=self._password,
            client_cert=self._client_cert, client_key=self._client_key,
            ca_certs=self._ca_certs, validate_cert=self._verify_cert)

        return request
