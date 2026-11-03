import asyncio
import Utils
from CommonClient import get_base_parser, server_loop, gui_enabled, logger
from worlds._bizhawk.context import _game_watcher, _patch_and_run_game
from worlds._bizhawk.client import BizHawkClient
from .ut_context import ContextClass
from ...constants import GAME_NAME

class PokemonSnapBizHawkClient(BizHawkClient):
    game = GAME_NAME
    system = "N64"

    async def validate_rom(self, ctx):
        # TODO: copy over ROM validation from other client
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        return True

    async def game_watcher(self, ctx):
        return await super().game_watcher(ctx)

def launch(*launch_args: str) -> None:
    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an Archipelago patch file")
        args = parser.parse_args(launch_args)

        if args.patch_file != "":
            metadata = _patch_and_run_game(args.patch_file)
            server = metadata.get("server")
            if server:  # ignore missing and empty string servers
                args.connect = server

        ctx = ContextClass(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        watcher_task = asyncio.create_task(_game_watcher(ctx), name="GameWatcher")

        try:
            await watcher_task
        except Exception as e:
            logger.exception(e)

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("BizHawkClient", exception_logger="Client")
    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()