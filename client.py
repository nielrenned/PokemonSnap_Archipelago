from typing import Optional, NamedTuple
import base64, os, re, time, asyncio, sys

import Utils
from CommonClient import logger, server_loop, get_base_parser, gui_enabled
from NetUtils import ClientStatus

from .pj64_connector import PJ64Context, pj64connect, pj64disconnect, pj64_read_memory, pj64_write_memory
from .constants import *
from .locations import wonderful_id as wdfl_id, multiple_id as mult_id, regional_id as rgnl_id, special_id
from .update_pj64_config import safe_load_pj64_config
from .items import item_dictionary
from . import addresses as addr

_code_to_name = {data.ps_code: name for name, data in item_dictionary.items()}

_tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import (TrackerGameContext as CommonContext,
        TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION)
    _tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext, ClientCommandProcessor

class PokemonSnapReportScore(NamedTuple):
    special_bonus: int
    pose_score: int
    size_score: int
    technique_score: int
    same_pokemon_score: int
    special_pose_bits: int
    courses_seen_bits: int # bit field containing what courses photos have been taken in
    unused: int

    def poses(self) -> list[int]:
        pose_list = []
        for i in range(12):
            if self.special_pose_bits & (1 << i) != 0:
                pose_list.append(i + 1)
        return pose_list

    def score(self) -> int:
        # Note: this is probably inaccurate
        score = self.special_bonus + self.pose_score + self.size_score
        if self.technique_score != 0:
            score *= 2
        score += self.same_pokemon_score
        return score

class PokemonSnapCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext, server_address: str = None):
        if server_address:
            ctx.server_address = server_address
        super().__init__(ctx)

    def _cmd_pj64_status(self):
        """Gets the current status of the Project 64 connection."""
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
        self.checked_snap_locations: set[int] = set()

    def on_package(self, cmd: str, args: dict):
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        CommonContext.on_package(self, cmd, args)
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
        ui: type[GameManager] = CommonContext.make_gui(self)
        class UniversalWrapper(ui):
            base_title: str = "Pokemon Snap Client"

            def build(self):
                container = super().build()
                if _tracker_loaded:
                    self.base_title += f" | Universal Tracker {UT_VERSION}"
                return container

        return UniversalWrapper

    async def _expansion_loaded(self) -> bool:
        magic = (await pj64_read_memory(self, "u32", addr.EXPANSION_MAGIC, 4))[0]
        return magic == addr.EXPANSION_LOADED

    async def _read_auth_token(self):
        """Read the per-seed auth token from the ROM as base64, or None."""
        try:
            if self.streams is None or not await self._expansion_loaded():
                return None
            raw = bytes(await pj64_read_memory(self, "u8", addr.AUTH_ADDR, addr.AUTH_LEN))
            if not raw or raw == addr.UNPATCHED_AUTH:
                return None
            return base64.b64encode(raw).decode("ascii")
        except Exception:
            return None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        notified = False
        while not self.auth and not self.exit_event.is_set():
            token = await self._read_auth_token()
            if token:
                self.auth = token
                break
            if not notified:
                logger.info("Waiting to read the connect token from a patched, running Pokemon Snap ROM...")
                notified = True
            await asyncio.sleep(3)

        if not self.auth:
            return

        await self.send_connect()

    async def check_snap_locations(self):
        if not self.slot or not await self._expansion_loaded():
            return

        scores = []
        raw_scores = await pj64_read_memory(self, "u16", addr.SPECIES_SCORES, addr.NUM_SPECIES * 8 * 2)
        for i in range(0, addr.NUM_SPECIES * 8, 8):
            report_score = PokemonSnapReportScore(*raw_scores[i:i+8])
            scores.append(report_score)

        new_checks = set()
        for slot, report in enumerate(scores):
            if report.score() == 0: continue

            poses_seen_ids = [i+1 for i in range(12) if ((1 << i) & report.special_pose_bits) != 0]
            for pose_id in poses_seen_ids:
                if special_id(pose_id) not in self.checked_snap_locations:
                    new_checks.add(special_id(pose_id))

            courses_seen_ids = [i for i in range(7) if ((1 << i) & report.courses_seen_bits) != 0]
            for course_id in courses_seen_ids:
                location_id = rgnl_id(slot + 1, course_id)
                if location_id not in self.checked_snap_locations:
                    logger.info(f'Slot {slot + 1}: {report}')
                    new_checks.add(location_id)
                if report.technique_score != 0 and wdfl_id(location_id) not in self.checked_snap_locations:
                    new_checks.add(wdfl_id(location_id))
                if report.same_pokemon_score != 0 and mult_id(location_id) not in self.checked_snap_locations:
                    new_checks.add(mult_id(location_id))

        if new_checks:
            self.checked_snap_locations |= new_checks
            await self.check_locations(list(new_checks))

        if not self.finished_game and addr.MEW_LOCATION in self.checked_snap_locations:
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self.finished_game = True
            logger.info("Mew photographed - goal complete!")

    async def receive_snap_items(self):
        if not self.slot or not await self._expansion_loaded():
            return

        await pj64_write_memory(self, "u32", addr.CAN_USE_OVERRIDE, [0])
        await pj64_write_memory(self, "u32", addr.COURSE_OVERRIDE, [0])

        can_use_mask = 0
        course_mask = 0
        film = addr.FILM_BASE
        for net_item in self.items_received:
            name = _code_to_name.get(net_item.item)
            if name is None:
                continue
            if name in addr.CAN_USE_BITS:
                can_use_mask |= 1 << addr.CAN_USE_BITS[name]
            elif name in addr.COURSE_IDS:
                course_mask |= 1 << addr.COURSE_IDS[name]
            elif name == addr.FILM_UPGRADE:
                film = min(film + addr.FILM_STEP, addr.FILM_CAP)

        await pj64_write_memory(self, "u32", addr.CAN_USE_MASK, [can_use_mask])
        await pj64_write_memory(self, "u32", addr.COURSE_UNLOCK_MASK, [course_mask])
        await pj64_write_memory(self, "u32", addr.MAX_FILM, [film])

    async def wait_for_next_loop(self, time_to_wait: float):
        await asyncio.sleep(time_to_wait)

    async def pj64_sync_main_task(self):
        logger.info(f"Using {CLIENT_NAME}...")
        logger.info("Starting Project64 connector. Use /pj64_status for status information.")

        try:
            while not self.exit_event.is_set():
                try:
                    if not self.pj64_status == CONNECTED_STATUS:
                        if not self.pj64_status == CONNECTING_STATUS:
                            if not await pj64connect(self):
                                self.pj64_status = DISCONNECTED_STATUS
                                logger.info(self.pj64_status)
                                await self.wait_for_next_loop(5)
                                continue
                            self.pj64_status = CONNECTING_STATUS
                            logger.info(self.pj64_status)

                        # Wait for AP login and the patched ROM to be running.
                        if not self.slot or not await self._expansion_loaded():
                            await self.wait_for_next_loop(1)
                            continue

                        self.pj64_status = CONNECTED_STATUS
                        logger.info(self.pj64_status)

                    await self.check_snap_locations()
                    await self.receive_snap_items()
                    await self.wait_for_next_loop(0.125)

                except Exception as ex:
                    logger.error(f"Project64 connection lost: {ex}")
                    pj64disconnect(self)
                    self.pj64_status = DISCONNECTED_STATUS
                    logger.info(DISCONNECTED_STATUS)
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

def _patch_and_launch(patch_file: str) -> str:
    """Turn a dragged-in .apsnap patch into a ROM and start the emulator on it.

    Returns the Archipelago server address embedded in the patch (set when the
    patch was downloaded from a room), or an empty string if none.
    """
    from .rom import PokemonSnapProcedurePatch

    rom_path = os.path.splitext(patch_file)[0] + ".z64"
    server = ""
    try:
        patch = PokemonSnapProcedurePatch(patch_file)
        patch.read()
        server = patch.server or ""
        if not os.path.exists(rom_path):
            patch.patch(rom_path)
            logger.info(f"Patched ROM created at {rom_path}")
        else:
            logger.info(f"Using existing patched ROM at {rom_path}")
    except Exception as ex:
        logger.error(f"Failed to create the patched ROM: {ex}")
        Utils.messagebox(f"{CLIENT_NAME} Patch Error", str(ex), True)
        return server

    try:
        safe_load_pj64_config()
    except Exception as ex:
        logger.warning(f"Could not update the Project64 config automatically: {ex}")

    from settings import get_settings
    emu = get_settings()["pokemon_snap_options"]["emulator_settings"]
    if not emu["auto_start"]:
        logger.info(f"Auto-start is off; open this ROM in your emulator: {rom_path}")
        return server

    exe = str(emu["path"])
    if not os.path.exists(exe):
        exe = Utils.user_path(exe)
    if not os.path.exists(exe):
        logger.info(f"No emulator configured; open this ROM in Project64: {rom_path}")
        return server

    # PJ64 3.0 finds Scripts/ and Config/ relative to the cwd, so run it from there.
    import subprocess
    exe = os.path.abspath(exe)
    subprocess.Popen([exe, os.path.abspath(rom_path)], cwd=os.path.dirname(exe))
    logger.info(f"Launched {exe} with {rom_path}")
    logger.info("If the client doesn't connect, start ap_psnap_pj64_adapter_30.js via "
                "Debugger -> Scripts in Project64.")
    return server


def main(*launch_args: str):
    import colorama

    Utils.init_logging(CLIENT_NAME)
    logger.info(f"Starting {CLIENT_NAME}...")

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?",
                        help="Path to an .apsnap patch file to apply and launch.")
    args = parser.parse_args(launch_args)

    server_address: str = args.connect or ""
    if args.patch_file:
        patch_server = _patch_and_launch(args.patch_file)
        # --connect wins; else use the patch's embedded room address.
        if patch_server and not args.connect:
            server_address = patch_server
            logger.info(f"Connecting to the server address from the patch: {server_address}")

    async def _main(connect, password):
        try:
            ap_port = safe_load_pj64_config()
            ctx = PokemonSnapContext(connect, password, ap_port)
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
    asyncio.run(_main(server_address, args.password))
    colorama.deinit()

if __name__ == "__main__":
    Utils.init_logging(CLIENT_NAME, exception_logger="Client")
    main(*sys.argv[1:])
