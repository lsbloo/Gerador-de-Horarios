"""Request engine errors."""

__author__ = 'vovanec@gmail.com'

import http.client


class RequestError(Exception):

    """Base request error."""


class CommunicationError(RequestError):

    """Communication problem with server."""


class MalformedResponse(RequestError):

    """Server responded with data which client could not understand."""


class HTTPError(RequestError):

    """Server returned HTTP error."""

    def __init__(self, code, response_body=None):
        """Constructor.

        :param int code: HTTP code.
        :param str response_body: HTTP response body.
        """

        self.code = code
        self.body = response_body

        super().__init__('HTTP %d: %s' % (
            self.code, self.body or http.client.responses.get(code, 'Unknown')))


class ClientError(HTTPError):

    """Client side error."""


class ServerError(HTTPError):

    """Server side error."""
