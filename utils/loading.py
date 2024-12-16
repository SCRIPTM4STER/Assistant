from colorama import Fore, Style
import time

def loading():
    print(f"{Fore.YELLOW}Initializing ALPHA{Style.RESET_ALL}")
    print(f"{Fore.CYAN}\n----------------------------{Style.RESET_ALL}")
    for i in range(5):
        if i > 3:
            print(f"{Fore.BLUE}Loading...{Style.RESET_ALL}")
            time.sleep(1)
        elif i < 2:
            print(f"{Fore.BLUE}Loading....{Style.RESET_ALL}")
            time.sleep(1)
        elif i < 1:
            print(f"{Fore.BLUE}Loading.....{Style.RESET_ALL}")
            time.sleep(1)