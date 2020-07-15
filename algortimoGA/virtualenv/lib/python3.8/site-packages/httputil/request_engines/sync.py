"""Synchronous request engine."""

__author__ = 'vovanec@gmail.com'


import requests.adapters
import requests.exceptions
import requests.models
import time

from .base import BaseRequestEngine
from .errors import ClientError
from .errors import CommunicationError
from .errors import MalformedResponse
from .errors import ServerError


class SyncRequestEngine(BaseRequestEngine):

    """Synchronous request engine.

    Uses requests module to make HTTP requests.

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

    def _request(self, url, *,
                 method='GET', headers=None, data=None, result_callback=None):
        """Perform synchronous request.

        :param str url: request URL.
        :param str method: request method.
        :param object data: JSON-encodable object.
        :param object -> object result_callback: result callback.

        :rtype: dict
        :raise: APIError
        """

        retries_left = self._conn_retries

        while True:
            s = self._make_session()
            try:
                cert = None
                if self._client_cert and self._client_key:
                    cert = (self._client_cert, self._client_key)
                elif self._client_cert:
                    cert = self._client_cert

                if self._verify_cert:
                    verify = True
                    if self._ca_certs:
                        verify = self._ca_certs
                else:
                    verify = False

                auth = None
                if self._username and self._password:
                    auth = (self._username, self._password)

                response = s.request(method, url, data=data,
                                     timeout=self._connect_timeout,
                                     cert=cert,
                                     headers=headers,
                                     verify=verify,
                                     auth=auth)
                """:type: requests.models.Response
                """
                if 400 <= response.status_code < 500:
                    raise ClientError(
                        response.status_code, response.content)
                elif response.status_code >= 500:
                    raise ServerError(
                        response.status_code, response.content)

                try:
                    if result_callback:
                        return result_callback(response.content)
                except (ValueError, TypeError) as err:
                    raise MalformedResponse(err) from None

                return response.content

            except (requests.exceptions.RequestException,
                    requests.exceptions.BaseHTTPError) as exc:
                if self._conn_retries is None or retries_left <= 0:
                    raise CommunicationError(exc) from None
                else:
                    retries_left -= 1
                    retry_in = (self._conn_retries - retries_left) * 2
                    self._log.warning('Server communication error: %s. '
                                      'Retrying in %s seconds.', exc, retry_in)
                    time.sleep(retry_in)
                    continue
            finally:
                s.close()

    @staticmethod
    def _make_session():
        """Create session object.

        :rtype: requests.Session
        """

        sess = requests.Session()
        sess.mount('http://', requests.adapters.HTTPAdapter(max_retries=False))
        sess.mount('https://', requests.adapters.HTTPAdapter(max_retries=False))

        return sess
