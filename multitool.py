#!/usr/bin/env python3

import socket
import string
import math
import sys
import urllib.request
import urllib.error

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime


# ============================================================
# SETTINGS
# ============================================================

MAX_THREADS = 50
WEB_THREADS = 20
DEFAULT_TIMEOUT = 0.5

RESULT_FILE = "scan_results.txt"


# ============================================================
# COMMON PASSWORDS
# ============================================================

COMMON_PASSWORDS = {
    "123456",
    "password",
    "123456789",
    "12345678",
    "12345",
    "qwerty",
    "abc123",
    "password1",
    "admin",
    "letmein",
    "welcome",
    "monkey",
    "111111",
    "iloveyou",
    "azerty",
    "admin123",
    "root",
    "toor",
}


KEYBOARD_PATTERNS = {
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "azerty",
    "qwertyuiop",
    "asdfghjkl",
}


# ============================================================
# BANNER
# ============================================================

def banner():

    print(r"""
   ____      __           ____
  / ___|   _| |_   _ ___ / ___|  ___ __ _ _ __
 | |      | | | | | / __| \___ \ / __/ _` | '_ \
 | |___   | |_| |_| \__ \  ___) | (_| (_| | | | |
  \____|   \__|\__,_|___/ |____/ \___\__,_|_| |_|

        Cybersecurity Multi-Tool
              by Mohamed
                 ver: 4.0.0
""")


# ============================================================
# PORT SCANNER
# ============================================================

def check_port(target_ip, port, timeout=DEFAULT_TIMEOUT):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(timeout)

    try:

        result = sock.connect_ex(
            (target_ip, port)
        )

        if result != 0:
            return None

        try:

            service = socket.getservbyport(
                port,
                "tcp"
            )

        except OSError:

            service = "unknown"

        return {
            "port": port,
            "service": service
        }

    except (
        socket.timeout,
        OSError
    ):

        return None

    finally:

        sock.close()


def validate_ports(start_port, end_port):

    if not 1 <= start_port <= 65535:

        raise ValueError(
            "Start port khaso ykon bin 1 w 65535."
        )

    if not 1 <= end_port <= 65535:

        raise ValueError(
            "End port khaso ykon bin 1 w 65535."
        )

    if start_port > end_port:

        raise ValueError(
            "Start port maymknch ykon kber mn end port."
        )


def save_scan_results(
    target,
    target_ip,
    results
):

    try:

        with open(
            RESULT_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write("\n")
            file.write("=" * 60 + "\n")

            file.write(
                f"Tarikh: "
                f"{datetime.now().isoformat()}\n"
            )

            file.write(
                f"Target: {target}\n"
            )

            file.write(
                f"IP: {target_ip}\n"
            )

            file.write("=" * 60 + "\n")

            for result in results:

                file.write(
                    f"{result['port']}/tcp "
                    f"OPEN - "
                    f"{result['service']}\n"
                )

            file.write("\n")

        return True

    except OSError as error:

        print(
            f"[!] Mochkil f save: {error}"
        )

        return False


def port_scanner():

    print("\n" + "=" * 60)
    print("PORT SCANNER")
    print("=" * 60)

    target = input(
        "Target IP/hostname: "
    ).strip()

    if not target:

        print("[!] Target khawi.")
        return

    try:

        start_port = int(
            input("Start port: ")
        )

        end_port = int(
            input("End port: ")
        )

        validate_ports(
            start_port,
            end_port
        )

    except ValueError as error:

        print(f"[!] {error}")
        return

    try:

        target_ip = socket.gethostbyname(
            target
        )

    except socket.gaierror:

        print(
            "[!] Ma9dertch nl9a target."
        )

        return

    total = (
        end_port - start_port + 1
    )

    print()
    print(
        f"[*] Target : {target}"
    )

    print(
        f"[*] IP     : {target_ip}"
    )

    print(
        f"[*] Range  : "
        f"{start_port}-{end_port}"
    )

    print(
        "[*] Kanbda scan..."
    )

    results = []
    completed = 0

    with ThreadPoolExecutor(
        max_workers=MAX_THREADS
    ) as executor:

        futures = {
            executor.submit(
                check_port,
                target_ip,
                port
            ): port

            for port in range(
                start_port,
                end_port + 1
            )
        }

        for future in as_completed(
            futures
        ):

            completed += 1

            try:

                result = future.result()

            except Exception:

                result = None

            if result:

                results.append(result)

                print(
                    f"\n[+] "
                    f"{result['port']}/tcp OPEN "
                    f"- {result['service']}"
                )

            progress = (
                completed / total
            ) * 100

            print(
                f"\r[*] Progress: "
                f"{completed}/{total} "
                f"({progress:.1f}%)",
                end=""
            )

    results.sort(
        key=lambda x: x["port"]
    )

    print("\n")

    print("=" * 60)
    print("SCAN SALA")
    print("=" * 60)

    print(
        f"Open ports: {len(results)}"
    )

    if results:

        save = input(
            "Bghiti tsave results? (y/n): "
        ).strip().lower()

        if save == "y":

            if save_scan_results(
                target,
                target_ip,
                results
            ):

                print(
                    "[+] Results tsavaw."
                )

    print()


# ============================================================
# PASSWORD CHECKER
# ============================================================

def has_sequence(password):

    password = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "9876543210"
    ]

    for sequence in sequences:

        for size in range(4, 7):

            for i in range(
                len(sequence) - size + 1
            ):

                part = sequence[
                    i:i + size
                ]

                if part in password:

                    return True

    return False


def has_keyboard_pattern(password):

    password = password.lower()

    for pattern in KEYBOARD_PATTERNS:

        if pattern in password:

            return True

    return False


def analyze_password(password):

    length = len(password)

    lower = any(
        c in string.ascii_lowercase
        for c in password
    )

    upper = any(
        c in string.ascii_uppercase
        for c in password
    )

    digit = any(
        c in string.digits
        for c in password
    )

    symbol = any(
        c in string.punctuation
        for c in password
    )

    charset = 0

    if lower:
        charset += 26

    if upper:
        charset += 26

    if digit:
        charset += 10

    if symbol:
        charset += len(
            string.punctuation
        )

    if length and charset:

        entropy = (
            length *
            math.log2(charset)
        )

    else:

        entropy = 0

    common = (
        password.lower()
        in COMMON_PASSWORDS
    )

    repeated = False

    if length:

        for char in set(password):

            if (
                password.count(char)
                > length * 0.5
            ):

                repeated = True
                break

    return {
        "length": length,
        "lower": lower,
        "upper": upper,
        "digit": digit,
        "symbol": symbol,
        "entropy": entropy,
        "common": common,
        "repeated": repeated,
        "sequence": has_sequence(password),
        "keyboard": has_keyboard_pattern(
            password
        )
    }


def get_strength(result):

    if result["common"]:
        return "VERY WEAK"

    if result["keyboard"]:
        return "VERY WEAK"

    if result["sequence"]:
        return "WEAK"

    if result["repeated"]:
        return "WEAK"

    entropy = result["entropy"]

    if entropy < 28:
        return "VERY WEAK"

    if entropy < 36:
        return "WEAK"

    if entropy < 60:
        return "MEDIUM"

    if entropy < 100:
        return "STRONG"

    return "VERY STRONG"


def password_checker():

    print("\n" + "=" * 60)
    print("PASSWORD STRENGTH CHECKER")
    print("=" * 60)

    # Hna password ghadi yban normal f terminal
    password = input(
        "Password: "
    )

    if not password:

        print(
            "[!] Password khawya."
        )

        return

    result = analyze_password(
        password
    )

    strength = get_strength(
        result
    )

    print("\n" + "-" * 60)

    print(
        f"Password   : {password}"
    )

    print(
        f"Length     : "
        f"{result['length']}"
    )

    print(
        f"Lowercase  : "
        f"{'YES' if result['lower'] else 'NO'}"
    )

    print(
        f"Uppercase  : "
        f"{'YES' if result['upper'] else 'NO'}"
    )

    print(
        f"Numbers    : "
        f"{'YES' if result['digit'] else 'NO'}"
    )

    print(
        f"Symbols    : "
        f"{'YES' if result['symbol'] else 'NO'}"
    )

    print(
        f"Entropy    : "
        f"{result['entropy']:.1f} bits"
    )

    print(
        f"Common     : "
        f"{'YES' if result['common'] else 'NO'}"
    )

    print(
        f"Repetition : "
        f"{'YES' if result['repeated'] else 'NO'}"
    )

    print(
        f"Sequence   : "
        f"{'YES' if result['sequence'] else 'NO'}"
    )

    print(
        f"Keyboard   : "
        f"{'YES' if result['keyboard'] else 'NO'}"
    )

    print("-" * 60)

    print(
        f"STRENGTH   : {strength}"
    )

    print("-" * 60)

    tips = []

    if result["length"] < 12:

        tips.append(
            "Zid f length, 12+ characters a7san."
        )

    if not result["lower"]:

        tips.append(
            "Zid lowercase."
        )

    if not result["upper"]:

        tips.append(
            "Zid uppercase."
        )

    if not result["digit"]:

        tips.append(
            "Zid numbers."
        )

    if not result["symbol"]:

        tips.append(
            "Zid symbols."
        )

    if result["common"]:

        tips.append(
            "Bdel password 7it common."
        )

    if result["sequence"]:

        tips.append(
            "Tjanab sequences bhal 123456."
        )

    if result["keyboard"]:

        tips.append(
            "Tjanab patterns bhal qwerty."
        )

    if result["repeated"]:

        tips.append(
            "Tjanab repetition kbir."
        )

    print(
        "\nNsa2e7:"
    )

    if not tips:

        print(
            "[+] Password kayban 9awi."
        )

    else:

        for tip in tips:

            print(
                f"- {tip}"
            )

    print()


# ============================================================
# WEB CONTENT DISCOVERY
# ============================================================

def check_web_path(
    target,
    word
):

    word = word.strip().lstrip("/")

    if not word:

        return None

    url = (
        target.rstrip("/")
        + "/"
        + word
    )

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": "CyberScan/4.0"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=3
        ) as response:

            status = response.status

            if status in {
                200,
                204,
                301,
                302,
                307,
                308,
                401,
                403
            }:

                return {
                    "url": url,
                    "status": status
                }

    except urllib.error.HTTPError as error:

        if error.code in {
            401,
            403
        }:

            return {
                "url": url,
                "status": error.code
            }

    except (
        urllib.error.URLError,
        socket.timeout,
        TimeoutError
    ):

        pass

    except Exception:

        pass

    return None


def web_content_discovery():

    print("\n" + "=" * 60)
    print("WEB CONTENT DISCOVERY")
    print("=" * 60)

    target = input(
        "Target URL "
        "(matalan http://127.0.0.1:3000): "
    ).strip()

    wordlist = input(
        "Wordlist path: "
    ).strip()

    if not target:

        print(
            "[!] URL khawi."
        )

        return

    if not target.startswith(
        ("http://", "https://")
    ):

        print(
            "[!] URL khaso ybda "
            "b http:// wla https://"
        )

        return

    try:

        with open(
            wordlist,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            words = [
                line.strip()
                for line in file
                if line.strip()
            ]

    except OSError as error:

        print(
            f"[!] Mochkil f wordlist: "
            f"{error}"
        )

        return

    if not words:

        print(
            "[!] Wordlist khawya."
        )

        return

    print(
        f"\n[*] Target: {target}"
    )

    print(
        f"[*] Words: {len(words)}"
    )

    print(
        "[*] Kanbda web scan..."
    )

    found = []
    completed = 0
    total = len(words)

    with ThreadPoolExecutor(
        max_workers=20
    ) as executor:

        futures = [
            executor.submit(
                check_web_path,
                target,
                word
            )
            for word in words
        ]

        for future in as_completed(
            futures
        ):

            completed += 1

            try:

                result = future.result()

            except Exception:

                result = None

            if result:

                found.append(result)

                print(
                    f"\n[+] "
                    f"{result['status']} "
                    f"{result['url']}"
                )

            progress = (
                completed / total
            ) * 100

            print(
                f"\r[*] Progress: "
                f"{completed}/{total} "
                f"({progress:.1f}%)",
                end=""
            )

    print("\n")

    found.sort(
        key=lambda x: x["url"]
    )

    print("=" * 60)
    print("WEB SCAN SALA")
    print("=" * 60)

    print(
        f"Pages/files l9inahom: "
        f"{len(found)}"
    )

    print()


# ============================================================
# NETWORK INFO
# ============================================================

def network_info():

    print("\n" + "=" * 60)
    print("LOCAL NETWORK INFO")
    print("=" * 60)

    try:

        hostname = socket.gethostname()

        print(
            f"Hostname : {hostname}"
        )

        try:

            local_ip = socket.gethostbyname(
                hostname
            )

            print(
                f"Local IP : {local_ip}"
            )

        except socket.gaierror:

            print(
                "Local IP : ma3roufach"
            )

        print(
            "Loopback : 127.0.0.1"
        )

    except socket.error as error:

        print(
            f"[!] Mochkil: {error}"
        )

    print("=" * 60)
    print()


# ============================================================
# FILE ORGANIZER
# ============================================================

def get_file_category(file_path):

    extension = file_path.suffix.lower()

    categories = {
        "Images": {
            ".jpg", ".jpeg", ".png", ".gif", ".bmp",
            ".webp", ".svg", ".ico", ".tiff"
        },
        "Videos": {
            ".mp4", ".mkv", ".avi", ".mov", ".webm",
            ".flv", ".wmv", ".m4v"
        },
        "Audio": {
            ".mp3", ".wav", ".flac", ".aac", ".ogg",
            ".m4a", ".opus"
        },
        "Documents": {
            ".pdf", ".doc", ".docx", ".txt", ".rtf",
            ".odt", ".xls", ".xlsx", ".csv",
            ".ppt", ".pptx", ".odp"
        },
        "Archives": {
            ".zip", ".rar", ".7z", ".tar", ".gz",
            ".bz2", ".xz", ".tar.gz", ".tar.xz"
        },
        "Programs": {
            ".exe", ".msi", ".deb", ".rpm", ".AppImage",
            ".sh", ".bat", ".cmd", ".apk"
        }
    }

    for category, extensions in categories.items():

        if extension in extensions:
            return category

    return "Others"


def unique_destination(destination):

    if not destination.exists():
        return destination

    counter = 1

    while True:

        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_destination = (
            destination.parent / new_name
        )

        if not new_destination.exists():
            return new_destination

        counter += 1


def file_organizer():

    print("\n" + "=" * 60)
    print("FILE ORGANIZER")
    print("=" * 60)

    folder = input(
        "Folder path (matalan ~/Downloads): "
    ).strip()

    if not folder:

        print("[!] Folder khawi.")
        return

    folder_path = Path(folder).expanduser()

    if not folder_path.exists():

        print("[!] Had folder ma kaynach.")
        return

    if not folder_path.is_dir():

        print("[!] Had path machi folder.")
        return

    files = [
        file
        for file in folder_path.iterdir()
        if file.is_file()
    ]

    if not files:

        print("[!] Ma kaynach files f had folder.")
        return

    print(
        f"\n[*] Folder : {folder_path}"
    )

    print(
        f"[*] Files  : {len(files)}"
    )

    confirm = input(
        "Bghiti tbda torganizi files? (y/n): "
    ).strip().lower()

    if confirm != "y":

        print("[*] Operation tlghat.")
        return

    moved = 0

    for file in files:

        category = get_file_category(file)

        category_folder = (
            folder_path / category
        )

        try:

            category_folder.mkdir(
                exist_ok=True
            )

            destination = (
                category_folder / file.name
            )

            destination = unique_destination(
                destination
            )

            file.rename(destination)

            print(
                f"[+] {file.name} -> "
                f"{category}/"
            )

            moved += 1

        except OSError as error:

            print(
                f"[!] Ma9dertch n7rek "
                f"{file.name}: {error}"
            )

    print("\n" + "-" * 60)

    print(
        f"[+] Files torganizaw: {moved}/{len(files)}"
    )

    print(
        "[+] Ma tms7 7ta file."
    )

    print("-" * 60)
    print()


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        banner()

        print(
            "[1] Port Scanner"
        )

        print(
            "[2] Password Strength Checker"
        )

        print(
            "[3] Web Content Discovery"
        )

        print(
            "[4] Local Network Information"
        )

        print(
            "[5] File Organizer"
        )

        print(
            "[6] Exit"
        )

        print()

        choice = input(
            "Choice: "
        ).strip()

        if choice == "1":

            port_scanner()

        elif choice == "2":

            password_checker()

        elif choice == "3":

            web_content_discovery()

        elif choice == "4":

            network_info()

        elif choice == "5":

            file_organizer()

        elif choice == "6":

            print(
                "\nSlam! 👋"
            )

            sys.exit(0)

        else:

            print(
                "[!] Choice ghalat."
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()