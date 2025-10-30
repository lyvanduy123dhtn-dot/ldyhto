import requests
from concurrent.futures import ThreadPoolExecutor
import os
import time
from time import sleep

# =================== Hiệu ứng cầu vồng ===================
def rainbow_text(text, delay=0.05, repeat=3):
    colors = [
        "\033[31m",  # đỏ
        "\033[33m",  # vàng
        "\033[32m",  # xanh lá
        "\033[36m",  # xanh dương nhạt
        "\033[34m",  # xanh dương
        "\033[35m",  # tím
    ]
    for _ in range(repeat):
        for color in colors:
            os.system("cls" if os.name == "nt" else "clear")
            print(f"{color}\n\n\t\t██╗      ██████╗ ██╗   ██╗██╗  ██╗    \n\t\t██║     ██╔═══██╗██║   ██║██║ ██╔╝    \n\t\t██║     ██║   ██║██║   ██║█████╔╝     \n\t\t██║     ██║   ██║██║   ██║██╔═██╗     \n\t\t███████╗╚██████╔╝╚██████╔╝██║  ██╗    \n\t\t╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    \n")
            print(f"\t\t\033[1;97mADMIN : {color}LDYH PRO\n")
            time.sleep(delay)

# =================== Hàm clear ===================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# =================== Hiệu ứng gõ chậm ===================
def slow_type(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

# =================== Bắt đầu chạy ===================
sleep(1)
rainbow_text("ADMIN : LDYH PRO", delay=0.15, repeat=2)
clear()
print("\033[1;37m >> TOOL LỌC PROXY - LDYH PRO <<\n")

# =================== Chương trình chính ===================
proxy_file = input("\033[1;32m Nhập file chứa Proxy: \033[1;33m").strip()
with open(proxy_file, 'r') as f:
    proxy_list = [x.strip() for x in f if x.strip()]
    proxy_count = len(proxy_list)

save_file = input("\033[1;31m Nhập file để lưu Proxy Live: \033[1;37m").strip()
slow_type(f"\033[1;31mĐã tìm thấy \033[1;37m{proxy_count} \033[1;31mproxy.\n")

def check_proxy(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
        if response.ok:
            ip = proxy.split(':')[0]
            info = requests.get(f"http://ip-api.com/json/{ip}").json()
            country = info.get('country', 'Unknown')
            city = info.get('city', 'Unknown')
            print(f"\033[1;32m[LIVE]\033[1;37m {proxy} \033[1;36m• {country}/{city}")
            with open(save_file, 'a', encoding='utf-8') as f:
                f.write(proxy + '\n')
        else:
            print(f"\033[1;31m[BAD]\033[1;37m {proxy}")
    except Exception:
        pass

print("\033[1;37mĐang kiểm tra proxy...\n")
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(check_proxy, proxy_list)

print(f"\n\033[1;32mHoàn tất! Proxy live đã lưu tại: \033[1;37m{save_file}")
input("\nNhấn Enter để thoát... ")
