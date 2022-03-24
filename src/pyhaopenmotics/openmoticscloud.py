"""Module containing a OpenMoticsCloud Client for the OpenMotics API."""

from __future__ import annotations

import asyncio
import socket
from collections.abc import Awaitable, Callable
from typing import Any, Optional

import aiohttp
import async_timeout
import backoff
from aiohttp.client import ClientError
from yarl import URL

from .__version__ import __version__
from .cloud.groupactions import OpenMoticsGroupActions
from .cloud.installations import OpenMoticsInstallations
from .cloud.lights import OpenMoticsLights
from .cloud.models.installation import Installation
from .cloud.outputs import OpenMoticsOutputs
from .cloud.sensors import OpenMoticsSensors
from .cloud.shutters import OpenMoticsShutters
from .cloud.thermostats import OpenMoticsThermostats
from .const import CLOUD_API_URL
from .errors import OpenMoticsConnectionError, OpenMoticsConnectionTimeoutError


class OpenMoticsCloud:
    """Docstring."""

    _installations: Optional[list[Installation]] = None
    _close_session: bool = False

    def __init__(
        self,
        token: str,
        *,
        request_timeout: int = 8,
        session: Optional[aiohttp.client.ClientSession] | None = None,
        token_refresh_method: Optional[Callable[[], Awaitable[str]]] = None,
        installation_id: Optional[int] = None,
        base_url: str = CLOUD_API_URL,
    ) -> None:
        """Initialize connection with the OpenMotics Cloud API.

        Args:
            token: str
            request_timeout: int
            session: aiohttp.client.ClientSession
            token_refresh_method: token refresh function
            installation_id: int
            base_url: str
        """
        self.session = session
        self.token = None if token is None else token.strip()
        self._installation_id = installation_id
        self.base_url = base_url

        self.request_timeout = request_timeout
        self.token_refresh_method = token_refresh_method
        self.user_agent = f"PyHAOpenMotics/{__version__}"

        self.installations = OpenMoticsInstallations(self)
        self.outputs = OpenMoticsOutputs(self)
        self.groupactions = OpenMoticsGroupActions(self)
        self.lights = OpenMoticsLights(self)
        self.sensors = OpenMoticsSensors(self)
        self.shutters = OpenMoticsShutters(self)
        self.thermostats = OpenMoticsThermostats(self)

    @property
    def installation_id(self) -> int | None:
        """Get installation id.

        Returns:
            The installation id that will be used for this session.
        """
        return self._installation_id

    @installation_id.setter
    def installation_id(self, installation_id: int) -> None:
        """Set installation id.

        Args:
            installation_id: The installation id that will be used
                for this session.
        """
        self._installation_id = installation_id

    @backoff.on_exception(
        backoff.expo, OpenMoticsConnectionError, max_tries=3, logger=None
    )
    async def _request(
        self,
        path: str,
        *,
        method: str = aiohttp.hdrs.METH_GET,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Make post request using the underlying httpx AsyncClient.

        with the default timeout of 15s. in case of retryable exceptions,
        requests are retryed for up to 10 times or 5 minutes.

        Args:
            path: path
            method: get of post
            params: dict
            **kwargs: extra args

        Returns:
            response json or text

        Raises:
            OpenMoticsConnectionError: An error occurred while communitcation with
                the OpenMotics API.
            OpenMoticsConnectionTimeoutError: A timeout occurred while communicating
                with the OpenMotics API.
        """
        if self.token_refresh_method is not None:
            self.token = await self.token_refresh_method()

        url = str(URL(f"{self.base_url}{path}"))

        if self.session is None:
            self.session = aiohttp.ClientSession()
            self._close_session = True

        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

        if params:
            for key, value in params.items():
                if isinstance(value, bool):
                    params[key] = str(value).lower()

        try:
            async with async_timeout.timeout(self.request_timeout):
                resp = await self.session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    **kwargs,
                )

            resp.raise_for_status()

        except asyncio.TimeoutError as exception:
            raise OpenMoticsConnectionTimeoutError(
                "Timeout occurred while connecting to OpenMotics API"
            ) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            raise OpenMoticsConnectionError(
                "Error occurred while communicating with OpenMotics API."
            ) from exception

        if "application/json" in resp.headers.get("Content-Type", ""):
            response_data = await resp.json()
            return response_data

        return await resp.text()

    async def get(self, path: str, **kwargs: Any) -> Any:
        """Make get request using the underlying aiohttp.ClientSession.

        Args:
            path: string
            **kwargs: any

        Returns:
            response json or text
        """
        response = await self._request(
            path,
            method=aiohttp.hdrs.METH_GET,
            **kwargs,
        )
        return response

    async def post(self, path: str, **kwargs: Any) -> Any:
        """Make get request using the underlying aiohttp.ClientSession.

        Args:
            path: path
            **kwargs: extra args

        Returns:
            response json or text
        """
        response = await self._request(
            path,
            method=aiohttp.hdrs.METH_POST,
            **kwargs,
        )
        return response

    async def subscribe_webhook(self) -> None:
        """Register a webhook with OpenMotics for live updates.

        """
        # Register webhook
        await self._request(
            "/ws/events",
            method=aiohttp.hdrs.METH_POST,
            data={
                "type": "ACTION",
                "data": {
                    "action": "set_subscription",
                    "types": [
                        "OUTPUT_CHANGE",
                        "SENSOR_CHANGE",
                        "SHUTTER_CHANGE",
                        "THERMOSTAT_CHANGE",
                        "THERMOSTAT_GROUP_CHANGE",
                        "VENTILATION_CHANGE",
                    ],
                    "installation_ids": [self.installation_id],
                },
            },
        )

    async def unsubscribe_webhook(self) -> None:
        """Delete all webhooks for this application ID."""
        await self._request(
            "/ws/events",
            method=aiohttp.hdrs.METH_DELETE,
        )

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> OpenMoticsCloud:
        """Async enter.

        Returns:
            OpenMoticsCloud: The OpenMoticsCloud object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.

        Args:
            *_exc_info: Exec type.
        """
        await self.close()
