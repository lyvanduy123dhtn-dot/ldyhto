import os
import sys
import random
from time import sleep
from pystyle import Colors, Colorate
import requests
# Lưu ý: Các thư viện bên ngoài (pystyle, rich) cần được cài đặt nếu chạy bên ngoài môi trường đã có.

# --- KHAI BÁO MÀU SẮC ANSI ---
# ANSI color codes
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
tim = '\033[1;39m'
hong = "\033[1;35m"
trang = "\033[1;37m"
whiteb = "\033[1;37m"
red = "\033[0;31m"
redb = "\033[1;31m"
end = '\033[0m'

# List of main colors for randomization
RANDOM_COLORS = [xnhac, do, luc, vang, xduong, hong]

def get_random_color():
    """Returns a random ANSI color code from the main color list."""
    return random.choice(RANDOM_COLORS)

def banner():
    """Hiển thị banner với hiệu ứng màu ngẫu nhiên và hiệu ứng gõ chữ."""
    # os.system("cls" if os.name == "nt" else "clear") # Giữ lại comment để tránh xóa màn hình trong một số môi trường
    
    # Tạo một danh sách màu ngẫu nhiên cho 6 dòng banner ASCII art
    COLORS_LIST = [luc, vang, do, hong, xnhac, xduong]
    random.shuffle(COLORS_LIST)
    
    c1, c2, c3, c4, c5, c6 = COLORS_LIST[0], COLORS_LIST[1], COLORS_LIST[2], COLORS_LIST[3], COLORS_LIST[4], COLORS_LIST[5]
    
    # Áp dụng chuỗi màu ngẫu nhiên theo mô hình tuần hoàn cho từng segment
    banner_ascii = f"""
{c1}██╗░░░░░{c2}██████╗░{c3}██╗░░░██╗{c4}██╗░░██╗{end}  {c5}████████╗░{c6}█████╗░░{c1}█████╗░{c2}██╗░░░░░
{c3}██║░░░░░{c4}██╔══██╗{c5}╚██╗░██╔╝{c6}██║░░██║{end}  {c1}╚══██╔══╝{c2}██╔══██╗{c3}██╔══██╗{c4}██║░░░░░
{c5}██║░░░░░{c6}██║░░██║{c1}░╚████╔╝░{c2}███████║{end}  {c3}░░░██║░░░{c4}██║░░██║{c5}██║░░██║{c6}██║░░░░░
{c1}██║░░░░░{c2}██║░░██║{c3}░░╚██╔╝░░{c4}██╔══██║{end}  {c5}░░░██║░░░{c6}██║░░██║{c1}██║░░██║{c2}██║░░░░░
{c3}███████╗{c4}██████╔╝{c5}░░░██║░░░{c6}██║░░██║{end}  {c1}░░░██║░░░{c2}╚█████╔╝{c3}╚█████╔╝{c4}███████╗
{c5}╚══════╝{c6}╚═════╝░{c1}░░░╚═╝░░░{c2}╚═╝░░╚═╝{end}  {c3}░░░╚═╝░░░{c4}░╚════╝░░{c5}╚════╝░{c6}╚══════╝\n
"""
    
    INFO_COLOR = get_random_color()
    
    # Information section using random colors
    banner_info = f"""{trang}Tool By: {INFO_COLOR}Let’s Do Your Hack 💻 {end}           {trang}Phiên Bản: {INFO_COLOR}DEMO{end}    
{trang}════════════════════════════════════════════════{end}  
{trang}[{do}<>{trang}]{hong} BOX ZALO{do} : {xnhac}https://zalo.me/g/ehnpay312{end}
{trang}[{do}<>{trang}]{vang} YOUTUBE{do} : {luc}Let’s Do Your Hack{end} 
{trang}[{do}<>{trang}]{luc} ADMIN{do} : {xduong}LŸ VÄN DÜY{end}

{trang}════════════════════════════════════════════════{end}  
"""
    full_banner = banner_ascii + banner_info
    
    # Typing effect
    for X in full_banner:
        sys.stdout.write(X)
        sys.stdout.flush()
        sleep(0.00125)

os.system("cls" if os.name == "nt" else "clear")
banner()
print("\033[1;31m────────────────────────────────────────────────────────────")
print (Colorate.Diagonal(Colors.blue_to_white, "╔═════════════════════╗"))
print (Colorate.Diagonal(Colors.blue_to_white, "║  Tool TDS & TTC     ║"))
print (Colorate.Diagonal(Colors.blue_to_white, "╚═════════════════════╝"))

print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.1\033[1;31m] \033[1;35mTDS TIKTOK \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.2\033[1;31m] \033[1;35mTDS TIKTOK \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.3\033[1;31m] \033[1;35mTDS FACEBOOK")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.4\033[1;31m] \033[1;35mTDS INSTAGRAM")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.5\033[1;31m] \033[1;35mTTC FACEBOOK FULL JOB \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.6\033[1;31m] \033[1;35mTTC TIKTOK \033[1;33m[\033[1;31mDEMO\033[1;33m] ")

print("\033[1;31m────────────────────────────────────────────────────────────")
print (Colorate.Diagonal(Colors.blue_to_white, "╔═════════════════════╗"))
print (Colorate.Diagonal(Colors.blue_to_white, "║  Tool MAIL & Proxy  ║"))
print (Colorate.Diagonal(Colors.blue_to_white, "╚═════════════════════╝"))
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m3.1\033[1;31m] \033[1;35mTOOL SCAN MAIL LẤY MÃ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m3.2\033[1;31m] \033[1;35mTOOL GET PROXY")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m3.3\033[1;31m] \033[1;35mTOOL LỌC PROXY")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m3.4\033[1;31m] \033[1;35mTOOL REG MAIL.TM")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m3.5\033[1;31m] \033[1;35mTOOL REG ACC GARENA")

print("\033[1;31m────────────────────────────────────────────────────────────")
print (Colorate.Diagonal(Colors.blue_to_white, "╔═════════════════════════╗"))
print (Colorate.Diagonal(Colors.blue_to_white, "║     Tool DEMO           ║"))
print (Colorate.Diagonal(Colors.blue_to_white, "╚═════════════════════════╝"))
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m4.1\033[1;31m] \033[1;35mTOOL DEMO \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m4.2\033[1;31m] \033[1;35mTOOL DEMO \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m4.3\033[1;31m] \033[1;35mTOOL DEMO \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m4.4\033[1;31m] \033[1;35mTOOL DEMO \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m4.5\033[1;31m] \033[1;35mTOOL DEMO \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m4.6\033[1;31m] \033[1;35mTOOL DEMO \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m4.7\033[1;31m] \033[1;35mTOOL DEMO \033[1;33m[\033[1;31mDEMO\033[1;33m] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m4.8\033[1;31m] \033[1;35mTOOL DEMO \033[1;33m[\033[1;31mDEMO\033[1;33m] ")

print("\033[1;31m────────────────────────────────────────────────────────────")
print (Colorate.Diagonal(Colors.blue_to_white, "╔═════════════════════════╗"))
print (Colorate.Diagonal(Colors.blue_to_white, "║Tool ENC & DEC CỦA IDOL  ║"))
print (Colorate.Diagonal(Colors.blue_to_white, "╚═════════════════════════╝"))
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m5.1\033[1;31m] \033[1;35mTOOL EC shenron_obfuscator by NXT")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m5.2\033[1;31m] \033[1;35mTOOL DEC Kramer-Specter_Deobf (khanhduy)")
print("\033[1;31m────────────────────────────────────────────────────────────")
print (Colorate.Diagonal(Colors.blue_to_white, "╔═════════════════════════╗"))
print (Colorate.Diagonal(Colors.blue_to_white, "║      Tool GOLIKE        ║"))
print (Colorate.Diagonal(Colors.blue_to_white, "╚═════════════════════════╝"))
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m6.1\033[1;31m] \033[1;35mTOOL Auto TikTok")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m6.2\033[1;31m] \033[1;35mTOOL Auto Instagram ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m6.3\033[1;31m] \033[1;35mTOOL Auto Twitter")

print("\033[1;31m────────────────────────────────────────────────────────────")
print (Colorate.Diagonal(Colors.blue_to_white, "╔═════════════════════════╗"))
print (Colorate.Diagonal(Colors.blue_to_white, "║     Tool Profile        ║"))
print (Colorate.Diagonal(Colors.blue_to_white, "╚═════════════════════════╝"))
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m7.1\033[1;31m] \033[1;35mBuff Share ảo [Cookie] ")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m7.2\033[1;31m] \033[1;35mTOOL LẤY TOKEN FB")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m7.3\033[1;31m] \033[1;35mTOOL LẤY ID TK & BÀI VIẾT")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m7.4\033[1;31m] \033[1;35mTOOL NUÔI FB")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m7.5\033[1;31m] \033[1;35mTOOL GET COOKIE FB")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;35mNhập\033[1;36m Số \033[1;31m[\033[1;33m7.6\033[1;31m] \033[1;35mTOOL WAR MESS")

print("\033[1;31m────────────────────────────────────────────────────────────")
print (Colorate.Diagonal(Colors.blue_to_white, "╔════════════════╗"))
print (Colorate.Diagonal(Colors.blue_to_white, "║Tool Tiện Ích   ║"))
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
    exec(requests.get('https://raw.githubusercontent.com/lyvanduy123dhtn-dot/ldyhto/main/bsa1911.py').text)
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

