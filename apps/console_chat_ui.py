import asyncio
import time
from infrastructure.services.service_coordinator import Coordinator

bold_start = '\033[1m'
bold_end = '\033[0m'
coordinator = Coordinator()
safe_words = ['terminate', 'esc', 'goodbye', 'bye', '-esc', 'exit']
ascii_art = """
        ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░ 
       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
       ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
       ░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░   ░▒▓█▓▒░     
       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░     
       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░     
        ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░   ░▒▓█▓▒░     
"""


async def chat_loop(message: str, role: str = 'user'):
    async for chunk in coordinator.user_to_completion(message = message, role = role):
        yield chunk
    print('\n', end='')


async def console_interaction(bot_name:str = 'Bot'):
    user_input = ''
    while user_input.lower() not in safe_words:
        user_input = input(f"{bold_start}User{bold_end}:\t")
        if user_input.lower() not in safe_words:
            print(f"{bold_start}{bot_name}{bold_end}:\t",end='')
            async for resp in chat_loop(user_input):
                print(resp,end='', flush=True)

            await coordinator.update_last_activity()
    else:
        print(f"\n{'_'*80}\n")
        await coordinator.save_current()
        print(f"Session Ended: Goodbye\n{'_'*80}")
        exit(0)


async def get_cur_user(bot_name):
    await coordinator.set_user(name = input(f"{bold_start}Input Name{bold_end}:\t"))
    print(f"{bold_start}{bot_name}{bold_end}:\t", end='')
    async for resp in chat_loop(message=f"{coordinator.cur_user} has logged in", role='system'):
        print(resp, end='', flush=True)



async def start_ui():
    response = await coordinator.system_start_up()
    for _ in range(7):
        print(f"{ascii_art[_*75:75*(1+_)]}",end="")
        time.sleep(.101)
    print(f"\n\n{' '*14}{bold_start}Generative-Heuristic-Operations-for-Simulated-Traits{bold_end}{' '*14}")
    print(f"{'_'*80}\nto end type {bold_start}-esc{bold_end} and press {bold_start}enter{bold_end}\n{'_'*80}")
    return response


async def main():
    start_up = await start_ui()
    await get_cur_user(start_up['bot_name'])
    await console_interaction(start_up['bot_name'])


def launch():
    asyncio.run(main())
