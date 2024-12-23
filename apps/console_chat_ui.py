import asyncio
from infrastructure.services.service_coordinator import Coordinator

coordinator = Coordinator()

async def chat_loop(user_input):
    async for chunk in coordinator.user_to_completion(user_input):
        yield chunk


async def console_interaction():
    safewords = ['terminate', 'esc', 'goodbye', 'bye', '-esc', 'exit']
    await coordinator.system_start_up()
    bot_name = coordinator.mem_manager.get_identity()['name']
    print('Chat\n' + '_' * 80 + '\n' + 'to end type "-esc" and press *enter*\n' + '_' * 80)
    user_input = ''
    while user_input.lower() not in safewords:
        user_input = input('\033[1mUser\033[0m:\t')
        if user_input.lower() not in safewords:
            print(f'\033[1m{bot_name}\033[0m:\t',end='')
            async for resp in chat_loop(user_input):
                print(resp,end='', flush=True)
            print('\n',end='')
            await coordinator.update_last_activity()

    else:
        print('\n' + '_' * 80 + '\n')
        await coordinator.save_current()
        print('Session Ended: Goodbye\n' + '_' * 80)

asyncio.run(console_interaction())