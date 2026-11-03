import asyncio
import Utils
from CommonClient import get_base_parser, server_loop, gui_enabled, logger
from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor, _game_watcher, _patch_and_run_game

# Check for Universal Tracker
try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor
    tracker_loaded = True
except ModuleNotFoundError:
    tracker_loaded = False

if tracker_loaded:
    class BizHawkTrackerCommandProcessor(BizHawkClientCommandProcessor, TrackerCommandProcessor):
        pass

    class BizHawkTrackerClientContext(TrackerGameContext, BizHawkClientContext):
        tags = {"AP"}
        command_processor = BizHawkTrackerCommandProcessor
        server_auth = BizHawkClientContext.server_auth

        def on_package(self, cmd, args):
            BizHawkClientContext.on_package(self, cmd, args)
            TrackerGameContext.on_package(self, cmd, args)

        def make_gui(self):
            ui = super().make_gui()
            ui.base_title = "Archipelago BizHawk Client"
            return ui

    ContextClass = BizHawkTrackerClientContext
else:
    ContextClass = BizHawkClientContext

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
        if tracker_loaded:
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