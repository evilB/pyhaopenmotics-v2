"""Module HTTP communication with the OpenMotics API."""

from pyhaopenmotics.cloud.models import Installation

from .errors import (
    OpenMoticsConnectionError,
    OpenMoticsConnectionTimeoutError,
    OpenMoticsError,
)
from .helpers import get_ssl_context
from .localgateway import LocalGateway
from .openmoticscloud import OpenMoticsCloud

__all__ = [
    "OpenMoticsCloud",
    "LocalGateway",
    "OpenMoticsError",
    "OpenMoticsConnectionError",
    "OpenMoticsConnectionTimeoutError",
    "Installation",
    "get_ssl_context",
]
