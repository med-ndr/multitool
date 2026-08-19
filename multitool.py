
import socket
import string
import math
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from getpass import getpass


# ============================================================
# PORT SCANNER
# ============================================================

def check_port(target_ip, port, timeout=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "unknown"

            return port, service

    except (socket.timeout, OSError):
        pass

    finally:
        sock.close()

    return None


def port_scanner():

    print("\n" + "=" * 60)
    print("PORT SCANNER")
    print("=" * 60)

    target = input("Target IP/hostname: ").strip()

    try:
        start_port = int(input("Start port: "))
        end_port = int(input("End port: "))
    except ValueError:
        print("[!] Port khaso يكون ra9m.")
        return

    if not (1 <= start_port <= 65535):
        print("[!] Start port khaso يكون بين 1 و 65535.")
        return

    if not (1 <= end_port <= 65535):
        print("[!] End port khaso يكون بين 1 و 65535.")
        return

    if start_port > end_port:
        print("[!] Start port ma ymknch يكون kber mn end port.")
        return

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("[!] Ma9dertch nl9a target.")
        return

    print(f"\n[*] Target : {target}")
    print(f"[*] IP     : {target_ip}")
    print(f"[*] Ports  : {start_port}-{end_port}")
    print("[*] Scanning...\n")

    open_ports = []

    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=50) as executor:

        futures = [
            executor.submit(check_port, target_ip, port)
            for port in ports
        ]

        for future in as_completed(futures):

            result = future.result()

            if result:
                port, service = result

                open_ports.append((port, service))

                print(
                    f"[+] {port}/tcp OPEN"
                    f"    Service: {service}"
                )

    open_ports.sort()

    print("\n" + "-" * 60)
    print(f"[*] Scan salat.")
    print(f"[*] Open ports: {len(open_ports)}")
    print("-" * 60)


# ============================================================
# PASSWORD STRENGTH CHECKER
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
}


def analyze_password(password):

    length = len(password)

    has_lower = any(
        c in string.ascii_lowercase
        for c in password
    )

    has_upper = any(
        c in string.ascii_uppercase
        for c in password
    )

    has_digit = any(
        c in string.digits
        for c in password
    )

    has_symbol = any(
        c in string.punctuation
        for c in password
    )

    charset_size = 0

    if has_lower:
        charset_size += 26

    if has_upper:
        charset_size += 26

    if has_digit:
        charset_size += 10

    if has_symbol:
        charset_size += len(string.punctuation)

    if length > 0 and charset_size > 0:
        entropy = length * math.log2(charset_size)
    else:
        entropy = 0

    common = password.lower() in COMMON_PASSWORDS

    repeated = False

    if length > 0:
        for char in set(password):
            if password.count(char) > length * 0.5:
                repeated = True
                break

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
    }


def get_strength(analysis):

    entropy = analysis["entropy"]

    if analysis["common"]:
        return "VERY WEAK"

    if analysis["repeated"]:
        return "WEAK"

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

    password = getpass("Password: ")

    if not password:
        print("[!] Password khawya.")
        return

    result = analyze_password(password)

    strength = get_strength(result)

    print("\n" + "-" * 60)

    print(f"Length       : {result['length']}")
    print(f"Lowercase    : {'YES' if result['lower'] else 'NO'}")
    print(f"Uppercase    : {'YES' if result['upper'] else 'NO'}")
    print(f"Numbers      : {'YES' if result['digit'] else 'NO'}")
    print(f"Symbols      : {'YES' if result['symbol'] else 'NO'}")
    print(f"Entropy      : {result['entropy']:.1f} bits")
    print(f"Common       : {'YES' if result['common'] else 'NO'}")
    print(f"Repetition   : {'YES' if result['repeated'] else 'NO'}")

    print("-" * 60)
    print(f"STRENGTH     : {strength}")
    print("-" * 60)

    print("\nRecommendations:")

    tips = []

    if result["length"] < 12:
        tips.append("Zid f length, 12+ characters a7san.")

    if not result["lower"]:
        tips.append("Zid lowercase.")

    if not result["upper"]:
        tips.append("Zid uppercase.")

    if not result["digit"]:
        tips.append("Zid numbers.")

    if not result["symbol"]:
        tips.append("Zid symbols.")

    if result["common"]:
        tips.append("Matsta3mlch password cha2i3a.")

    if result["repeated"]:
        tips.append("Tjanab repetition kbir.")

    if not tips:
        print("  [+] Password kayban 9awi.")

    else:
        for tip in tips:
            print(f"  - {tip}")

    print()


# ============================================================
# BANNER
# ============================================================

def banner():

    print("""
============================================================
                    CYBERSCAN v2
============================================================
        Educational Cybersecurity Multi-Tool

        [1] Port Scanner
        [2] Password Strength Checker
        [3] Exit
============================================================
""")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        banner()

        choice = input("Choice: ").strip()

        if choice == "1":

            port_scanner()

        elif choice == "2":

            password_checker()

        elif choice == "3":

            print("\nSlam! 👋")
            sys.exit(0)

        else:

            print("[!] Choice ghalat.")


if __name__ == "__main__":
    main()