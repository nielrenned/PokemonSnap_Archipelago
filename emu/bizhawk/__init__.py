import asyncio
import worlds._bizhawk as bizhawk
import Utils

from typing import Sequence
from CommonClient import get_base_parser, server_loop, gui_enabled, logger
from worlds._bizhawk.context import BizHawkClientContext, _game_watcher, _patch_and_run_game
from worlds._bizhawk.client import BizHawkClient

from .ut_context import ContextClass
from .. import PokemonSnapGenericEmuClient
from ...constants import GAME_NAME
from ...client import PokemonSnapClient

INT_SIZE = {
    'u8':  1,
    's8':  1,
    'u16': 2,
    's16': 2,
    'u32': 4,
    's32': 4,
}

SIGNEDNESS = {
    'u8':  False,
    's8':  True,
    'u16': False,
    's16': True,
    'u32': False,
    's32': True,
}

ADDR_MASK = 0x1FFFFFFF

class PokemonSnapBizHawkClient(BizHawkClient, PokemonSnapGenericEmuClient):
    client: PokemonSnapClient
    game = GAME_NAME
    system = "N64"

    async def validate_rom(self, ctx: BizHawkClientContext):
        # TODO: copy over ROM validation from other client
        self.client = PokemonSnapClient()
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        ctx.slot_data = {}
        return True

    async def game_watcher(self, ctx: BizHawkClientContext):
        if ctx.slot_data:
            await self.client.check_snap_locations(self, ctx)
            await self.client.receive_snap_items(self, ctx)

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict):
        ...

    async def read(self, ctx: BizHawkClientContext, read_list: Sequence[tuple[int, int, str]]):
        # Convert the read requests
        bizhawk_read_list = [(addr & ADDR_MASK, size, 'RDRAM') for addr, size, _ in read_list]
        bizhawk_results = await bizhawk.read(ctx.bizhawk_ctx, bizhawk_read_list)
        # Convert the results
        results = []
        for i, (_, size, int_type) in enumerate(read_list):
            result_bytes = bizhawk_results[i]
            int_size = INT_SIZE[int_type]
            converted_result = [int.from_bytes(result_bytes[j:j+int_size], byteorder='big', signed=SIGNEDNESS[int_type])
                                for j in range(0, size, int_size)]
            results.append(converted_result)
        return results

    async def write(self, ctx: BizHawkClientContext, write_list: Sequence[tuple[int, Sequence[int], str]]):
        # Convert the write requests
        bizhawk_write_list = []
        for addr, ints, write_type in write_list:
            bytes_to_write = b''.join(int.to_bytes(n, length=INT_SIZE[write_type], byteorder='big', signed=SIGNEDNESS[write_type]) for n in ints)
            bizhawk_write_list.append((addr & ADDR_MASK, bytes_to_write, 'RDRAM'))
        return await bizhawk.write(ctx.bizhawk_ctx, bizhawk_write_list)


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