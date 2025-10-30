#!/usr/bin/env python3
"""
mailtm_batch_create_rainbow_continuous.py
Interactive Mail.tm batch register tool with continuous rainbow banner (top line).
Outputs: email,password  (TXT)

Run:
    python mailtm_batch_create_rainbow_continuous.py
"""

import os
import sys
import time
import math
import random
import string
import requests
import threading
from datetime import datetime

# ---------------- Config ----------------
API_BASE = "https://api.mail.tm"
DEFAULT_DOMAIN = "tiffincrane.com"
BANNER_TEXT = " admin by : LDYH TOOL "
# banner thread settings
BANNER_FPS = 12            # frames per second for banner animation (higher = smoother, more CPU)
BANNER_AMPLITUDE = 0.7     # affects color wave speed
# ----------------------------------------

# Enable colorama on Windows for ANSI support
try:
    import colorama
    colorama.init()
except Exception:
    pass

# Simple helper to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Truecolor rainbow calculation
def rgb(wave, i, speed=0.7):
    r = int((math.sin(speed * (i + wave)) + 1) * 127.5)
    g = int((math.sin(speed * (i + wave) + 2*math.pi/3) + 1) * 127.5)
    b = int((math.sin(speed * (i + wave) + 4*math.pi/3) + 1) * 127.5)
    return r, g, b

def colored_text_truecolor(text, wave):
    out = ""
    for i, ch in enumerate(text):
        r,g,b = rgb(wave, i, speed=BANNER_AMPLITUDE)
        out += f"\x1b[38;2;{r};{g};{b}m{ch}"
    out += "\x1b[0m"
    return out

# Banner runner (runs in background thread)
class BannerThread(threading.Thread):
    def __init__(self, text, fps=12):
        super().__init__(daemon=True)
        self.text = text
        self.fps = fps
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self.wave = 0.0

    def stop(self):
        self._stop.set()
        # small pause so last frame clears appropriately
        time.sleep(0.02)

    def run(self):
        interval = 1.0 / max(1, self.fps)
        try:
            while not self._stop.is_set():
                with self._lock:
                    # Save cursor, move to top-left, write banner, clear rest of line, restore cursor
                    # \x1b[s save cursor pos, \x1b[u restore
                    # \x1b[1;1H move to line 1 col 1
                    banner = colored_text_truecolor(self.text, self.wave)
                    sys.stdout.write("\x1b7")                # save cursor
                    sys.stdout.write("\x1b[1;1H")           # go to line 1, col 1
                    sys.stdout.write("\x1b[2K")             # clear entire line
                    sys.stdout.write(banner)                # print banner
                    sys.stdout.write("\x1b[0K")             # clear to end (safety)
                    sys.stdout.write("\x1b8")                # restore cursor
                    sys.stdout.flush()
                    # advance wave
                    self.wave += 0.9
                time.sleep(interval)
        except Exception:
            # don't crash main if banner fails
            pass
        finally:
            # On exit, clear banner line
            try:
                sys.stdout.write("\x1b7\x1b[1;1H\x1b[2K\x1b8")
                sys.stdout.flush()
            except Exception:
                pass

# ---------------- Password & account helpers ----------------
def random_localpart(length=8):
    chars = string.ascii_lowercase + string.digits + "._"
    s = "".join(random.choice(chars) for _ in range(length))
    s = s.strip("._")
    if not s:
        s = "user" + "".join(random.choice(string.digits) for _ in range(4))
    return s

def generate_password(length=12, use_symbols=False):
    if length < 4:
        length = 4
    lower = random.choice(string.ascii_lowercase)
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    symbols = "!@#$%^&*()-_=+[]{}<>?,./"
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    if use_symbols:
        chars += symbols
    pw = [lower, upper, digit]
    if use_symbols:
        pw.append(random.choice(symbols))
    while len(pw) < length:
        pw.append(random.choice(chars))
    random.shuffle(pw)
    return "".join(pw)

def create_account(address, password, timeout=15):
    url = f"{API_BASE}/accounts"
    payload = {"address": address, "password": password}
    try:
        return requests.post(url, json=payload, timeout=timeout)
    except requests.RequestException:
        return None

# ---------------- Main ----------------
def main():
    clear_screen()
    # Start banner thread (it will print on the top line continuously)
    banner = BannerThread(BANNER_TEXT, fps=BANNER_FPS)
    banner.start()

    # Print a small spacer so input starts on line 3 (banner uses line 1)
    # We ensure the cursor is below banner
    print("\n")  # line 2 blank

    try:
        # Interactive inputs (normal prints will appear below the banner)
        while True:
            try:
                count = int(input("Số lượng acc muốn reg: ").strip() or "0")
            except ValueError:
                print("Nhập số hợp lệ.")
                continue
            if count <= 0:
                print("Số lượng phải > 0. Thoát.")
                banner.stop()
                return
            break

        try:
            delay = float(input("Delay giữa mỗi lần reg (giây) [vd: 1.0]: ").strip() or "1.0")
            if delay < 0:
                delay = 1.0
        except ValueError:
            delay = 1.0

        domain_input = input(f"Domain (mặc định: {DEFAULT_DOMAIN}) — Enter để dùng mặc định: ").strip()
        domain = domain_input if domain_input else DEFAULT_DOMAIN

        try:
            pw_len = int(input("Độ dài mật khẩu [mặc định 12]: ").strip() or "12")
        except ValueError:
            pw_len = 12
        sym_choice = input("Bao gồm ký tự đặc biệt trong mật khẩu? (y/N): ").strip().lower()
        use_symbols = sym_choice == 'y'

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_filename = f"mailtm_accounts_{timestamp}.txt"

        print(f"\nBắt đầu tạo {count} tài khoản — domain mặc định: @{domain}")
        print(f"Kết quả sẽ lưu vào: {out_filename}")
        print("Nhấn Ctrl+C để dừng thủ công.\n")

        created = 0
        attempts = 0

        with open(out_filename, "w", encoding="utf-8") as fout:
            while created < count:
                attempts += 1
                local_len = random.randint(6,10)
                local = random_localpart(local_len)
                address = f"{local}@{domain}"
                password = generate_password(length=pw_len, use_symbols=use_symbols)

                resp = create_account(address, password)
                if resp is None:
                    print(f"[!] Lỗi kết nối khi tạo {address} (attempt {attempts}). Đợi {delay}s và thử lại...")
                    time.sleep(delay)
                    continue

                if resp.status_code in (201, 200):
                    # store only email,password
                    fout.write(f"{address},{password}\n")
                    fout.flush()
                    created += 1
                    print(f"[{created}/{count}] Created: {address}")
                else:
                    text = resp.text if hasattr(resp, "text") else str(resp)
                    print(f"[!] Failed ({resp.status_code}) tạo {address}: {text}")
                    if domain != DEFAULT_DOMAIN:
                        print("    [i] Domain bạn nhập có thể không được mail.tm hỗ trợ. Thử lại với mặc định hoặc để trống.")
                    else:
                        print("    [i] Nếu domain mặc định bị từ chối, cân nhắc đổi domain hoặc để mail.tm chọn domain tự động.")
                time.sleep(delay)

        print(f"\nHoàn tất. Tổng tạo thành công: {created}. File: {out_filename}")

    except KeyboardInterrupt:
        print("\nĐã dừng bằng Ctrl+C.")
    finally:
        # stop banner thread cleanly
        banner.stop()
        # wait a moment for banner to clear top line
        time.sleep(0.05)

if __name__ == "__main__":
    main()
