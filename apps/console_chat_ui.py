import asyncio
import time
from infrastructure.services.service_coordinator import Coordinator

bold_start = '\033[1m'
bold_end = '\033[0m'
coordinator = Coordinator()
bot_name = coordinator.mem_manager.get_identity()['name']
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


async def chat_loop(user_input):
    async for chunk in coordinator.user_to_completion(user_input):
        yield chunk


async def console_interaction():
    user_input = ''
    while user_input.lower() not in safe_words:
        user_input = input(f"{bold_start}User{bold_end}:\t")
        if user_input.lower() not in safe_words:
            print(f"{bold_start}{bot_name}{bold_end}:\t",end='')
            async for resp in chat_loop(user_input):
                print(resp,end='', flush=True)
            print('\n',end='')
            await coordinator.update_last_activity()
    else:
        print(f"\n{'_'*80}\n")
        await coordinator.save_current()
        print(f"Session Ended: Goodbye\n{'_'*80}")
        exit(0)


async def start_ui():
    await coordinator.system_start_up()
    for _ in range(7):
        print(f"{ascii_art[_*75:75*(1+_)]}",end="")
        time.sleep(.101)
    print(f"\n\n{' '*14}{bold_start}Generative-Heuristic-Operations-for-Simulated-Traits{bold_end}{' '*14}")
    print(f"{'_'*80}\nto end type {bold_start}-esc{bold_end} and press {bold_start}enter{bold_end}\n{'_'*80}")


async def main():
    await start_ui()
    await console_interaction()


def launch():
    asyncio.run(main())
