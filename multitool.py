#!/usr/bin/env python3
"""
Educational Multi-Tool - Python
Fiha: Port Scanner + Password Strength Checker

⚠️ Khddem Port Scanner ghir 3la:
   - L jhaz dyalk lkhas
   - Lab machia lta3lim (bhal scanme.nmap.org, TryHackMe, HackTheBox)
   - Targets fin 3ndk idn ktabi
"""

import socket
import string
import math
import sys


# ============================================================
#  TOOL 1: PORT SCANNER
# ============================================================

def port_scanner():
    print("\n[Port Scanner]")
    target = input("Dkhel IP wla hostname (mtalan scanme.nmap.org): ").strip()
    try:
        start_port = int(input("Port lbidaya (mtalan 20): "))
        end_port = int(input("Port nihaya (mtalan 100): "))
    except ValueError:
        print("[!] Khassek dkhel rakm s7i7.")
        return

    print(f"\n[*] Kanbda nscanni {target} mn port {start_port} l {end_port}...\n")

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("[!] Ma9dertch nl9a l hostname.")
        return

    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"[+] Port {port}/tcp mftou7")
            open_ports.append(port)
        sock.close()

    print(f"\n[*] Scan salat. 3adad dyal ports lmftou7in: {len(open_ports)}")


# ============================================================
#  TOOL 2: PASSWORD STRENGTH CHECKER
# ============================================================

def analyze_password(password: str) -> dict:
    length = len(password)

    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    has_space = " " in password

    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_symbol:
        charset_size += len(string.punctuation)
    if has_space:
        charset_size += 1

    if charset_size > 0 and length > 0:
        entropy = length * math.log2(charset_size)
    else:
        entropy = 0

    # Kanftardo attacker 9ader yjarreb 10 milyar mo7awala/tanya (GPU 7ditha)
    guesses_per_second = 10_000_000_000
    total_combinations = charset_size ** length if charset_size > 0 else 0
    seconds_to_crack = (total_combinations / 2) / guesses_per_second if guesses_per_second > 0 else 0

    # Lista basita dyal passwords cha2i3in bzaf (lta3lim)
    common_passwords = {
        "123456", "password", "123456789", "12345678", "12345",
        "qwerty", "abc123", "password1", "admin", "letmein",
        "welcome", "monkey", "111111", "iloveyou", "azerty"
    }
    is_common = password.lower() in common_passwords

    # Chouf wach kayn tekrar kbir dyal l7oroof (bhal "aaaaaa")
    has_repetition = any(password.count(c) > length * 0.5 for c in set(password)) if length > 0 else False

    return {
        "length": length,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "charset_size": charset_size,
        "entropy_bits": entropy,
        "seconds_to_crack": seconds_to_crack,
        "is_common": is_common,
        "has_repetition": has_repetition,
    }


def format_time(seconds: float) -> str:
    """Kaydir convert dyal tawaniya l siga mafhouma (da9ay9, snin...)"""
    if seconds < 1:
        return "A9el mn tanya"
    elif seconds < 60:
        return f"{seconds:.1f} tanya"
    elif seconds < 3600:
        return f"{seconds/60:.1f} de9i9a"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} sa3a"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} nhar"
    elif seconds < 31536000 * 100:
        return f"{seconds/31536000:.1f} 3am"
    else:
        years = seconds / 31536000
        if years > 1e12:
            return "Blayin dyal snin (mostahil 3ملia)"
        return f"{years:.2e} 3am"


def get_strength_label(analysis: dict) -> tuple:
    entropy = analysis["entropy_bits"]

    if analysis["is_common"]:
        return ("D3ifa bzaf - Password cha2i3a bzaf!", "🔴")
    if analysis["has_repetition"]:
        return ("D3ifa - fiha tekrar kbir", "🔴")
    if entropy < 28:
        return ("D3ifa bzaf", "🔴")
    elif entropy < 36:
        return ("D3ifa", "🟠")
    elif entropy < 60:
        return ("Motawassita", "🟡")
    elif entropy < 100:
        return ("9awya", "🟢")
    else:
        return ("9awya bzaf", "🟢")


def print_password_report(password: str):
    analysis = analyze_password(password)
    label, emoji = get_strength_label(analysis)

    print("\n" + "=" * 55)
    print(f"  Ra9m dyal 9owwa dyal Password")
    print("=" * 55)

    # Wri password mkhbya b jouj dyal l7oroof ghir (aman)
    masked = password[:2] + "*" * (len(password) - 2) if len(password) > 2 else "*" * len(password)
    print(f"  Password (mkhbya): {masked}")
    print(f"  Toul: {analysis['length']} 7arf")
    print("-" * 55)

    print("  No3 l7oroof mosta3mlin:")
    print(f"    - 7oroof sghar (a-z): {'✓' if analysis['has_lower'] else '✗'}")
    print(f"    - 7oroof kbar (A-Z): {'✓' if analysis['has_upper'] else '✗'}")
    print(f"    - Ar9am (0-9): {'✓' if analysis['has_digit'] else '✗'}")
    print(f"    - Rmouz (!@#$...): {'✓' if analysis['has_symbol'] else '✗'}")
    print("-" * 55)

    print(f"  Entropy: {analysis['entropy_bits']:.1f} bits")
    print(f"  We9t lkasr lmoqadar (brute-force): {format_time(analysis['seconds_to_crack'])}")
    print("-" * 55)

    if analysis["is_common"]:
        print("  ⚠️  Tanbih: had password mawjouda f la9wayem dyal l-passwords cha2i3in!")
    if analysis["has_repetition"]:
        print("  ⚠️  Tanbih: fiha tekrar kbir dyal l7oroof")
    if analysis["length"] < 8:
        print("  ⚠️  Tanbih: 9sira bzaf (kanansa7 b 12+ 7arf)")

    print("-" * 55)
    print(f"  Natija nha2iya: {emoji} {label}")
    print("=" * 55)

    tips = []
    if analysis["length"] < 12:
        tips.append("Zid f toul (12+ 7arf a7san)")
    if not analysis["has_upper"]:
        tips.append("Zid 7oroof kbar (A-Z)")
    if not analysis["has_digit"]:
        tips.append("Zid ar9am")
    if not analysis["has_symbol"]:
        tips.append("Zid rmouz (!@#$%...)")
    if analysis["is_common"]:
        tips.append("Bdelha - hadi cha2i3a bzaf")

    if tips:
        print("\n  💡 Nsayeh bach t9awiha:")
        for tip in tips:
            print(f"    - {tip}")
    print()


def password_checker():
    print("\n[Password Strength Checker]")
    pwd = input("Dkhel password (mgadich ttahfad wla ttab3at l7ad): ").strip()
    if not pwd:
        print("[!] Makaynch password.")
        return
    print_password_report(pwd)


# ============================================================
#  MAIN MENU
# ============================================================

def banner():
    print("=" * 50)
    print("   Educational Multi-Tool - Python")
    print("=" * 50)


def main_menu():
    banner()
    while True:
        print("""
Khtar wazifa:
  1) Port Scanner
  2) Password Strength Checker
  3) Khoroj (Exit)
""")
        choice = input("Lekhtiyar dyalk: ").strip()

        if choice == "1":
            port_scanner()
        elif choice == "2":
            password_checker()
        elif choice == "3":
            print("Slam!")
            sys.exit()
        else:
            print("[!] Khtiyar khayb, 3awed.")


if __name__ == "__main__":
    main_menu()