from typing import Optional
import re, time, asyncio, sys

import Utils
from CommonClient import logger, server_loop, get_base_parser, gui_enabled

from .pj64_connector import PJ64Context, pj64connect
from .constants import *
from .update_pj64_config import safe_load_pj64_config

_tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import (TrackerGameContext as CommonContext,
        TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION)
    _tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext, ClientCommandProcessor

class PokemonSnapCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext, server_address: str = None):
        if server_address:
            ctx.server_address = server_address
        super().__init__(ctx)

    def _cmd_pj64_status(self):
        """Gets the current stats of the Project 64 connection."""
        if isinstance(self.ctx, PokemonSnapContext):
            logger.info(f"Project64 Status: {self.ctx.pj64_status}")

class PokemonSnapContext(CommonContext, PJ64Context):
    command_processor = PokemonSnapCommandProcessor
    game = "Pokemon Snap"
    items_handling = 0b111
    tracker_enabled: bool = False
    instance_id: float | None
    pj64_sync_task: Optional[asyncio.Task[None]] = None
    pj64_status: str

    def __init__(self, server_address, password, ap_port):
        """
        Initialize the Pokemon Snap Universal Context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        CommonContext.__init__(self, server_address, password)
        PJ64Context.__init__(self, ap_port)
        self.instance_id = None
        self.tracker_enabled = _tracker_loaded
        self.pj64_status = INITIAL_STATUS
        self.ap_port = ap_port

    def on_package(self, cmd: str, args: dict):
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        CommonContext.on_package(cmd, args)
        match cmd:
            case "PrintJSON":
                if args.get("type", "") == "Countdown" and len(list(args.get("data", []))) > 0 and \
                        "starting countdown of " in args["data"][0]["text"].lower():
                    countdown_var: int = int(re.search(r"\d+", args["data"][0]["text"]).group())
                    print(str(countdown_var))

            case "Connected":  # On Connect
                pass

            case "Bounced":
                if "tags" not in args:
                    return
                if not hasattr(self, "instance_id"):
                    self.instance_id = time.time()

    def _main(self):
        if self.tracker_enabled:
            self.run_generator()
            self.tags.remove("Tracker")
        else:
            logger.warning("Could not find Universal Tracker.")

    def make_gui(self):
        if not _check_universal_tracker_version():
            Utils.messagebox("Universal Tracker needs updated",
            f"Please update your Universal Tracker. The version currently installed is {UT_VERSION}.", error=True)
            raise ImportError("Need to update universal tracker version to at least v0.2.11.")

        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from kvui import GameManager
        ui: type[GameManager] = CommonContext.make_gui()
        class UniversalWrapper(ui):
            base_title: str = "Pokemon Snap Client"

            def build(self):
                container = super().build()
                if _tracker_loaded:
                    self.base_title += f" | Universal Tracker {UT_VERSION}"
                return container

        return UniversalWrapper

    async def check_snap_locations(self):
        pass

    async def receive_snap_items(self):
        pass

    async def disconnect(self, allow_autoreconnect: bool = False):
        await CommonContext.disconnect(self, allow_autoreconnect)
        self.pj64_status = INITIAL_STATUS

    async def wait_for_next_loop(self, time_to_wait: float):
        await asyncio.sleep(time_to_wait)

    async def pj64_sync_main_task(self):
        logger.info(f"Using {CLIENT_NAME} client...")
        logger.info("Starting Project64 connector. Use /project64 for status information.")

        try:
            while not self.exit_event.is_set():
                try:
                    if not self.pj64_status == CONNECTED_STATUS:
                        await pj64connect(self)

                        if not self.pj64_status == CONNECTING_STATUS:
                            self.pj64_status = CONNECTING_STATUS
                            logger.info(self.pj64_status)

                        if not self.slot:
                            await self.wait_for_next_loop(5)
                            continue

                        # TODO validate seed here
                        # TODO validate GameID here or in PJ64 loop
                        # TODO check for in_game or something similar?

                        self.pj64_status = CONNECTED_STATUS
                        logger.info(self.pj64_status)

                    await self.check_snap_locations()
                    await self.receive_snap_items()

                except Exception as ex:
                    logger.error(str(ex))
                    self.pj64_status = DISCONNECTED_STATUS
                    logger.info(DISCONNECTED_STATUS)
                    await self.disconnect()
                    await self.wait_for_next_loop(5)
                    continue
        except Exception as threadEx:
            logger.error("Something went horribly wrong with the Pokemon Snap client. Details: " + str(threadEx))


def _check_universal_tracker_version() -> bool:
    import re
    if not _tracker_loaded:
        return True

    # We are checking for a string that starts with v contains any amount of digits followed by a period
    # repeating three times (e.x. v0.2.11)
    match = re.search(r"v\d+.(\d+).(\d+)", UT_VERSION)
    if len(match.groups()) < 2:
        return False
    if int(match.groups()[0]) < 2:
        return False
    if int(match.groups()[1]) < 11:
        return False

    return True

def main(*launch_args: str):
    import colorama

    server_address: str = ""

    Utils.init_logging(CLIENT_NAME)
    logger.info(f"Starting {CLIENT_NAME}...")

    parser = get_base_parser()
    args = parser.parse_args(launch_args)

    async def _main(connect, password):
        try:
            ap_port = safe_load_pj64_config()
            ctx = PokemonSnapContext(server_address if server_address else connect, password, ap_port)
            ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

            ctx.pj64_sync_task = asyncio.create_task(ctx.pj64_sync_main_task(), name="PokemonSnap_PJ64Sync")

            # Runs Universal Tracker's internal generator
            ctx._main()

            if gui_enabled:
                ctx.run_gui()
            ctx.run_cli()
            await ctx.wait_for_next_loop(5)

            await ctx.exit_event.wait()
            await ctx.shutdown()

            if ctx.pj64_sync_task:
                await ctx.pj64_sync_task
        except Exception as clientEx:
            client_msg: str = (f"An unknown error occurred while running Pokemon Snap's client.\n" +
                f"Additional details:\n") + str(clientEx)
            logger.error(client_msg)
            Utils.messagebox(f"{CLIENT_NAME} Client Issue", client_msg, True)
            raise clientEx

    colorama.just_fix_windows_console()
    asyncio.run(_main(args.connect, args.password))
    colorama.deinit()

if __name__ == "__main__":
    Utils.init_logging(CLIENT_NAME, exception_logger="Client")
    main(*sys.argv[1:])
