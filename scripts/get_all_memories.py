import asyncio
from infrastructure.services.service_coordinator import Coordinator

coordinator = Coordinator()
asyncio.run(coordinator.mem_manager.get_all_memories())
print(asyncio.run(coordinator.mem_manager.get_all_memories()))
