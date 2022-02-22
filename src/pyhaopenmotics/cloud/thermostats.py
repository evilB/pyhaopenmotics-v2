"""Module containing the base of an output."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import parse_obj_as

from pyhaopenmotics.cloud.models.thermostat import ThermostatGroup, ThermostatUnit

if TYPE_CHECKING:
    from pyhaopenmotics.openmoticscloud import OpenMoticsCloud  # pylint: disable=R0401


class OpenMoticsThermostats:  # noqa: SIM119
    """Object holding information of the OpenMotics thermostats.

    All actions related to thermostats or a specific thermostat.
    """

    def __init__(self, omcloud: OpenMoticsCloud) -> None:
        """Init the installations object.

        Args:
            _omcloud: _omcloud
        """
        self._omcloud = omcloud

        self.groups = OpenMoticsThermostatGroups(self._omcloud)
        self.units = OpenMoticsThermostatUnits(self._omcloud)

    async def set_mode(
        self,
        mode: str ,
    ) -> dict[str, Any]:
        """Set a mode to all Groups the User has access to

        Args:
            mode: "HEATING|COOLING"

        Returns:
            Returns something
        """

        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/mode"
        payload = {"mode": mode}
        return await self._omcloud.post(path, json=payload)

    async def set_state(
        self,
        state: str ,
    ) -> dict[str, Any]:
        """Set a mode to all Groups the User has access to

        Args:
            state: "ON|OFF"

        Returns:
            Returns something
        """

        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/state"
        payload = {"state": state}
        return await self._omcloud.post(path, json=payload)


class OpenMoticsThermostatGroups:  # noqa: SIM119
    """Object holding information of the OpenMotics thermostats.

    All actions related to thermostats or a specific thermostat.
    """

    def __init__(self, _omcloud: OpenMoticsCloud) -> None:
        """Init the installations object.

        Args:
            _omcloud: _omcloud
        """
        self._omcloud = _omcloud



    async def get_all(  # noqa: A003
        self,
    ) -> list[ThermostatGroup]:
        """Get a list of all thermostatgroup objects.

        Args:

        Returns:
            Dict with all thermostats
        """
        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/groups"

        body = await self._omcloud.get(path)

        return parse_obj_as(list[ThermostatGroup], body["data"])

    async def get_by_id(
        self,
        thermostatgroup_id: int,
    ) -> ThermostatGroup:
        """Get thermostatgroup_id by id.

        Args:
            thermostatgroup_id: int

        Returns:
            Returns a thermostatgroup_id with id
        """
        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/groups/{thermostatgroup_id}"
        body = await self._omcloud.get(path)

        return ThermostatGroup.parse_obj(body["data"])

    async def set_mode(
        self,
        thermostatgroup_id: int,
        mode: str ,
    ) -> dict[str, Any]:
        """Turn on a specified Output object.

        Args:
            thermostatgroup_id: int
            mode: "HEATING|COOLING"

        Returns:
            Returns a output with id
        """

        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/groups/{thermostatgroup_id}/mode"
        payload = {"mode": mode}
        return await self._omcloud.post(path, json=payload)

class OpenMoticsThermostatUnits:  # noqa: SIM119
    """Object holding information of the OpenMotics thermostats.

    All actions related to thermostats or a specific thermostat.
    """

    def __init__(self, _omcloud: OpenMoticsCloud) -> None:
        """Init the installations object.

        Args:
            _omcloud: _omcloud
        """
        self._omcloud = _omcloud



    async def get_all(  # noqa: A003
        self,
    ) -> list[ThermostatUnit]:
        """Get a list of all thermostatunit objects.

        Args:

        Returns:
            Dict with all thermostatunits
        """
        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/units"

        body = await self._omcloud.get(path)

        print(body["data"])

        return parse_obj_as(list[ThermostatUnit], body["data"])

    async def get_by_id(
        self,
        thermostatunit_id: int,
    ) -> ThermostatUnit:
        """Get thermostatgroup_id by id.

        Args:
            thermostatunit_id: int

        Returns:
            Returns a thermostatunit with id
        """
        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/units/{thermostatunit_id}"
        body = await self._omcloud.get(path)

        return ThermostatUnit.parse_obj(body["data"])

    async def set_state(
        self,
        thermostatunit_id: int,
        state: str ,
    ) -> dict[str, Any]:
        """Set state of a thermostatunit.

        Args:
            thermostatunit_id: int
            state: "ON|OFF"

        Returns:
            Returns a thermostatunit with id
        """

        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/units/{thermostatunit_id}/state"
        payload = {"state": state}
        return await self._omcloud.post(path, json=payload)

    async def set_temperature(
        self,
        thermostatunit_id: int,
        temperature: float ,
    ) -> dict[str, Any]:
        """Set temperature of a thermostatunit.

        Args:
            thermostatunit_id: int
            temperature: float

        Returns:
            Returns a thermostatunit with id
        """

        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/units/{thermostatunit_id}/setpoint"
        payload = {"temperature": temperature}
        return await self._omcloud.post(path, json=payload)

    async def set_preset(
        self,
        thermostatunit_id: int,
        preset: str,
    ) -> dict[str, Any]:
        """Set preset of a thermostatunit.

        Args:
            thermostatunit_id: int
            preset: "AUTO|AWAY|PARTY|VACATION"

        Returns:
            Returns a thermostatunit with id
        """

        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/units/{thermostatunit_id}/preset"
        payload = {"preset": preset}
        return await self._omcloud.post(path, json=payload)

    async def set_preset_config(
        self,
        thermostatunit_id: int,
        heating_away_temp: float,
        heating_vacation_temp: float,
        heating_party_temp: float,
        cooling_away_temp: float,
        cooling_vacation_temp: float,
        cooling_party_temp: float,
    ) -> dict[str, Any]:
        """Set preset of a thermostatunit.

        Args:
            thermostatunit_id: int
            preset: "AUTO|AWAY|PARTY|VACATION"

        Returns:
            Returns a thermostatunit with id
        """

        path = f"/base/installations/{self._omcloud.installation_id}/thermostats/units/{thermostatunit_id}/preset/config"
        payload = {
            "heating": {
                "AWAY": heating_away_temp,
                "VACATION": heating_vacation_temp,
                "PARTY": heating_party_temp
            },
            "cooling": {
                "AWAY": cooling_away_temp,
                "VACATION": cooling_vacation_temp,
                "PARTY": cooling_party_temp
            }
        }
        return await self._omcloud.post(path, json=payload)
