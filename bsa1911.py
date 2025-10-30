import sys
import os
os.system('clear')
import requests
import threading
import time
import json,requests,time
from time import strftime
from pystyle import Colorate, Colors, Write, Add, Center
ZALO = 'https://zalo.me/g/ehnpay312'
ADMIN = 'LDYH'
VERSION = '1.0'
NHV = '\033[1;91m[\033[1;92m●\033[1;91m]\033[1;97m ➻❥'  
def banner():
    print(f''' 
Tool Share Cookie Max Speed
          ''')
t=(Colorate.Horizontal(Colors.white_to_black,"- - - - - - - - - - - - - - - - - - - - - - - - -"))
print(t)
def clear():
    if(sys.platform.startswith('win')):
        os.system('cls')
    else:
        os.system('clear')
gome_token = []
def get_token(input_file):
    for cookie in input_file:
        header_ = {
            'authority': 'business.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'referer': 'https://www.facebook.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',

        }
        try:
            home_business = requests.get('https://business.facebook.com/content_management', headers=header_).text
            token = home_business.split('EAAG')[1].split('","')[0]
            cookie_token = f'{cookie}|EAAG{token}'
            gome_token.append(cookie_token)
        except:
            pass
    return gome_token

def share(tach, id_share):
    cookie = tach.split('|')[0]
    token = tach.split('|')[1]
    he = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'connection': 'keep-alive',
        'content-length': '0',
        'cookie': cookie,
        'host': 'graph.facebook.com'
    }
    try:
        res = requests.post(f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{id_share}&published=0&access_token={token}', headers=he).json()
    except:
        pass
    
    
def main_share():
    clear()
    banner()
    input_file = open(input("\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mNhập tên file chứa Cookies: \033[1;35m")).read().split('\n')
    id_share = input("\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mNhập ID Cần Share: \033[1;35m")
    delay = int(input("\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mNhập Delay Share: \033[1;35m"))
    total_share = int(input("\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mBao Nhiêu Share Thì Dừng Tool: \033[1;35m"))
    all = get_token(input_file)
    total_live = len(all)
    print(f'\033[1;31m────────────────────────────────────────────────────────────')
    if total_live == 0:
        sys.exit()
    stt = 0
    while True:
        for tach in all:
            stt = stt + 1
            threa = threading.Thread(target=share, args=(tach, id_share))
            threa.start()
            print(f'\033[1;91m[\033[1;33m{stt}\033[1;91m]\033[1;31m ❥ \033[1;95mSHARE\033[1;31m ❥\033[1;36m THÀNH CÔNG\033[1;31m ❥ ID ❥\033[1;31m\033[1;93m {id_share} \033[1;31m❥ \n', end='\r')
            time.sleep(delay)
        if stt == total_share:
            break
    gome_token.clear()
    input('\033[38;5;245m[\033[1;32mSUCCESS\033[38;5;245m] \033[1;32mĐã Share Thành Công | Nhấn [Enter] Để Chạy Lại \033[0m\033[0m')
while True:
    try:
        main_share()
    except KeyboardInterrupt:
        print('\n\033[38;5;245m[\033[38;5;9m!\033[38;5;245m] \033[38;5;9mNhớ Đăng Ký Kênh C25 Tool Nhé^^\033[0m')
        sys.exit()print (Colorate.Diagonal(Colors.blue_to_white, "║Tool Tiện Ích   ║"))
print (Colorate.Diagonal(Colors.blue_to_white, "╚════════════════╝"))
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m8.1\033[1;31m] \033[1;35mTOOL DOSS WEB & IP")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m8.2\033[1;31m] \033[1;35mTOOL SPAM SMS")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m8.3\033[1;31m] \033[1;35mTOOL BUFF TIKTOK ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m8.4\033[1;31m] \033[1;35mTOOL REG ACC FB")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m8.5\033[1;31m] \033[1;35mTOOL REG PAGE PR5")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m8.6\033[1;31m] \033[1;35mTOOL REG ACC TTC")

print("\033[1;31m────────────────────────────────────────────────────────────")
print (Colorate.Diagonal(Colors.blue_to_white, "╔════════════════╗"))
print (Colorate.Diagonal(Colors.blue_to_white, "║    Tool DEMO   ║"))
print (Colorate.Diagonal(Colors.blue_to_white, "╚════════════════╝"))
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m9.1\033[1;31m] \033[1;35mTOOL DEMO")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m00\033[1;31m] '\033[1;39mTHOÁT TOOL")

print("\033[1;31m────────────────────────────────────────────────────────────")

chon = str(input('\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;37m: \033[1;33m'))


# -----------------------------------------------------------
# PHẦN SỬA CHỮA CHÍNH BẮT ĐẦU TỪ ĐÂY
# Tất cả 'if' đã được đổi thành 'elif' để tạo thành một khối menu
# -----------------------------------------------------------
## xin phep khanh duy su dung chuc nang thoat tool
if chon == '00' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/thoattool/main/.github/workflows/main.yml').text)
    #tool tđs
elif chon == '1.1' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/td7272stt.py').text)
elif chon == '1.2':
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/td7272stt.py').text)
elif chon == '1.3' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/tdsfb.py').text) 
elif chon == '1.4' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/109tdsig1990.py').text) 
elif chon == '1.00' : 
 exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Mktds/main/4.py').text) 
 #tool spam sms
elif chon == '1.5' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/ttcfb.py').text)
elif chon == '1.6' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/ttctt.py').text)
    #tool đào mail
elif chon == '3.1' :
 exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/scanaolayma81819jsj.py').text)
elif chon == '3.2' :
 exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/getprxy8182zn9ak.py').text)
elif chon == '3.3' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/locproxy9181.py').text)
elif chon == '3.4' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/regalectiffincrane.py').text)
elif chon == '3.5' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/regarena1919.py').text)
    #tool đào&check proxy
elif chon == '4.1' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Checklivedieproxy/main/p.py').text)
elif chon == '4.2' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Check-live-die-DEMO/main/q.py').text)
elif chon == '4.3' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/ChecklivedieDEMO/main/p.py').text)
elif chon == '4.4' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/DaoprxDEMO/main/daoprxDEMO.py').text)
elif chon == '4.5' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/DaoprxDEMO/main/p.py').text)
elif chon == '4.6' :
  exec(requests.get('https://raw.githubusercontent.com/Khanh23047/DaoproxyDEMO/main/p.py').text)
elif chon == '4.7' :   
   exec(requests.get('https://raw.githubusercontent.com/Khanh23047/DaoproxyDEMO/main/p.py').text)
elif chon == '4.8' :  
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/DaoproxyDEMOvip/main/p.py').text)
    #tool en&dec
elif chon == '5.1' :
    exec(requests.get('https://raw.githubusercontent.com/nguyenxuantrinhnotpd/Shenron/refs/heads/main/shenron.py').text)
elif chon == '5.2' :
     exec(requests.get('https://raw.githubusercontent.com/KhanhNguyen9872/kramer-specter_deobf/main/kramer-specter-deobf.py').text)
   #tool golike
elif chon == '6.1' :  
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Golike/main/golike.py').text)
elif chon == '6.2' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Golike-ig/main/p.py').text)
elif chon == '6.3' :
     exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Golike-Twitter-/main/p.py').text)
     #tool idol khác 
elif chon == '7.1' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Tool-vlong/main/p.py').text)
elif chon == '7.2' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Tool-trinh-huong/main/huong.py').text)
elif chon == '7.3' :
	exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Full-mail/main/vietcode_toolmeow.py').text)
elif chon == '7.4' :
  exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Tool-hdt/main/p.py').text)
elif chon == '7.5' :   
   exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Tool-lkz/main/p.py').text)
elif chon == '7.6' :  
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Tool-jray/main/haha.py').text)
elif chon == '7.7' :  
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Beta-tool/main/beta.py').text)
    #tool tiện ích
elif chon == '8.1' :
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/doss.py').text)
elif chon == '8.2' :
     exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Reg-pro5-vip/main/reg.py').text)
elif chon == '8.3' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Rutgonlink/main/10.py').text)
elif chon == '8.4' :
    exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Phanhoilink/main/10.py').text)
elif chon == '8.5' :
	exec(requests.get('https://raw.githubusercontent.com/Khanh23047/L-c-Link-T-File/main/10.py').text)
elif chon == '8.6' :
  exec(requests.get('https://raw.githubusercontent.com/Khanh23047/Reg-fb/main/10.py').text)
  #tool tiện ích 
elif chon == '9.1' :   
   exec(requests.get('https://raw.githubusercontent.com/Khanh23047/May-tinh/main/0.py').text)
else :
    # Khối 'else' này sẽ bắt bất kỳ lựa chọn nào không có trong menu
    print(f"\n{do}[!] Lựa chọn '{chon}' không hợp lệ. Vui lòng chạy lại tool và chọn đúng!{end}")
    sleep(2)
    exit()

