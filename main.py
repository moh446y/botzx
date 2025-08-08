import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import script  # هذا الملف اللي فيه السكريبت الاصلي

API_TOKEN = "6927966683:AAHGSfdNmM9aVB_F7qUnQv0KCuq_eGqaklY"
bot = telebot.TeleBot(API_TOKEN)

# متغير للتحكم بإيقاف البوت أثناء تنفيذ العملية الطويلة
stop_flag = False
worker_thread = None

# بيانات المستخدم اللي راح يدخلها (تحديث مستمر)
user_data = {
    'owner': None,
    'owner_password': None,
    'member1': script.member1,  # ممكن تخليها ثابتة أو تخلي المستخدم يدخلها
    'member2': script.member2,
    'password_member2': script.password_member2
}

def reset_stop_flag():
    global stop_flag
    stop_flag = False

def run_script_async():
    global stop_flag
    owner = user_data['owner']
    owner_password = user_data['owner_password']
    member1 = user_data['member1']
    member2 = user_data['member2']
    password_member2 = user_data['password_member2']
    if not owner or not owner_password:
        return "لم يتم إدخال بيانات المالك."
    
    # العملية مع توقف متحكم فيه
    for i in range(40):
        if stop_flag:
            return "تم إيقاف العملية."
        result = script.run_full_cycle(owner, owner_password, member1, member2, password_member2)
        # بإمكانك ترسل رسالة هنا لو تحب، لكن ممكن تثقل البوت
    return "انتهى التشغيل بنجاح."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    reset_stop_flag()
    bot.send_message(message.chat.id, "مرحبا! من فضلك أدخل رقم مالك الخط:")
    bot.register_next_step_handler(message, process_owner_number)

def process_owner_number(message):
    user_data['owner'] = message.text.strip()
    bot.send_message(message.chat.id, "الآن أدخل
