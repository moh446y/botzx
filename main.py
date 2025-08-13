import sys
import time
import requests
import threading
import telebot
from telebot import types
import json

# Bot Token - ضع توكن البوت هنا
BOT_TOKEN = "6927966683:AAHGSfdNmM9aVB_F7qUnQv0KCuq_eGqaklY"
bot = telebot.TeleBot(BOT_TOKEN)

# متغير لحفظ بيانات المستخدمين
user_data = {}

sys.excepthook = lambda *args: None

def countdown_message(chat_id, message_id, seconds, loop=""):
    """عد تنازلي مع تحديث الرسالة"""
    for remaining in range(seconds, 0, -1):
        try:
            countdown_text = f"⏳ {loop} انتظار: {remaining} ثانية"
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=countdown_text
            )
            time.sleep(1)
        except:
            pass
    
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="✅ انتهى الانتظار"
        )
    except:
        pass

def login(number, password):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'silentLogin': 'false',
        'x-dynatrace': 'MT_3_17_3569497752_11-0_a556db1b-4506-43f3-854a-1d2527767923_0_25993_455',
        'x-agent-operatingsystem': '13',
        'clientId': 'AnaVodafoneAndroid',
        'Accept-Language': 'ar',
        'x-agent-device': 'Xiaomi M2101K9AG',
        'x-agent-version': '2025.7.3',
        'x-agent-build': '1068',
        'User-Agent': 'okhttp/4.11.0',
        'Host': 'mobile.vodafone.com.eg',
        'Accept-Encoding': 'gzip',
    }

    data = {
        "username": number,
        "password": password,
        "grant_type": "password",
        "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
        "client_id": "my-vodafone-app"
    }

    try:
        res = requests.post(
            "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token",
            headers=headers,
            data=data
        )
        
        if res.status_code == 200:
            access_token = res.json().get("access_token")
            return access_token
        else:
            return None
            
    except Exception as e:
        return None

def QuotaRedistribution(access_token, owner, member, quota):
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "Host": "mobile.vodafone.com.eg",
        "User-Agent": "okhttp/4.11.0",
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer "+access_token,
        "api-version": "v2",
        "x-agent-operatingsystem": "15",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "HONOR ELI-NX9",
        "x-agent-version": "2024.12.1",
        "x-agent-build": "946",
        "msisdn": owner,
        "Accept-Language": "ar"
    }
    data = {
          "category": [
            {
              "listHierarchyId": "TemplateID",
              "value": "47"
            }
          ],
          "createdBy": {
            "value": "MobileApp"
          },
          "parts": {
            "characteristicsValue": {
              "characteristicsValue": [
                {
                  "characteristicName": "quotaDist1",
                  "type": "percentage",
                  "value": quota
                }
              ]
            },
            "member": [
              {
                "id": [
                  {
                    "schemeName": "MSISDN",
                    "value": owner
                  }
                ],
                "type": "Owner"
              },
              {
                "id": [
                  {
                    "schemeName": "MSISDN",
                    "value": member
                  }
                ],
                "type": "Member"
              }
            ]
          },
          "type": "QuotaRedistribution"
    }
    response = requests.patch(url, headers=headers, json=data).text
    return f'[+]quota [{member}]| {quota} => {response}'

def SendInvitation(access_token, owner, member, quota):
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "Host": "web.vodafone.com.eg",
        "User-Agent": "Mozilla/5.0 (iPhone 15; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/605.1.15",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept": "application/json",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "sec-ch-ua-platform": "Android",
        "Authorization": "Bearer "+access_token,
        "Accept-Language": "AR",
        "msisdn": owner,
        "clientId": "WebsiteConsumer",
        "Origin": "https://web.vodafone.com.eg",
        "X-Requested-With": "mark.via.gp"
    }
    data = {
          "name": "FlexFamily",
          "type": "SendInvitation",
          "category": [
            {
              "value": 523,
              "listHierarchyId": "PackageID"
            },
            {
              "value": "47",
              "listHierarchyId": "TemplateID"
            },
            {
              "value": 523,
              "listHierarchyId": "TierID"
            }
          ],
          "parts": {
            "member": [
              {
                "id": [
                  {
                    "value": owner,
                    "schemeName": "MSISDN"
                  }
                ],
                "type": "Owner"
              },
              {
                "id": [
                  {
                    "value": member,
                    "schemeName": "MSISDN"
                  }
                ],
                "type": "Member"
              }
            ],
            "characteristicsValue": {
              "characteristicsValue": [
                {
                  "characteristicName": "quotaDist1",
                  "value": quota,
                  "type": "percentage"
                }
              ]
            }
          }
    }
    response = requests.post(url, headers=headers, json=data).text
    return f"[+]send [{member}] {quota} | {response}"

def AcceptInvitation(access_token, owner, member):
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "Host": "mobile.vodafone.com.eg",
        "User-Agent": "Mozilla/5.0 (iPhone 14; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/605.1.15",
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer "+access_token,
        "api-version": "v2",
        "x-agent-operatingsystem": "15",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "HONOR ELI-NX9",
        "x-agent-version": "2024.12.1",
        "x-agent-build": "946",
        "msisdn": member,
        "Accept-Language": "ar"
    }
    payload = {
        "name": "FlexFamily",
        "type": "AcceptInvitation",
        "category": [
            {"value": "47", "listHierarchyId": "TemplateID"}
        ],
        "parts": {
            "member": [
                {
                    "id": [{"value": owner, "schemeName": "MSISDN"}],
                    "type": "Owner"
                },
                {
                    "id": [{"value": member, "schemeName": "MSISDN"}],
                    "type": "Member"
                }
            ]
        }
    }
    response = requests.patch(url, headers=headers, json=payload).text
    return f"[+]Accept [{member}] | {response}"

def CancelInvitation(access_token, owner, member):
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "Host": "web.vodafone.com.eg",
        "User-Agent": "Mozilla/5.0 (iPhone 12; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/604.1 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer "+access_token,
        "api-version": "v2",
        "x-agent-operatingsystem": "15",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "iPhone 14 Pro Max",
        "x-agent-version": "2024.11.2",
        "x-agent-build": "944",
        "msisdn": owner,
        "Accept-Language": "ar"
    }
    payload = {
    "category": [
        {"listHierarchyId": "PackageID", "value": 523},
        {"listHierarchyId": "TemplateID", "value": "47"},
        {"listHierarchyId": "TierID", "value": 523}
    ],
    "parts": {
        "characteristicsValue": {
            "characteristicsValue": [
                {"characteristicName": "quotaDist1", "type": "percentage", "value": "40"}
            ]
        },
        "member": [
            {
                "id": [{"schemeName": "MSISDN", "value": owner}],
                "type": "Owner"
            },
            {
                "id": [{"schemeName": "MSISDN", "value": member}],
                "type": "Member"
            }
        ]
    },
    "type": "CancelInvitation"
}

    response = requests.post(url, headers=headers, json=payload).text
    return f"[+]Remove [{member}] | {response}"

def total_felix(access_token, owner):
    url = f"https://web.vodafone.com.eg/services/dxl/usage/usageConsumptionReport?bucket.product.publicIdentifier={owner}&@type=aggregated"
    headers = {
        "User-Agent": "okhttp/4.11.0",
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Connection": "Keep-Alive",
        "channel": "MOBILE",
        "useCase": "Promo",
        "Authorization": "Bearer "+access_token,
        "api-version": "v2",
        "x-agent-operatingsystem": "11",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "OPPO CPH2059",
        "x-agent-version": "2024.3.3",
        "x-agent-build": "593",
        "msisdn": owner,
        "Content-Type": "application/json",
        "Accept-Language": "ar",
        "Host": "web.vodafone.com.eg"
    }
    response = requests.get(url, headers=headers).json()
    value = None
    for item in response:
           if item.get("@type") == "OTHERS":
               for bucket in item.get("bucket", []):
                   if bucket.get("usageType") == "limit":
                       value = bucket["bucketBalance"][0]["remainingValue"]["amount"]
                       break
    return f"Flexat => {value}"

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 بدء تشغيل السكريبت")
    btn2 = types.KeyboardButton("⚙️ إعداد البيانات")
    btn3 = types.KeyboardButton("ℹ️ مساعدة")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id,
        "مرحباً بك في بوت Vodafone FlexFamily! 🎉\n\n"
        "يمكنك استخدام هذا البوت لتشغيل سكريبت توزيع الفليكسات تلقائياً.\n\n"
        "اختر من الأزرار أدناه:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "⚙️ إعداد البيانات")
def setup_data(message):
    user_id = message.from_user.id
    user_data[user_id] = {'step': 'owner_number'}
    
    bot.send_message(
        message.chat.id,
        "📱 أدخل رقم المالك (Owner):\nمثال: 01094899196"
    )

@bot.message_handler(func=lambda message: message.text == "ℹ️ مساعدة")
def help_message(message):
    help_text = """
📋 **دليل الاستخدام:**

1️⃣ **إعداد البيانات**: قم بإدخال جميع البيانات المطلوبة
2️⃣ **بدء التشغيل**: شغل السكريبت بعد إعداد البيانات

📝 **البيانات المطلوبة:**
• رقم المالك + كلمة المرور
• رقم العضو الأول
• رقم العضو الثاني + كلمة المرور
• عدد الحلقات المطلوبة

⚠️ **تنبيه:** تأكد من صحة البيانات قبل البدء
    """
    
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "🚀 بدء تشغيل السكريبت")
def start_script(message):
    user_id = message.from_user.id
    
    if user_id not in user_data or 'owner' not in user_data[user_id]:
        bot.send_message(
            message.chat.id,
            "❌ يجب إعداد البيانات أولاً!\nاضغط على 'إعداد البيانات' لبدء الإعداد."
        )
        return
    
    data = user_data[user_id]
    
    # عرض البيانات للتأكيد
    confirm_text = f"""
📋 **تأكيد البيانات:**

👤 **المالك:** {data['owner']}
👥 **العضو الأول:** {data['member1']}
👥 **العضو الثاني:** {data['member2']}
🔄 **عدد الحلقات:** {data['count_loop']}

هل تريد بدء التشغيل؟
    """
    
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("✅ تأكيد", callback_data="confirm_start")
    btn_no = types.InlineKeyboardButton("❌ إلغاء", callback_data="cancel_start")
    markup.add(btn_yes, btn_no)
    
    bot.send_message(message.chat.id, confirm_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "confirm_start")
def confirm_start_script(call):
    user_id = call.from_user.id
    data = user_data[user_id]
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🚀 بدء تشغيل السكريبت...\nجاري تسجيل الدخول..."
    )
    
    # تشغيل السكريبت في thread منفصل
    script_thread = threading.Thread(
        target=run_script,
        args=(call.message.chat.id, data)
    )
    script_thread.start()

@bot.callback_query_handler(func=lambda call: call.data == "cancel_start")
def cancel_start_script(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="❌ تم إلغاء التشغيل"
    )

def run_script(chat_id, data):
    try:
        owner = data['owner']
        password_owner = data['password_owner']
        member1 = data['member1']
        member2 = data['member2']
        password_member2 = data['password_member2']
        count_loop = data['count_loop']
        
        # تسجيل الدخول
        bot.send_message(chat_id, "🔐 جاري تسجيل دخول المالك...")
        access_owner = login(owner, password_owner)
        
        if not access_owner:
            bot.send_message(chat_id, "❌ فشل في تسجيل دخول المالك")
            return
            
        bot.send_message(chat_id, "✅ تم تسجيل دخول المالك بنجاح")
        
        bot.send_message(chat_id, "🔐 جاري تسجيل دخول العضو الثاني...")
        access_member = login(member2, password_member2)
        
        if not access_member:
            bot.send_message(chat_id, "❌ فشل في تسجيل دخول العضو الثاني")
            return
            
        bot.send_message(chat_id, "✅ تم تسجيل دخول العضو الثاني بنجاح")
        
        # بدء الحلقة الرئيسية
        for x in range(count_loop):
            loop_msg = bot.send_message(chat_id, f"🔄 بدء الحلقة {x+1} من {count_loop}")
            
            # إعادة تسجيل الدخول كل حلقتين
            if x % 2 == 0 and x != 0:
                bot.send_message(chat_id, "🔄 إعادة تسجيل الدخول...")
                access_owner = login(owner, password_owner)
                access_member = login(member2, password_member2)
                bot.send_message(chat_id, "✅ تم تجديد تسجيل الدخول")

            # توزيع الكوتا الأولى
            result = QuotaRedistribution(access_owner, owner, member1, '10')
            bot.send_message(chat_id, result)
            
            # انتظار 5 دقائق
            countdown_msg = bot.send_message(chat_id, "⏳ انتظار 5 دقائق...")
            countdown_message(chat_id, countdown_msg.message_id, 5*60)
            
            # إرسال الدعوة
            result = SendInvitation(access_owner, owner, member2, '40')
            bot.send_message(chat_id, result)
            
            time.sleep(15)
            
            # تشغيل العمليات المتوازية
            barrier = threading.Barrier(2)

            def fun1():
                barrier.wait()
                result = AcceptInvitation(access_member, owner, member2)
                bot.send_message(chat_id, result)

            def fun2():
                barrier.wait()
                result = QuotaRedistribution(access_owner, owner, member1, '40')
                bot.send_message(chat_id, result)

            t1 = threading.Thread(target=fun1)
            t2 = threading.Thread(target=fun2)

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            time.sleep(15)
            
            # إلغاء الدعوة
            result = CancelInvitation(access_owner, owner, member2)
            bot.send_message(chat_id, result)
            
            # عرض إجمالي الفليكسات
            result = total_felix(access_owner, owner)
            bot.send_message(chat_id, result)
            
            # انتظار 5 دقائق بين الحلقات
            if x < count_loop - 1:  # لا تنتظر بعد آخر حلقة
                countdown_msg = bot.send_message(chat_id, f"⏳ انتظار بين الحلقات...")
                countdown_message(chat_id, countdown_msg.message_id, 5*60, f'loop {x + 1} from {count_loop}')
        
        bot.send_message(chat_id, f"🎉 تم الانتهاء من جميع الحلقات ({count_loop})!")
        
    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ: {str(e)}")

@bot.message_handler(content_types=['text'])
def handle_setup_steps(message):
    user_id = message.from_user.id
    
    if user_id not in user_data:
        return
    
    step = user_data[user_id].get('step')
    
    if step == 'owner_number':
        user_data[user_id]['owner'] = message.text
        user_data[user_id]['step'] = 'owner_password'
        bot.send_message(message.chat.id, "🔒 أدخل كلمة مرور المالك:")
        
    elif step == 'owner_password':
        user_data[user_id]['password_owner'] = message.text
        user_data[user_id]['step'] = 'member1_number'
        bot.send_message(message.chat.id, "📱 أدخل رقم العضو الأول:")
        
    elif step == 'member1_number':
        user_data[user_id]['member1'] = message.text
        user_data[user_id]['step'] = 'member2_number'
        bot.send_message(message.chat.id, "📱 أدخل رقم العضو الثاني:")
        
    elif step == 'member2_number':
        user_data[user_id]['member2'] = message.text
        user_data[user_id]['step'] = 'member2_password'
        bot.send_message(message.chat.id, "🔒 أدخل كلمة مرور العضو الثاني:")
        
    elif step == 'member2_password':
        user_data[user_id]['password_member2'] = message.text
        user_data[user_id]['step'] = 'count_loop'
        bot.send_message(message.chat.id, "🔢 أدخل عدد الحلقات المطلوبة:")
        
    elif step == 'count_loop':
        try:
            count_loop = int(message.text)
            user_data[user_id]['count_loop'] = count_loop
            del user_data[user_id]['step']
            
            bot.send_message(
                message.chat.id,
                "✅ تم حفظ جميع البيانات بنجاح!\nيمكنك الآن الضغط على 'بدء تشغيل السكريبت'"
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ يجب إدخال رقم صحيح لعدد الحلقات")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(none_stop=True)
