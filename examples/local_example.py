#!/usr/bin/env python3
# noqa: E800
"""
Local Example.

How to use this script:
    pip install python-dotenv
    export LOCALGW='192.168.0.2'
    export USERNAME="dnfqsdfjqsjfqsdjfqf"
    export PASSWORD="djfqsdkfjqsdkfjqsdkfjqsdkfjkqsdjfkjdkfqjdskf"
    python cloud_example.py
"""
import asyncio
import logging
import os
import ssl
import certifi

from dotenv import load_dotenv

from pyhaopenmotics import LocalGateway

ssl_context  = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.options &= ~ssl.OP_NO_SSLv3
ssl_context.minimum_version = ssl.TLSVersion.TLSv1
#ssl_context.set_ciphers("DEFAULT:@SECLEVEL=1") # enables weaker ciphers and protocols
ssl_context.set_ciphers("AES256-SHA") # enables weaker ciphers and protocols
# ssl_context.load_verify_locations(certifi.where())
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

load_dotenv()

localgw = os.environ["LOCALGW"]
username = os.environ["USER_NAME"]
password = os.environ["PASSWORD"]
port = os.environ["PORT"]
tls = os.environ["TLS"]
# verify_ssl = os.environ["VERIFY_SSL"]


async def main() -> None:
    """Show example on controlling your OpenMotics device."""
    async with LocalGateway(
        localgw=localgw,
        username=username,
        password=password,
        port=port,
        tls=tls,
        # verify_ssl=verify_ssl,
        ssl_context=ssl_context,
    ) as omclient:
        await omclient.login()
    
        version = await omclient.exec_action('get_version')
        print(version)

        outputs = await omclient.outputs.get_all()
        print(outputs)

        if outputs[0].status.on is True:
            print('output_0 is on.')
        else:
            print('output_0 is off.')

        output_0 = await omclient.outputs.get_by_id(0)
        print(output_0)

        await omclient.outputs.toggle(0)
        # sensors = await omclient.sensors.get_all()
        # print(sensors)

        await omclient.close()


if __name__ == "__main__":
    asyncio.run(main())
