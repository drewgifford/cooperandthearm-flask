from cooperandthearm import CooperAndTheArm, Component
from cooperandthearm.command import Command
import asyncio

class ArmDispatcher:
    def __init__(self, arm: CooperAndTheArm):
        self.arm = arm
        self.queue = asyncio.Queue()
        self.running = False

    async def start(self):
        self.running = True
        asyncio.create_task(self._worker())

    async def stop(self):
        self.running = False
    
    async def dispatch(self, *commands: Command):
        fut = asyncio.get_event_loop().create_future()
        await self.queue.put((commands, fut))
        return await fut

    def dispatch_sync(self, *commands: Command):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()

            asyncio.set_event_loop(new_loop)

            try:
                return new_loop.run_until_complete(self.dispatch(*commands))
            finally:
                new_loop.close()
        else:
            return loop.run_until_complete(self.dispatch(*commands))
    

    async def _worker(self):
        while self.running:
            print('i am running')
            commands, fut = await self.queue.get()
            try:
                result = await self.arm.dispatch(*commands)
                fut.set_result(result)
            except Exception as e:
                fut.set_exception(e)