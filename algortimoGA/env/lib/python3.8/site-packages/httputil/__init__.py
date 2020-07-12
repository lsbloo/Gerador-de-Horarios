"""Utility functions to deal with HTTP stream: dechunking and decompressing
body etc.
"""

__author__ = 'vovanec@gmail.com'


from .httputil import BodyStreamError
from .httputil import DecompressError
from .httputil import DechunkError

from .httputil import BZIP2
from .httputil import DEFLATE
from .httputil import GZIP

from .httputil import read_body_stream
