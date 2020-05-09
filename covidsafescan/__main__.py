#!/usr/bin/env python3
import bleak
import asyncio
import traceback
import argparse
import sys
import datetime
import json

UUID="b82ab3fc-1595-4f6a-80f0-fe094cc218f9"

async def connect(address, loop):
    async with bleak.BleakClient(address, loop=loop, timeout=args.timeout) as client:
        message = await client.read_gatt_char(UUID, timeout=args.timeout)
        if args.json: #soooo deeeeep . what is pep8?
            data = {
                "time": datetime.datetime.now().isoformat(),
                "data":  message.decode("utf-8"),
                "address": address
            }
            print(json.dumps(data))
        else:
            print("[" + datetime.datetime.now().isoformat() + "] " + address + " : " + message.decode("utf-8"))

def log(message):
    if args.debug:
        print(str(message), file=sys.stderr)

async def run(loop):
    while True:
        log("Scanning")
        devices = await bleak.discover(timeout=args.timeout)
        log("Found devices")
        log(", ".join([x.address for x in devices]))
        for d in devices:
            try:
                if UUID in d.metadata['uuids']:
                    log("Connecting to " + d.address)
                    try:
                        result = await connect(d.address, loop)
                        if result == False:
                            log("Time out connecting")
                    except KeyboardInterrupt:
                        raise
                    except: # ignore errors - yolo driven dev
                        if args.debug:
                            traceback.print_exc(file=sys.stderr)
            except KeyError:
                pass
        if args.once:
            break

parser = argparse.ArgumentParser(description='Covidsafe BLE Scanner')
parser.add_argument('--debug', dest='debug', action='store_const',
                   const=True, default=False,
                   help='Enables logs')
parser.add_argument('--json', dest='json', action='store_const',
                   const=True, default=False,
                   help='JSON Output')
parser.add_argument('--timeout', type=int, dest='timeout', default=15,
                   help='JSON Output')
parser.add_argument('--once', dest='once', action='store_const',
                   const=True, default=False,
                   help='Only run once')
args = parser.parse_args()
loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))