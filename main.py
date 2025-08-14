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

# قائمة الأدمن (ضع الـ user_id الخاص بك هنا)
ADMIN_IDS = [5611407285]  # غير هذا الرقم بـ user_id الخاص بك

# قائمة المستخدمين المسموح لهم (يديرها الأدمن)
ALLOWED_USERS = set(ADMIN_IDS)  # الأدمن مسموح بشكل افتراضي

# متغير لحفظ بيانات المستخدمين
user_data = {}

sys.excepthook = lambda *args: None

def is_admin(user_id):
    """التحقق من كون المستخدم أدمن"""
    return user_id in ADMIN_IDS

def is_allowed(user_id):
    """التحقق من كون المستخدم مسموح له باستخدام البوت"""
    return user_id in ALLOWED_USERS

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
    user_id = message.from_user.id
    
    # التحقق من الصلاحيات
    if not is_allowed(user_id):
        bot.send_message(
            message.chat.id,
            "❌ عذراً، ليس لديك صلاحية لاستخدام هذا البوت.\n"
            "تواصل مع المطور للحصول على الصلاحية."
        )
        return
    
    # إنشاء الأزرار حسب نوع المستخدم
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 بدء تشغيل السكريبت")
    btn2 = types.KeyboardButton("⚙️ إعداد البيانات")
    btn3 = types.KeyboardButton("ℹ️ مساعدة")
    
    if is_admin(user_id):
        btn_admin = types.KeyboardButton("👑 لوحة الأدمن")
        markup.add(btn1, btn2)
        markup.add(btn3, btn_admin)
    else:
        markup.add(btn1, btn2, btn3)
    
    welcome_msg = "مرحباً بك في بوت Vodafone FlexFamily! 🎉\n\n"
    welcome_msg += "يمكنك استخدام هذا البوت لتشغيل سكريبت توزيع الفليكسات تلقائياً.\n\n"
    
    if is_admin(user_id):
        welcome_msg += "🔥 مرحباً أدمن! لديك صلاحيات إضافية.\n\n"
    
    welcome_msg += "اختر من الأزرار أدناه:"
    
    bot.send_message(
        message.chat.id,
        welcome_msg,
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "👑 لوحة الأدمن")
def admin_panel(message):
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ ليس لديك صلاحية أدمن!")
        return
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("➕ إضافة مستخدم", callback_data="admin_add_user")
    btn2 = types.InlineKeyboardButton("➖ حذف مستخدم", callback_data="admin_remove_user")
    btn3 = types.InlineKeyboardButton("📋 عرض المستخدمين", callback_data="admin_list_users")
    btn4 = types.InlineKeyboardButton("📊 إحصائيات", callback_data="admin_stats")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    
    admin_text = f"""
👑 **لوحة تحكم الأدمن**

📈 **إحصائيات سريعة:**
• المستخدمين المسموحين: {len(ALLOWED_USERS)}
• الأدمن: {len(ADMIN_IDS)}

⚙️ **الإعدادات المتاحة:**
    """
    
    bot.send_message(message.chat.id, admin_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_user")
def admin_add_user(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_data[user_id] = {'step': 'admin_add_user_id'}
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👤 أرسل User ID المراد إضافته:\n\n"
             "💡 يمكن الحصول على User ID عن طريق @userinfobot"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_remove_user")
def admin_remove_user(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_data[user_id] = {'step': 'admin_remove_user_id'}
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👤 أرسل User ID المراد حذفه:"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_list_users")
def admin_list_users(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    users_list = "📋 **قائمة المستخدمين المسموحين:**\n\n"
    
    for i, user_id_allowed in enumerate(ALLOWED_USERS, 1):
        status = "👑 (أدمن)" if user_id_allowed in ADMIN_IDS else "👤"
        users_list += f"{i}. {user_id_allowed} {status}\n"
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=users_list,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    stats_text = f"""
📊 **إحصائيات مفصلة:**

👥 **المستخدمين:**
• إجمالي المستخدمين المسموحين: {len(ALLOWED_USERS)}
• عدد الأدمن: {len(ADMIN_IDS)}
• المستخدمين العاديين: {len(ALLOWED_USERS) - len(ADMIN_IDS)}

🤖 **البوت:**
• حالة البوت: 🟢 يعمل
• البيانات المحفوظة: {len(user_data)} مستخدم
    """
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=stats_text,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == "⚙️ إعداد البيانات")
def setup_data(message):
    user_id = message.from_user.id
    
    if not is_allowed(user_id):
        bot.send_message(message.chat.id, "❌ ليس لديك صلاحية لاستخدام هذا البوت!")
        return
    
    user_data[user_id] = {'step': 'owner_number'}
    
    bot.send_message(
        message.chat.id,
        "📱 أدخل رقم المالك (Owner):\nمثال: 01094899196"
    )

@bot.message_handler(func=lambda message: message.text == "ℹ️ مساعدة")
def help_message(message):
    user_id = message.from_user.id
    
    if not is_allowed(user_id):
        bot.send_message(message.chat.id, "❌ ليس لديك صلاحية لاستخدام هذا البوت!")
        return
    
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

⏰ **ملاحظة:** السكريبت سينتظر 5 دقائق بين كل خطوة تلقائياً
    """
    
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "🚀 بدء تشغيل السكريبت")
def start_script(message):
    user_id = message.from_user.id
    
    if not is_allowed(user_id):
        bot.send_message(message.chat.id, "❌ ليس لديك صلاحية لاستخدام هذا البوت!")
        return
    
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

⏰ **ملاحظة:** سيتم الانتظار 5 دقائق تلقائياً بين كل خطوة

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
    status_message = None
    try:
        owner = data['owner']
        password_owner = data['password_owner']
        member1 = data['member1']
        member2 = data['member2']
        password_member2 = data['password_member2']
        count_loop = data['count_loop']
        
        # إنشاء رسالة الحالة الأولية
        initial_status = f"""
🤖 **حالة تشغيل السكريبت**

📊 **معلومات العملية:**
👤 المالك: {owner}
👥 العضو الأول: {member1}  
👥 العضو الثاني: {member2}
🔄 إجمالي الحلقات: {count_loop}

⏳ **الحالة الحالية:** جاري تسجيل الدخول...
        """
        status_message = bot.send_message(chat_id, initial_status, parse_mode='Markdown')
        
        # تسجيل الدخول
        access_owner = login(owner, password_owner)
        
        if not access_owner:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=initial_status.replace("جاري تسجيل الدخول...", "❌ فشل في تسجيل دخول المالك"),
                parse_mode='Markdown'
            )
            return
            
        access_member = login(member2, password_member2)
        
        if not access_member:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=initial_status.replace("جاري تسجيل الدخول...", "❌ فشل في تسجيل دخول العضو الثاني"),
                parse_mode='Markdown'
            )
            return
        
        # بدء الحلقة الرئيسية
        for x in range(count_loop):
            current_loop = x + 1
            
            # تحديث حالة الحلقة
            loop_status = f"""
🤖 **حالة تشغيل السكريبت**

📊 **معلومات العملية:**
👤 المالك: {owner}
👥 العضو الأول: {member1}  
👥 العضو الثاني: {member2}
🔄 الحلقة الحالية: {current_loop} من {count_loop}

⚡ **تقدم الحلقة الحالية:**
"""
            
            # إعادة تسجيل الدخول كل حلقتين
            if x % 2 == 0 and x != 0:
                current_status = loop_status + "🔄 إعادة تسجيل الدخول..."
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=status_message.message_id,
                    text=current_status,
                    parse_mode='Markdown'
                )
                access_owner = login(owner, password_owner)
                access_member = login(member2, password_member2)

            # الخطوة 1: توزيع الكوتا الأولى
            current_status = loop_status + "1️⃣ توزيع الكوتا الأولى..."
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=current_status,
                parse_mode='Markdown'
            )
            
            result1 = QuotaRedistribution(access_owner, owner, member1, '10')
            
            # الخطوة 2: انتظار 5 دقائق
            current_status = loop_status + f"1️⃣ توزيع الكوتا الأولى ✅\n2️⃣ انتظار 5 دقائق... ⏳"
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=current_status,
                parse_mode='Markdown'
            )
            
            time.sleep(5*60)  # انتظار 5 دقائق
            
            # الخطوة 3: إرسال الدعوة
            current_status = loop_status + f"1️⃣ توزيع الكوتا الأولى ✅\n2️⃣ انتظار 5 دقائق ✅\n3️⃣ إرسال الدعوة..."
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=current_status,
                parse_mode='Markdown'
            )
            
            result2 = SendInvitation(access_owner, owner, member2, '40')
            
            time.sleep(15)
            
            # الخطوة 4: العمليات المتوازية
            current_status = loop_status + f"1️⃣ توزيع الكوتا الأولى ✅\n2️⃣ انتظار 5 دقائق ✅\n3️⃣ إرسال الدعوة ✅\n4️⃣ تنفيذ العمليات المتوازية..."
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=current_status,
                parse_mode='Markdown'
            )
            
            # تشغيل العمليات المتوازية
            barrier = threading.Barrier(2)
            results = {}

            def fun1():
                barrier.wait()
                results['accept'] = AcceptInvitation(access_member, owner, member2)

            def fun2():
                barrier.wait()
                results['quota'] = QuotaRedistribution(access_owner, owner, member1, '40')

            t1 = threading.Thread(target=fun1)
            t2 = threading.Thread(target=fun2)

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            time.sleep(15)
            
            # الخطوة 5: إلغاء الدعوة
            current_status = loop_status + f"1️⃣ توزيع الكوتا الأولى ✅\n2️⃣ انتظار 5 دقائق ✅\n3️⃣ إرسال الدعوة ✅\n4️⃣ العمليات المتوازية ✅\n5️⃣ إلغاء الدعوة..."
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=current_status,
                parse_mode='Markdown'
            )
            
            result3 = CancelInvitation(access_owner, owner, member2)
            
            # الخطوة 6: عرض الفليكسات
            current_status = loop_status + f"1️⃣ توزيع الكوتا الأولى ✅\n2️⃣ انتظار 5 دقائق ✅\n3️⃣ إرسال الدعوة ✅\n4️⃣ العمليات المتوازية ✅\n5️⃣ إلغاء الدعوة ✅\n6️⃣ جاري حساب الفليكسات..."
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=current_status,
                parse_mode='Markdown'
            )
            
            flex_result = total_felix(access_owner, owner)
            
            # عرض نتيجة الحلقة المكتملة
            completed_status = f"""
🤖 **حالة تشغيل السكريبت**

📊 **معلومات العملية:**
👤 المالك: {owner}
👥 العضو الأول: {member1}  
👥 العضو الثاني: {member2}
🔄 الحلقة المكتملة: {current_loop} من {count_loop}

✅ **نتيجة الحلقة {current_loop}:**
• {flex_result}

⚡ **حالة جميع الخطوات:**
1️⃣ توزيع الكوتا الأولى ✅
2️⃣ انتظار 5 دقائق ✅  
3️⃣ إرسال الدعوة ✅
4️⃣ العمليات المتوازية ✅
5️⃣ إلغاء الدعوة ✅
6️⃣ حساب الفليكسات ✅
"""
            
            # إضافة حالة الانتظار إذا لم تكن آخر حلقة
            if x < count_loop - 1:
                completed_status += f"\n⏳ انتظار 5 دقائق قبل الحلقة {current_loop + 1}..."
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=status_message.message_id,
                    text=completed_status,
                    parse_mode='Markdown'
                )
                time.sleep(5*60)  # انتظار بين الحلقات
            else:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=status_message.message_id,
                    text=completed_status,
                    parse_mode='Markdown'
                )
        
        # رسالة الإتمام النهائية
        final_status = f"""
🎉 **تم الانتهاء من جميع الحلقات!**

📊 **ملخص العملية:**
👤 المالك: {owner}
👥 العضو الأول: {member1}  
👥 العضو الثاني: {member2}
✅ الحلقات المكتملة: {count_loop} حلقة

🏆 **النتيجة النهائية:**
• {total_felix(access_owner, owner)}

⏰ **وقت الإتمام:** {time.strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_message.message_id,
            text=final_status,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        error_status = f"""
❌ **حدث خطأ في السكريپت!**

🔍 **تفاصيل الخطأ:**
{str(e)}

📞 **تواصل مع المطور للمساعدة**
        """
        
        if status_message:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_message.message_id,
                text=error_status,
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, error_status, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_setup_steps(message):
    user_id = message.from_user.id
    
    if not is_allowed(user_id):
        bot.send_message(message.chat.id, "❌ ليس لديك صلاحية لاستخدام هذا البوت!")
        return
    
    if user_id not in user_data:
        return
    
    step = user_data[user_id].get('step')
    
    # خطوات الأدمن
    if step == 'admin_add_user_id':
        try:
            new_user_id = int(message.text)
            ALLOWED_USERS.add(new_user_id)
            del user_data[user_id]['step']
            bot.send_message(
                message.chat.id,
                f"✅ تم إضافة المستخدم {new_user_id} بنجاح!"
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ يجب إدخال رقم صحيح للـ User ID")
            
    elif step == 'admin_remove_user_id':
        try:
            remove_user_id = int(message.text)
            if remove_user_id in ADMIN_IDS:
                bot.send_message(message.chat.id, "❌ لا يمكن حذف الأدمن!")
            elif remove_user_id in ALLOWED_USERS:
                ALLOWED_USERS.remove(remove_user_id)
                bot.send_message(
                    message.chat.id,
                    f"✅ تم حذف المستخدم {remove_user_id} بنجاح!"
                )
            else:
                bot.send_message(message.chat.id, "❌ هذا المستخدم غير موجود في القائمة!")
            del user_data[user_id]['step']
        except ValueError:
            bot.send_message(message.chat.id, "❌ يجب إدخال رقم صحيح للـ User ID")
    
    # خطوات إعداد البيانات العادية
    elif step == 'owner_number':
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
                "✅ تم حفظ جميع البيانات بنجاح!\nيمكنك الآن الضغط على 'بدء تشغيل السكريپت'"
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ يجب إدخال رقم صحيح لعدد الحلقات")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    print(f"👑 Admin IDs: {ADMIN_IDS}")
    print("⚠️  تأكد من تغيير ADMIN_IDS في الكود!")
    bot.polling(none_stop=True)
