import os
import base64
import json
import requests
import time
import random
from datetime import datetime
from fake_useragent import FakeUserAgent
from colorama import Fore, Style, Back, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Default headers
DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://app.nodego.ai",
    "Referer": "https://app.nodego.ai/",
}

class NodeGoAutomation:
    def __init__(self):
        self.proxies = []
        self.last_proxy = None
        
    def show_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""
{Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════════════╗
║             NODEGO AUTOMATION BOT             ║
║        Auto Check-in & Task Completion        ║
║        Created by: t.me/sentineldiscus        ║
╚═══════════════════════════════════════════════╝{Style.RESET_ALL}
        """)
        
    def log_success(self, message):
        print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")
        
    def log_info(self, message):
        print(f"{Fore.CYAN}[i] {message}{Style.RESET_ALL}")
        
    def log_warning(self, message):
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
        
    def log_error(self, message):
        print(f"{Fore.RED}[×] {message}{Style.RESET_ALL}")

    def setup_proxy(self):
        while True:
            print(f"\n{Fore.CYAN}[SELECT PROXY MODE]{Style.RESET_ALL}")
            print(f"{Fore.RED}1. Gunakan proxy gratis")
            print("2. Gunakan proxy pribadi")
            print(f"3. Jalankan tanpa proxy {Style.RESET_ALL}")
            
            try:
                choice = int(input(f"\n{Fore.CYAN}Choose [1/2/3]: {Style.RESET_ALL}"))
                if choice in [1, 2, 3]:
                    self.load_proxies(choice)
                    return choice
                self.log_error("Please enter 1, 2, or 3!")
            except ValueError:
                self.log_error("Invalid input!")

    def load_proxies(self, choice):
        if choice == 3:
            return
            
        filename = "proxy.txt" if choice == 2 else "proxyshare.txt"
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                if self.proxies:
                    self.log_success(f"Loaded {len(self.proxies)} proxies")
                else:
                    self.log_warning("No proxies found in file")
            else:
                self.log_error(f"Proxy file {filename} not found")
        except Exception as e:
            self.log_error(f"Error loading proxies: {str(e)}")

    def get_next_proxy(self):
        if not self.proxies:
            return None
        if self.last_proxy in self.proxies:
            index = self.proxies.index(self.last_proxy)
            self.last_proxy = self.proxies[(index + 1) % len(self.proxies)]
        else:
            self.last_proxy = random.choice(self.proxies)
        return self.last_proxy

    def decode_token(self, token):
        try:
            payload = token.split(".")[1]
            pad = "=" * (4 - len(payload) % 4)
            decoded = base64.urlsafe_b64decode(payload + pad).decode("utf-8")
            return json.loads(decoded).get("email")
        except Exception:
            return None

    def process_account(self, token, progress):
        email = self.decode_token(token)
        if not email:
            progress.update(1)
            return f"{Fore.RED}[×] Invalid token: {token[:20]}...{Style.RESET_ALL}"

        self.log_info(f"Processing account: {email}")
        
        try:
            while True:
                proxy = self.get_next_proxy()
                proxy_dict = {"http": proxy, "https": proxy} if proxy else None
                
                # Check-in
                try:
                    response = requests.post(
                        "https://nodego.ai/api/user/checkin",
                        headers={**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"},
                        proxies=proxy_dict,
                        timeout=15
                    )
                    if response.status_code == 200:
                        self.log_success(f"Check-in successful for {email}")
                except Exception as e:
                    self.log_error(f"Check-in failed for {email}: {str(e)}")
                    continue

                # Get and complete tasks
                try:
                    tasks_response = requests.get(
                        "https://nodego.ai/api/tasks",
                        headers={**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"},
                        proxies=proxy_dict,
                        timeout=15
                    )
                    if tasks_response.status_code == 200:
                        tasks = tasks_response.json().get("metadata", [])
                        for task in tasks:
                            complete_response = requests.post(
                                "https://nodego.ai/api/user/task",
                                headers={**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"},
                                json={"taskId": task["code"]},
                                proxies=proxy_dict,
                                timeout=15
                            )
                            if complete_response.status_code == 200:
                                self.log_success(f"Completed task: {task['title']} for {email}")
                except Exception as e:
                    self.log_error(f"Task processing failed for {email}: {str(e)}")
                    continue

                # Ping server
                while True:
                    try:
                        requests.post(
                            "https://nodego.ai/api/user/nodes/ping",
                            headers={**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"},
                            proxies=proxy_dict,
                            timeout=15
                        )
                        self.log_info(f"Ping sent for {email}")
                        time.sleep(180)
                    except Exception as e:
                        self.log_error(f"Ping failed for {email}: {str(e)}")
                        break

        except Exception as e:
            self.log_error(f"Account processing failed for {email}: {str(e)}")
        finally:
            progress.update(1)

    def run(self):
        self.show_banner()
        proxy_mode = self.setup_proxy()

        # Load tokens
        try:
            with open('data.txt', 'r') as f:
                tokens = [line.strip() for line in f if line.strip()]
        except Exception as e:
            self.log_error(f"Error loading tokens: {str(e)}")
            return

        # Get thread count
        try:
            thread_count = int(input(f"\n{Fore.CYAN}Enter number of threads (default 5): {Style.RESET_ALL}") or 5)
        except ValueError:
            thread_count = 5
            self.log_warning("Invalid thread count, using default: 5")

        print(f"\n{Fore.CYAN}[STARTING AUTOMATION]{Style.RESET_ALL}\n")

        # Process accounts with progress bar
        with tqdm(total=len(tokens), desc="Processing Accounts", 
                 bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Style.RESET_ALL)) as progress:
            
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = []
                for token in tokens:
                    future = executor.submit(self.process_account, token, progress)
                    futures.append(future)
                
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if result:
                            print(result)
                    except Exception as e:
                        self.log_error(f"Thread error: {str(e)}")

if __name__ == "__main__":
    automation = NodeGoAutomation()
    automation.run()
