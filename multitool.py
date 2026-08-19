#!/usr/bin/env python3

import socket
import string
import math
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from getpass import getpass
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

MAX_THREADS = 50
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
# PORT SCANNER
# ============================================================

def check_port(target_ip, port, timeout=DEFAULT_TIMEOUT):
    """
    Kaychouf wach TCP port مفتوح.
    """

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

        banner = ""

        try:

            sock.sendall(
                b"HEAD / HTTP/1.0\r\n\r\n"
            )

            data = sock.recv(256)

            banner = (
                data.decode(
                    "utf-8",
                    errors="ignore"
                )
                .strip()
                .replace("\r", " ")
                .replace("\n", " ")
            )

        except (
            socket.timeout,
            OSError
        ):
            pass

        return {
            "port": port,
            "service": service,
            "banner": banner[:100]
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
            "Start port khaso يكون بين 1 و 65535."
        )

    if not 1 <= end_port <= 65535:

        raise ValueError(
            "End port khaso يكون بين 1 و 65535."
        )

    if start_port > end_port:

        raise ValueError(
            "Start port ma ymknch يكون "
            "kber mn end port."
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
            file.write(
                "=" * 70 + "\n"
            )

            file.write(
                f"Scan date: "
                f"{datetime.now().isoformat()}\n"
            )

            file.write(
                f"Target: {target}\n"
            )

            file.write(
                f"IP: {target_ip}\n"
            )

            file.write(
                "=" * 70 + "\n"
            )

            for result in results:

                file.write(
                    f"{result['port']}/tcp "
                    f"OPEN "
                    f"Service={result['service']} "
                    f"Banner={result['banner']}\n"
                )

            file.write("\n")

        return True

    except OSError as error:

        print(
            f"[!] Error saving results: {error}"
        )

        return False


def port_scanner():

    print("\n" + "=" * 70)
    print("PORT SCANNER")
    print("=" * 70)

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
            "[!] Ma9dertch nl9a hostname."
        )

        return

    total_ports = (
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
        f"[*] Ports  : {total_ports}"
    )

    print(
        "[*] Scanning..."
    )

    print()

    results = []

    completed = 0

    ports = range(
        start_port,
        end_port + 1
    )

    with ThreadPoolExecutor(
        max_workers=MAX_THREADS
    ) as executor:

        futures = {
            executor.submit(
                check_port,
                target_ip,
                port
            ): port

            for port in ports
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

                results.append(
                    result
                )

                print(
                    f"\n[+] "
                    f"{result['port']}/tcp OPEN"
                )

                print(
                    f"    Service : "
                    f"{result['service']}"
                )

                if result["banner"]:

                    print(
                        f"    Banner  : "
                        f"{result['banner']}"
                    )

            progress = (
                completed /
                total_ports
            ) * 100

            print(
                f"\r[*] Progress: "
                f"{completed}/{total_ports} "
                f"({progress:.1f}%)",
                end=""
            )

    results.sort(
        key=lambda item:
        item["port"]
    )

    print("\n")

    print(
        "=" * 70
    )

    print(
        "SCAN FINISHED"
    )

    print(
        "=" * 70
    )

    print(
        f"Open ports: "
        f"{len(results)}"
    )

    if results:

        print(
            "\nOpen ports:"
        )

        for result in results:

            print(
                f"  "
                f"{result['port']}/tcp "
                f"- "
                f"{result['service']}"
            )

        save_choice = input(
            "\nSave results? (y/n): "
        ).strip().lower()

        if save_choice == "y":

            if save_scan_results(
                target,
                target_ip,
                results
            ):

                print(
                    f"[+] Results saved to "
                    f"{RESULT_FILE}"
                )

    print()


# ============================================================
# PASSWORD ANALYSIS
# ============================================================

def has_sequence(password):

    lower = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "9876543210",
    ]

    for sequence in sequences:

        for size in range(4, 7):

            for index in range(
                len(sequence) - size + 1
            ):

                part = sequence[
                    index:index + size
                ]

                if part in lower:

                    return True

    return False


def has_keyboard_pattern(password):

    lower = password.lower()

    for pattern in KEYBOARD_PATTERNS:

        if pattern in lower:

            return True

    return False


def analyze_password(password):

    length = len(password)

    has_lower = any(
        char in string.ascii_lowercase
        for char in password
    )

    has_upper = any(
        char in string.ascii_uppercase
        for char in password
    )

    has_digit = any(
        char in string.digits
        for char in password
    )

    has_symbol = any(
        char in string.punctuation
        for char in password
    )

    charset_size = 0

    if has_lower:

        charset_size += 26

    if has_upper:

        charset_size += 26

    if has_digit:

        charset_size += 10

    if has_symbol:

        charset_size += len(
            string.punctuation
        )

    if length > 0 and charset_size > 0:

        entropy = (
            length *
            math.log2(charset_size)
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

    sequence = has_sequence(
        password
    )

    keyboard = has_keyboard_pattern(
        password
    )

    return {
        "length": length,
        "lower": has_lower,
        "upper": has_upper,
        "digit": has_digit,
        "symbol": has_symbol,
        "charset": charset_size,
        "entropy": entropy,
        "common": common,
        "repeated": repeated,
        "sequence": sequence,
        "keyboard": keyboard,
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

    print("\n" + "=" * 70)
    print("PASSWORD STRENGTH CHECKER")
    print("=" * 70)

    password = getpass(
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

    print(
        "\n" + "-" * 70
    )

    print(
        f"Length       : "
        f"{result['length']}"
    )

    print(
        f"Lowercase    : "
        f"{'YES' if result['lower'] else 'NO'}"
    )

    print(
        f"Uppercase    : "
        f"{'YES' if result['upper'] else 'NO'}"
    )

    print(
        f"Numbers      : "
        f"{'YES' if result['digit'] else 'NO'}"
    )

    print(
        f"Symbols      : "
        f"{'YES' if result['symbol'] else 'NO'}"
    )

    print(
        f"Entropy      : "
        f"{result['entropy']:.1f} bits"
    )

    print(
        f"Common       : "
        f"{'YES' if result['common'] else 'NO'}"
    )

    print(
        f"Repetition   : "
        f"{'YES' if result['repeated'] else 'NO'}"
    )

    print(
        f"Sequence     : "
        f"{'YES' if result['sequence'] else 'NO'}"
    )

    print(
        f"Keyboard     : "
        f"{'YES' if result['keyboard'] else 'NO'}"
    )

    print(
        "-" * 70
    )

    print(
        f"STRENGTH     : "
        f"{strength}"
    )

    print(
        "-" * 70
    )

    tips = []

    if result["length"] < 12:

        tips.append(
            "Zid f length: "
            "12+ characters."
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
            "Bdel password "
            "7it common."
        )

    if result["sequence"]:

        tips.append(
            "Tjanab sequences "
            "bhal 123456."
        )

    if result["keyboard"]:

        tips.append(
            "Tjanab keyboard "
            "patterns bhal qwerty."
        )

    if result["repeated"]:

        tips.append(
            "Tjanab repetition "
            "kbir."
        )

    print(
        "\nRecommendations:"
    )

    if not tips:

        print(
            "  [+] Password kayban 9awi."
        )

    else:

        for tip in tips:

            print(
                f"  - {tip}"
            )

    print()


# ============================================================
# LOCAL NETWORK INFORMATION
# ============================================================

def network_info():

    print("\n" + "=" * 70)
    print("LOCAL NETWORK INFORMATION")
    print("=" * 70)

    try:

        hostname = socket.gethostname()

        print(
            f"Hostname     : "
            f"{hostname}"
        )

        try:

            local_ip = socket.gethostbyname(
                hostname
            )

            print(
                f"Local IP     : "
                f"{local_ip}"
            )

        except socket.gaierror:

            print(
                "Local IP     : unavailable"
            )

        print(
            "Loopback     : "
            "127.0.0.1"
        )

        try:

            fqdn = socket.getfqdn()

            print(
                f"FQDN         : "
                f"{fqdn}"
            )

        except Exception:

            print(
                "FQDN         : unavailable"
            )

    except socket.error as error:

        print(
            f"[!] Network error: "
            f"{error}"
        )

    print(
        "=" * 70
    )

    print()


# ============================================================
# BANNER
# ============================================================

def banner():

    print("""
======================================================================
                         CYBERSCAN v3
======================================================================

        Educational Cybersecurity Multi-Tool

        [1] Port Scanner
        [2] Password Strength Checker
        [3] Local Network Information
        [4] Exit

======================================================================
""")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        banner()

        choice = input(
            "Choice: "
        ).strip()

        if choice == "1":

            port_scanner()

        elif choice == "2":

            password_checker()

        elif choice == "3":

            network_info()

        elif choice == "4":

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