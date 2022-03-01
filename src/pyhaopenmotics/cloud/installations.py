"""Module containing the base of an installation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import parse_obj_as

from pyhaopenmotics.cloud.models.installation import Installation

if TYPE_CHECKING:
    from pyhaopenmotics.openmoticscloud import OpenMoticsCloud  # pylint: disable=R0401


class OpenMoticsInstallations:  # noqa: SIM119
    """Object holding information of the OpenMotics installation.

    All actions related to Installations or a specific Installation.
    """

    def __init__(self, omcloud: OpenMoticsCloud) -> None:
        """Init the installations object.

        Args:
            omcloud: OpenMoticsCloud
        """
        self._omcloud = omcloud

    async def get_all(  # noqa: A003
        self,
        installation_filter: str | None = None,
    ) -> list[Installation]:
        """List all Installation objects.

        Args:
            installation_filter: str

        Returns:
            all installations objects

        Optional filter (URL encoded JSON).
            * size: When the size filter is specified, when specified
            the matching Image metadata will be included in the response,
            if any. Possible values: SMALL|MEDIUM|ORIGINAL
            * gateways:
                gateway_model: openmotics|somfy|sense|healthbox3
            * openmotics:
                platform: CLASSIC|CORE|CORE_PLUS|ESAFE

        """
        path = "/base/installations"
        if installation_filter:
            query_params = {"filter": installation_filter}
            body = await self._omcloud.get(
                path=path,
                params=query_params,
            )
        else:
            body = await self._omcloud.get(path)

        return parse_obj_as(list[Installation], body["data"])

    async def get_by_id(
        self,
        installation_id: int,
    ) -> Installation:
        """Get a single Installation object.

        Args:
            installation_id: int

        Returns:
            a single Installation object

        """
        path = f"/base/installations/{installation_id}"
        body = await self._omcloud.get(path)

        return Installation.parse_obj(body["data"])
