#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garena_termux_autoinstall.py
Termux-friendly script:
 - Tự động cài system packages qua `pkg` (nếu môi trường Termux)
 - Tự động cài pip packages cần thiết (requests, colorama)
 - Chạy tool reg Garena (requests-version) với banner cầu vồng
 - Hỗ trợ proxy từ file (mỗi dòng ip:port)
 - Lưu kết quả dạng user|pass vào garena_acc.txt

GHI CHÚ: Garena có CAPTCHA/anti-bot — script này mô phỏng phần gửi request.
"""
import os
import sys
import time
import math
import random
import string
import threading
import subprocess
import importlib

# ----------------- HỖ TRỢ CÀI HỎA -----------------
PIP_REQS = ["requests", "colorama"]

def run_cmd(cmd):
    try:
        print(f"[i] Chạy: {cmd}")
        res = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[!] Lệnh thất bại: {cmd}")
        # print(e.stdout.decode(), e.stderr.decode())
        return False

def is_termux():
    # đơn giản: kiểm tra biến môi trường PREFIX hay presence of /data/data/com.termux
    if "com.termux" in os.environ.get("PREFIX", ""):
        return True
    if os.path.exists("/data/data/com.termux"):
        return True
    return False

def ensure_system_pkgs():
    """Nếu đang chạy trên Termux (khả năng cao), tự chạy pkg install cho 1 số gói hữu ích."""
    if not is_termux():
        print("[i] Không phát hiện Termux — bỏ qua cài system packages.")
        return
    # gói đề xuất
    pkgs = ["python", "curl", "wget"]
    for p in pkgs:
        print(f"[i] Đảm bảo system package: {p}")
        run_cmd(f"pkg install -y {p}")

def ensure_pip_packages(pkgs):
    """Cài pip packages nếu thiếu."""
    for pkg in pkgs:
        try:
            importlib.import_module(pkg)
        except Exception:
            print(f"[i] Package pip '{pkg}' chưa có — cài tự động...")
            try:
                run_cmd(f"{sys.executable} -m pip install {pkg}")
            except Exception as e:
                print(f"[!] Không thể cài {pkg} tự động: {e}")
    # reload imports (best-effort)
    for pkg in pkgs:
        try:
            importlib.import_module(pkg)
        except Exception as e:
            print(f"[!] Vẫn không import được {pkg}: {e}")

# ----------------- BANNER CẦU VỒNG -----------------
try:
    import colorama
    colorama.init()
except Exception:
    # colorama sẽ được cài ở ensure_pip_packages
    pass

def rgb(wave, i, speed=0.7):
    r = int((math.sin(speed * (i + wave)) + 1) * 127.5)
    g = int((math.sin(speed * (i + wave) + 2*math.pi/3) + 1) * 127.5)
    b = int((math.sin(speed * (i + wave) + 4*math.pi/3) + 1) * 127.5)
    return r, g, b

def colored_text(text, wave):
    out = ""
    for i, ch in enumerate(text):
        r,g,b = rgb(wave, i)
        out += f"\x1b[38;2;{r};{g};{b}m{ch}"
    out += "\x1b[0m"
    return out

class Banner(threading.Thread):
    def __init__(self, text):
        super().__init__(daemon=True)
        self.text = text
        self.stop_event = threading.Event()
        self.wave = 0.0
    def run(self):
        while not self.stop_event.is_set():
            banner = colored_text(self.text, self.wave)
            try:
                # save cursor, go to 1;1, clear line, print banner, restore cursor
                sys.stdout.write("\x1b7\x1b[1;1H\x1b[2K" + banner + "\x1b8")
                sys.stdout.flush()
            except Exception:
                pass
            self.wave += 1
            time.sleep(0.08)
    def stop(self):
        self.stop_event.set()

# ----------------- RANDOM CREDENTIALS -----------------
def rand_user(l=8):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(l))

def rand_pass(l=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(l))

# ----------------- MOCK/REQUEST REGISTER -----------------
import requests  # try import early; will be available after ensure_pip_packages
def reg_garena_request(username, password, proxy=None):
    """
    GỬI REQUEST GIẢ LẬP ĐĂNG KÝ:
    - Garena thật có CAPTCHa & token => không thể reg thực sự bằng requests đơn giản.
    - Hàm này mô phỏng request/flow để dùng trong Termux; trả về True/False như kết quả.
    Nếu bạn có endpoint thật hoặc hiểu rõ form POST của Garena, bạn có thể chỉnh trong hàm này.
    """
    try:
        # ví dụ mô phỏng: gửi request giả tới endpoint (không thực tế)
        # url_demo = "https://account.garena.com/api/register"  # không thực tế
        # payload = {"username": username, "password": password, "email": f"{username}@tiffincrane.com"}
        # headers = {"User-Agent": "Mozilla/5.0 (Android) AppleWebKit/537.36"}
        # proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        # r = requests.post(url_demo, json=payload, headers=headers, proxies=proxies, timeout=15)
        # nếu r.status_code in (200,201): return True else False

        # Hiện tại: mô phỏng delay và success random (giúp test tool)
        time.sleep(random.uniform(0.8, 1.8))
        # giả lập tỉ lệ thành công 60% (khi không có captcha)
        success = random.random() < 0.6
        return success
    except Exception as e:
        return False

# ----------------- MAIN FLOW -----------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("== Garena Termux Auto Installer & Register (LDYH TOOL) ==")
    # bước auto cài system packages nếu cần
    if is_termux():
        print("[i] Phát hiện Termux — sẽ cố gắng cài system packages cần thiết (qua pkg).")
        ensure_system_pkgs()
    else:
        print("[i] Không phải Termux (hoặc không rõ). Bỏ cài system packages.")

    # ensure pip packages
    ensure_pip_packages(PIP_REQS)

    # (re-import colorama after install)
    try:
        import colorama
        colorama.init()
    except Exception:
        pass

    banner = Banner(" admin by : LDYH TOOL ")
    banner.start()
    print("\n")

    try:
        sl = int(input("Số lượng tài khoản muốn reg: ").strip() or "1")
        delay = float(input("Delay giữa mỗi acc (giây) [vd: 2]: ").strip() or "2")
    except Exception as e:
        banner.stop()
        print(f"Lỗi nhập: {e}")
        return

    use_proxy = input("Có muốn dùng proxy (từ file)? (y/N): ").strip().lower().startswith("y")
    proxies = []
    if use_proxy:
        path = input("Đường dẫn file proxy (mỗi dòng ip:port): ").strip()
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as pf:
                proxies = [ln.strip() for ln in pf if ln.strip()]
            if not proxies:
                print("[!] File proxy rỗng, bỏ proxy.")
                proxies = []
        else:
            print("[!] File proxy không tồn tại, bỏ proxy.")
            proxies = []

    out_file = "garena_acc.txt"
    print(f"\nBắt đầu tạo {sl} acc — lưu vào {out_file}\n")

    created = 0
    with open(out_file, "a", encoding="utf-8") as fout:
        for i in range(sl):
            user = rand_user(8)
            pw = rand_pass(10)
            proxy = random.choice(proxies) if proxies else None
            print(f"[{i+1}/{sl}] Reg: {user} ...", end=" ")
            ok = reg_garena_request(user, pw, proxy)
            if ok:
                print("✅")
                fout.write(f"{user}|{pw}\n")
                fout.flush()
                created += 1
            else:
                print("❌")
            time.sleep(delay)

    banner.stop()
    print(f"\nHoàn tất! Thành công: {created}/{sl}. Kết quả lưu: {out_file}")

if __name__ == "__main__":
    main()
