#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
import time
from datetime import datetime
import base64
import re
import uuid
import random
from bs4 import BeautifulSoup
import sys

# ==============================================================================
# SECTION: UI & COLORS
# ==============================================================================

class UI:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;46m'
    YELLOW = '\033[38;5;226m'
    BLUE = '\033[38;5;39m'
    PURPLE = '\033[38;5;135m'
    CYAN = '\033[38;5;51m'
    ORANGE = '\033[38;5;208m'
    WHITE = '\033[38;5;255m'
    GREY = '\033[38;5;240m'

    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'

    RAINBOW_COLORS = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 51, 45, 39, 33, 27, 57, 93, 129, 165, 201]

    @staticmethod
    def banner():
        os.system('cls' if os.name == 'nt' else 'clear')
        logo = """
████████╗██████╗ ███████╗    ████████╗ ██████╗  ██████╗ ██╗     
╚══██╔══╝██╔══██╗██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
   ██║   ██║  ██║███████╗       ██║   ██║   ██║██║   ██║██║     
   ██║   ██║  ██║╚════██║       ██║   ██║   ██║██║   ██║██║     
   ██║   ██████╔╝███████║       ██║   ╚██████╔╝╚██████╔╝███████╗
   ╚═╝   ╚═════╝ ╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
        """
        colored_logo = ""
        c_idx = 0
        for char in logo:
            if char != " " and char != "\n":
                colored_logo += f"\033[38;5;{UI.RAINBOW_COLORS[c_idx % len(UI.RAINBOW_COLORS)]}m{char}"
                c_idx += 1
            else:
                colored_logo += char

        print(colored_logo + UI.RESET)
        print(f"{UI.BOLD}{UI.WHITE}──────────────────────────────────────────────────────────{UI.RESET}")
        print(f"{UI.YELLOW} Author   : {UI.WHITE}H-Tool 2025")
        print(f"{UI.YELLOW} Server   : {UI.GREEN}TraoDoiSub (TDS API){UI.RESET}")
        print(f"{UI.YELLOW} Update   : {UI.GREEN}Version 6.8 (Fix Job API){UI.RESET}")
        print(f"{UI.BOLD}{UI.WHITE}──────────────────────────────────────────────────────────{UI.RESET}\n")

    @staticmethod
    def log(name, action, message, status="INFO"):
        now = datetime.now().strftime('%H:%M:%S')
        col_time = f"{UI.GREY}[{now}]{UI.RESET}"

        clean_name = name.strip()[:10]
        col_name = f"{UI.CYAN}{clean_name}{UI.RESET}" 
        col_action = f"{UI.YELLOW}{action}{UI.RESET}"

        if status == "SUCCESS":
            print(f"{col_time}|{col_name}|{col_action}|{UI.GREEN}SUCCESS{UI.RESET}| {UI.WHITE}{message}{UI.RESET}")
        elif status == "ERROR":
            print(f"{col_time}|{col_name}|{col_action}|{UI.RED}ERROR{UI.RESET}| {UI.RED}{message}{UI.RESET}")
        elif status == "WARNING":
            print(f"{col_time}|{col_name}|{col_action}|{UI.ORANGE}WARNING{UI.RESET}| {UI.ORANGE}{message}{UI.RESET}")
        elif status == "INFO":
            print(f"{col_time} {UI.BLUE}➤{UI.RESET} {message}")

    @staticmethod
    def searching_led(job_name):
        text = f"Đang tìm nhiệm vụ {job_name} ......"
        seconds = 1.0 
        fps = 10
        total_frames = int(seconds * fps)

        for frame in range(total_frames):
            led_text = ""
            offset = frame 
            for i, char in enumerate(text):
                color_idx = (i + offset) % len(UI.RAINBOW_COLORS)
                color = UI.RAINBOW_COLORS[color_idx]
                led_text += f"\033[38;5;{color}m{char}"

            sys.stdout.write(f"\r  {UI.BLUE}➤{UI.RESET} {led_text}{UI.RESET}   ")
            sys.stdout.flush()
            time.sleep(1.0 / fps)

        sys.stdout.write(f"\r  {UI.BLUE}➤{UI.RESET} {led_text}{UI.RESET}   \r") 

    @staticmethod
    def progress_bar(seconds, message="Đợi"):
        fps = 5  
        total_frames = int(seconds * fps)

        for frame in range(total_frames):
            remaining = seconds - (frame // fps)
            display_str = f"{message} {remaining}s"

            led_text = ""
            offset = frame 
            for i, char in enumerate(display_str):
                color_idx = (i + offset) % len(UI.RAINBOW_COLORS)
                color = UI.RAINBOW_COLORS[color_idx]
                led_text += f"\033[38;5;{color}m{char}"

            sys.stdout.write(f"\r  {UI.BLUE}➤{UI.RESET} {led_text}{UI.RESET}   ")
            sys.stdout.flush()
            time.sleep(1.0 / fps)

        sys.stdout.write("\r" + " "*50 + "\r") 

# ==============================================================================
# SECTION: CONFIG
# ==============================================================================

ACCOUNT_FILE = "accounttds.txt" 
COOKIE_FILE = "cookie.txt"

# URL CHUẨN CỦA TRAODOISUB
TDS_BASE_URL = "https://traodoisub.com/api"
TDS_FIELDS_URL = f"{TDS_BASE_URL}/?fields="
TDS_COIN_URL = f"{TDS_BASE_URL}/coin/?type="
TDS_DATNICK_URL = "https://traodoisub.com/scr/datnick.php" 

SUPPORTED_TASK_TYPES = {
    "1": "facebook_reaction",
    "2": "facebook_follow",
    "3": "facebook_share",
    "4": "facebook_page"
}

REACTION_IDS = {
    "LIKE": "1635855486666999", "LOVE": "1678524932434102", "CARE": "613557422527858",
    "HAHA": "115940658764963", "WOW": "478547315650144", "SAD": "908563459236466", 
    "ANGRY": "444813342392137"
}

# ==============================================================================
# SECTION: CORE CLASSES
# ==============================================================================

class FacebookAccount:
    def __init__(self, cookie_str):
        self.cookie = cookie_str
        self.name = "Unknown"
        self.uid = None
        self.fb_dtsg = None
        self.is_valid = self._validate_and_fetch_details()

    def _validate_and_fetch_details(self):
        try:
            uid_match = re.search(r"c_user=(\d+)", self.cookie)
            if uid_match: self.uid = uid_match.group(1)
            else: return False

            headers = {
                'authority': 'www.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'cookie': self.cookie,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }

            homepage_response = requests.get('https://www.facebook.com/', headers=headers, timeout=20)
            homepage_text = homepage_response.text

            if 'login.php' in str(homepage_response.url) or "Đăng nhập Facebook" in homepage_text:
                return False

            fb_dtsg_match = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"', homepage_text) or \
                            re.search(r'name="fb_dtsg" value="(.*?)"', homepage_text) or \
                            re.search(r'"async_get_token":"(.*?)"', homepage_text)

            if fb_dtsg_match: self.fb_dtsg = fb_dtsg_match.group(1)

            name_match = re.search(r'"NAME":"(.*?)"', homepage_text)
            if name_match: 
                self.name = name_match.group(1).encode('latin1').decode('unicode-escape')
            else:
                soup = BeautifulSoup(homepage_text, 'html.parser')
                title_tag = soup.find('title')
                if title_tag: self.name = title_tag.string

            return True
        except: return False

class FacebookInteractor:
    def __init__(self, fb_account: FacebookAccount):
        self.account = fb_account
        self.headers = {
            "accept": "*/*", "content-type": "application/x-www-form-urlencoded",
            "cookie": self.account.cookie, "origin": "https://www.facebook.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-fb-lsd": "SaEkSywP_uH8A3cpczP2RG"
        }

    def _get_post_id(self, task_id):
        if '_' in task_id: return task_id.split('_')[1]
        return task_id

    def _perform_reaction(self, task_id, reaction_name):
        reaction_id = REACTION_IDS.get(reaction_name.upper())
        if not reaction_id: return False

        post_id = self._get_post_id(task_id)
        feedback_id = base64.b64encode(f"feedback:{post_id}".encode()).decode()

        variables = {
            "input": {
                "feedback_id": feedback_id, "feedback_reaction_id": reaction_id, 
                "feedback_source": "NEWS_FEED", "actor_id": self.account.uid, 
                "client_mutation_id": str(uuid.uuid4())
            }
        }
        data = {
            "av": self.account.uid, "__user": self.account.uid, "fb_dtsg": self.account.fb_dtsg,
            "fb_api_req_friendly_name": "CometUFIFeedbackReactMutation", 
            "variables": json.dumps(variables), "doc_id": "9518016021660044"
        }
        try:
            requests.post("https://www.facebook.com/api/graphql/", headers=self.headers, data=data, timeout=10)
            return True
        except: return False

    def follow_user(self, target_id):
        variables = {"input": { "friend_requestee_ids": [target_id], "friending_channel": "PROFILE_BUTTON", "actor_id": self.account.uid }}
        headers = self.headers.copy(); headers.update({'x-fb-friendly-name': 'FriendingCometFriendRequestSendMutation'})
        data = { "av": self.account.uid, "__user": self.account.uid, "fb_dtsg": self.account.fb_dtsg, "doc_id": "9088602351172612", "variables": json.dumps(variables)}
        try:
            requests.post("https://www.facebook.com/api/graphql/", headers=headers, data=data, timeout=10)
            return True
        except: return False

    def like_page(self, page_id):
        variables = {"input": {"page_id": page_id, "actor_id": self.account.uid, "client_mutation_id": str(random.randint(1, 10))}, "scale": 1}
        headers = self.headers.copy(); headers.update({'x-fb-friendly-name': 'CometProfilePlusLikeMutation'})
        data = { "av": self.account.uid, "__user": self.account.uid, "fb_dtsg": self.account.fb_dtsg, "variables": json.dumps(variables), "doc_id": "10062329867123540" }
        try:
            requests.post("https://www.facebook.com/api/graphql/", headers=headers, data=data, timeout=10)
            return True
        except: return False

    def share_post(self, task_id):
        post_id = self._get_post_id(task_id)
        variables = {
            "input": {
                "composer_entry_point": "share_modal", "composer_source_surface": "feed_story", "composer_type": "share",
                "idempotence_token": f"{str(uuid.uuid4())}_FEED", "source": "WWW",
                "attachments": [{"link": {"share_scrape_data": json.dumps({"share_type": 22, "share_params": [post_id]})}}],
                "audience": {"privacy": {"base_state": "EVERYONE"}}, "actor_id": self.account.uid, "client_mutation_id": "2"
            }
        }
        headers = self.headers.copy(); headers.update({'x-fb-friendly-name': 'ComposerStoryCreateMutation'})
        data = { "av": self.account.uid, "__user": self.account.uid, "fb_dtsg": self.account.fb_dtsg, "variables": json.dumps(variables), "doc_id": "9502543119760740" }
        try:
            requests.post("https://www.facebook.com/api/graphql/", headers=headers, data=data, timeout=10)
            return True
        except: return False

class TDSClient:
    def __init__(self, token):
        self.token = token

    def get_job_list(self, task_type):
        url = f"{TDS_FIELDS_URL}{task_type}&access_token={self.token}"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if "data" in data: return data["data"]
            return []
        except: return []

    def claim_reward(self, job_id, task_type):
        url = f"{TDS_COIN_URL}{task_type}&id={job_id}&access_token={self.token}"
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except: return None

    def submit_for_review(self, job_id, task_type):
        review_type = f"{task_type}_cache"
        url = f"{TDS_COIN_URL}{review_type}&id={job_id}&access_token={self.token}"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if "cache" in data:
                return {"status": "CACHE", "count": data["cache"], "msg": f"Cache: {data['cache']}"}
            if "xu" in data:
                 return data 
            return data
        except: return None

# ==============================================================================
# SECTION: MAIN LOGIC (UPDATED DATNICK URL)
# ==============================================================================

def login_tds(username, password):
    url = "https://traodoisub.com/scr/login.php"
    try:
        res = requests.post(url, data={"username": username, "password": password})
        if "success" in res.text:
            cookies = res.cookies
            info = requests.post("https://traodoisub.com/view/setting/load.php", cookies=cookies).json()
            if "tokentds" in info:
                return info['tokentds'], info.get('user', username), info.get('xu', '0'), cookies
    except: pass
    return None, None, None, None

# HÀM SET MAIN ACCOUNT CHUẨN TDS
def set_main_account_tds(tds_cookies, fb_uid):
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    data = {"iddat": fb_uid}
    try:
        res = requests.post(TDS_DATNICK_URL, headers=headers, cookies=tds_cookies, data=data, timeout=10)
        return res.text.strip() == "1"
    except: return False

def process_job(job_type, job, tds_client, interactor):
    job_id = job['id']
    job_code = job.get('code', job_id)
    success = False

    display_type = job_type.replace('facebook_', '').upper()
    if display_type == 'REACTION': display_type = job.get('type', 'LIKE').upper()

    try:
        if job_type == "facebook_reaction":
            rtype = job.get('type', 'LIKE').upper()
            success = interactor._perform_reaction(job_id, rtype)
        elif job_type == "facebook_share":
            success = interactor.share_post(job_id)
        elif job_type == "facebook_follow":
            success = interactor.follow_user(job_id)
        elif job_type == "facebook_page":
            success = interactor.like_page(job_id)

        if not success:
            return 'ACTION_FAILED', 0, "FB Block/Lỗi"

        time.sleep(1) 

        if job_type in ["facebook_follow", "facebook_page"]:
            res = tds_client.submit_for_review(job_code, job_type)
            if res and res.get("status") == "CACHE":
                return 'CACHE', 0, res.get("msg")
            elif res and "xu" in res:
                return 'SUCCESS', int(res['xu']), res.get('msg')
            else:
                 return 'API_ERROR', 0, str(res)

        else:
            if job_type == "facebook_share": time.sleep(2) 
            res = tds_client.claim_reward(job_code, job_type)
            if res and "xu" in res:
                return 'SUCCESS', int(res['xu']), res.get('msg')
            else:
                return 'API_ERROR', 0, str(res)

    except Exception as e:
        return 'ERROR', 0, str(e)

def main():
    UI.banner()

    # 1. LOGIN TDS
    print(f"{UI.BG_GREEN}{UI.WHITE} ĐĂNG NHẬP TRAODOISUB {UI.RESET}")
    tds_data = None

    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE) as f: lines = f.readlines()
        if lines:
            u, p = lines[0].strip().split('|')
            if input(f"{UI.YELLOW}Dùng tài khoản {u}? (y/n): {UI.RESET}").lower() == 'y':
                token, user, xu, ck = login_tds(u, p)
                if token: tds_data = (token, user, xu, ck)

    if not tds_data:
        u = input("Username TDS: "); p = input("Password TDS: ")
        token, user, xu, ck = login_tds(u, p)
        if token:
            with open(ACCOUNT_FILE, 'w') as f: f.write(f"{u}|{p}")
            tds_data = (token, user, xu, ck)
        else:
            print("Đăng nhập thất bại!"); return

    token, user, current_xu, tds_cookies = tds_data
    tds_client = TDSClient(token)
    print(f"{UI.GREEN}Login thành công: {user} | Xu: {current_xu}{UI.RESET}")

    # 2. CONFIG
    global settings
    print(f"\n{UI.BG_GREEN}{UI.WHITE} CẤU HÌNH TOOL {UI.RESET}")
    try:
        delay_min = int(input(f"{UI.YELLOW}Delay Min (giây): {UI.RESET}"))
        delay_max = int(input(f"{UI.YELLOW}Delay Max (giây): {UI.RESET}"))
        jobs_break = int(input(f"{UI.YELLOW}Chạy bao nhiêu job thì nghỉ: {UI.RESET}"))
        time_break = int(input(f"{UI.YELLOW}Thời gian nghỉ (giây): {UI.RESET}"))
        job_switch = int(input(f"{UI.YELLOW}Chạy bao nhiêu job thì đổi acc: {UI.RESET}"))
        max_job = int(input(f"{UI.YELLOW}Chạy bao nhiêu job thì dừng acc (0=full): {UI.RESET}"))

        settings = {
            'DELAY': (delay_min, delay_max), 'BREAK': (jobs_break, time_break),
            'SWITCH': job_switch, 'MAX': max_job
        }
    except:
        print("Nhập sai, dùng mặc định."); settings = {'DELAY': (5,10), 'BREAK': (20,60), 'SWITCH': 100, 'MAX': 0}

    # 3. COOKIES
    print(f"\n{UI.BG_GREEN}{UI.WHITE} NHẬP COOKIE FACEBOOK {UI.RESET}")
    raw_cookies = []
    if input("1: Dán | 2: File cookie.txt : ") == '2':
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE) as f: raw_cookies = [l.strip() for l in f if l.strip()]
    else:
        print("Dán cookie (Enter dòng trống để chạy):")
        while True:
            c = input(); 
            if not c: break
            raw_cookies.append(c.strip())

    # 4. CHECK LIVE
    valid_accs = []
    print(f"\n{UI.BOLD}Đang kiểm tra cookie...{UI.RESET}")
    for i, c in enumerate(raw_cookies):
        acc = FacebookAccount(c)
        if acc.is_valid:
            valid_accs.append(acc)
            print(f"[{i+1}] {UI.GREEN}LIVE{UI.RESET} | {acc.name} | {acc.uid}")
        else:
            print(f"[{i+1}] {UI.RED}DIE {UI.RESET}")
    if not valid_accs: return

    # 5. SELECT JOBS
    print(f"\n{UI.BG_GREEN}{UI.WHITE} CHỌN JOB {UI.RESET}")
    print("1. Reaction  2. Follow  3. Share  4. Page")
    c = input("Chọn (vd 1+2): ")
    selected_types = []
    for x in c.split('+'):
        if x in SUPPORTED_TASK_TYPES: selected_types.append(SUPPORTED_TASK_TYPES[x])
    if not selected_types: selected_types = list(SUPPORTED_TASK_TYPES.values())

    # 6. RUN
    UI.banner()
    print(f" {UI.BG_GREEN}{UI.WHITE} Chạy {len(valid_accs)} acc Facebook với TDS: {user} {UI.RESET}\n")
    print(f"{UI.YELLOW}Số dư ban đầu: {UI.GREEN}{current_xu} xu{UI.RESET}\n")

    acc_job_counters = {acc.uid: 0 for acc in valid_accs} 
    session_job_counter = 0
    acc_idx = 0
    blocked_jobs = {acc.uid: set() for acc in valid_accs}
    total_balance = int(current_xu)

    while True:
        try:
            curr_acc = valid_accs[acc_idx % len(valid_accs)]
            if not curr_acc.is_valid:
                valid_accs.remove(curr_acc)
                if not valid_accs: print("Hết acc."); break
                continue

            # QUAN TRỌNG: Cấu hình nick cho TDS
            set_main_account_tds(tds_cookies, curr_acc.uid)

            interactor = FacebookInteractor(curr_acc)
            jtype = random.choice(selected_types)
            jtype_display = jtype.replace('facebook_', '').upper()

            try:
                UI.searching_led(jtype_display)
                jobs = tds_client.get_job_list(jtype)

                sys.stdout.write("\r" + " "*80 + "\r")
                sys.stdout.flush()

                if jobs:
                    print(f"  {UI.GREEN}➤ Tìm thấy {len(jobs)} nhiệm vụ. Đang cày...{UI.RESET}")

                    for job in jobs:
                        if settings['MAX'] > 0 and acc_job_counters[curr_acc.uid] >= settings['MAX']:
                            UI.log(curr_acc.name, "STOP", f"Đã xong {settings['MAX']} jobs.", "WARNING")
                            valid_accs.remove(curr_acc)
                            break 

                        if acc_job_counters[curr_acc.uid] > 0 and acc_job_counters[curr_acc.uid] % settings['SWITCH'] == 0:
                            UI.log(curr_acc.name, "SWITCH", f"Đổi acc...", "INFO")
                            acc_idx += 1
                            break 

                        if session_job_counter > 0 and session_job_counter % settings['BREAK'][0] == 0:
                            print(f"\n{UI.YELLOW}Đã làm {settings['BREAK'][0]} jobs. Nghỉ ngơi...{UI.RESET}")
                            UI.progress_bar(settings['BREAK'][1], "Nghỉ")
                            session_job_counter = 0 

                        status, earned, msg = process_job(jtype, job, tds_client, interactor)

                        display_name = jtype.replace('facebook_', '').upper()
                        if jtype == 'facebook_reaction': display_name = job.get('type', 'LIKE').upper()

                        if status == 'SUCCESS': 
                            total_balance += earned
                            acc_job_counters[curr_acc.uid] += 1
                            session_job_counter += 1
                            UI.log(curr_acc.name, display_name, f"+{earned} xu | {UI.YELLOW}{total_balance} xu{UI.RESET}", "SUCCESS")

                            delay = random.randint(settings['DELAY'][0], settings['DELAY'][1])
                            UI.progress_bar(delay, "Chờ")

                        elif status == 'CACHE':
                            UI.log(curr_acc.name, display_name, f"{msg}", "WARNING")
                            time.sleep(1)

                        elif status == 'API_ERROR': pass
                        else: pass

                    if not valid_accs: print("Done."); break
                else:
                    time.sleep(2)

            except Exception as e:
                pass

        except KeyboardInterrupt: break
        except Exception: pass

if __name__ == "__main__":
    main()
