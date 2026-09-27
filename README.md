# CyberScan — Cybersecurity Multi-Tool (ver 4.0.0)

*[English below / الانجليزية تحت]*

---

## 🇲🇦 بالعربية

سكريبت بسيط بلغة Python كيجمع 5 أدوات ديال الأمن المعلوماتي والشبكات، الكل فواجهة (menu) وحدة فالـ terminal.

### المميزات

1. **Port Scanner** — كيسكان مجموعة ديال البورتات (ports) فـ IP أو hostname معين (multi-threaded)، وكيوريك كل port مفتوح مع الخدمة (service) المرتبطة بيه.
2. **Password Strength Checker** — كيحلل password (الطول، الحروف الكبيرة والصغيرة، الأرقام، الرموز، entropy)، وكيكتشف الباسوردات الشائعة، أنماط الكيبورد (`qwerty`...)، السلاسل المتسلسلة (`123456`...) والتكرار، ومن بعد كيعطيك تقييم (VERY WEAK → VERY STRONG) مع نصائح باش تحسن الباسورد ديالك.
3. **Web Content Discovery** — بحال أداة gobuster/dirbuster صغيرة: كيدير طلب GET لكل كلمة فوردليست (wordlist) باش يكتشف الملفات والمجلدات الموجودة فموقع معين (بناءً على status codes بحال 200، 301، 403...).
4. **Local Network Info** — كيوريك hostname و local IP ديال الجهاز.
5. **File Organizer** — كينظم أوتوماتيكيا الملفات فمجلد معين (بحال Downloads) حسب النوع (صور، فيديوهات، صوت، مستندات، أرشيف، برامج، أخرى).

### المتطلبات

- Python 3.8 أو أكثر
- ماخصكش تزيد أي library، كولشي standard library (`socket`, `urllib`, `concurrent.futures`, `pathlib`...)

### التثبيت

```bash
git clone https://github.com/med-ndr/multitool.git
cd cyberscan
python3 cyberscan.py
```

### الاستعمال

```bash
python3 cyberscan.py
```

غادي يبان ليك هاد المنيو:

```
[1] Port Scanner
[2] Password Strength Checker
[3] Web Content Discovery
[4] Local Network Information
[5] File Organizer
[6] Exit
```

اختار رقم وتبع التعليمات (target، ports، wordlist path...).

**ملاحظة على Web Content Discovery:** خاصك تكون عندك wordlist (ملف `.txt`، كلمة فكل سطر). كاينين wordlists جاهزين فـ [SecLists](https://github.com/danielmiessler/SecLists).

### النتائج

- Port Scanner: كيمكن تسجل النتائج فملف `scan_results.txt` (append mode).
- Password Checker / Web Discovery / Network Info: النتائج كتبان غير فالـ terminal.
- File Organizer: كيخلق subfolders (Images, Videos...) وكينقل الملفات ليهم.

### ⚠️ تنبيه مهم

هاد الأداة (خصوصا Port Scanner و Web Content Discovery) خاصها تتستعمل غير على targets اللي عندك الإذن باش تختبرهم (ديالك الشخصية، أو فإطار CTF/lab/pentest بموافقة). استعمالها على أنظمة أو شبكات ما عندكش الإذن باش تختبرها ممنوع وممكن يكون مخالف للقانون.

---

## 🇬🇧 English

A simple Python script that bundles 5 security/networking utilities into a single CLI menu.

### Features

1. **Port Scanner** — scans a port range on a target IP/hostname (multi-threaded), showing each open port along with its detected service.
2. **Password Strength Checker** — analyzes a password (length, upper/lowercase, digits, symbols, entropy), detects common passwords, keyboard patterns (`qwerty`, etc.), sequences (`123456`, etc.) and character repetition, then gives a rating (VERY WEAK → VERY STRONG) with improvement tips.
3. **Web Content Discovery** — a mini gobuster/dirbuster: sends a GET request for every word in a wordlist to find folders/files on a target site (based on status codes like 200, 301, 403, etc.).
4. **Local Network Info** — shows the machine's hostname and local IP address.
5. **File Organizer** — automatically organizes files in a folder (e.g. Downloads) by category (Images, Videos, Audio, Documents, Archives, Programs, Others).

### Requirements

- Python 3.8+
- No extra libraries needed — everything is standard library (`socket`, `urllib`, `concurrent.futures`, `pathlib`, etc.)

### Installation

```bash
git clone https://github.com/med-ndr/multitool.git
cd cyberscan
python3 cyberscan.py
```

### Usage

```bash
python3 cyberscan.py
```

You'll see this menu:

```
[1] Port Scanner
[2] Password Strength Checker
[3] Web Content Discovery
[4] Local Network Information
[5] File Organizer
[6] Exit
```

Pick a number and follow the prompts (target, ports, wordlist path, etc.).

**Note on Web Content Discovery:** you'll need a wordlist (a `.txt` file, one word per line) to test against. Ready-made wordlists are available on [SecLists](https://github.com/danielmiessler/SecLists).

### Output

- Port Scanner: optionally saves results to `scan_results.txt` (append mode).
- Password Checker / Web Discovery / Network Info: results are printed to the terminal only.
- File Organizer: creates subfolders (Images, Videos, ...) and moves files into them.

### ⚠️ Disclaimer

This tool (particularly the port scanner and web content discovery modules) should only be used against targets you own or have explicit authorization to test (personal systems, or a CTF/lab/pentest engagement with proper consent). Using it against systems or networks you don't have permission to test is prohibited and may be illegal.

