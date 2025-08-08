import asyncio
import time
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# --- استيراد دوال سكربت فودافون ---

from vodafone_script import (
    login,
    send_invitation,
    Accept_invitation,
    Change_quota,
    Delete_member,
    info_felix,
    password_owner,
    member1,
    member2,
    password_member2,
    owner
)

# مراحل المحادثة
ENTER_NUMBER = 1

# متغير تحكم في الإيقاف
running_task = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً! من فضلك أدخل رقم الهاتف الذي تريد تشغيل السكربت عليه:"
    )
    return ENTER_NUMBER


async def receive_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running_task
    number = update.message.text.strip()
    context.user_data['number'] = number

    await update.message.reply_text(f"تم استلام الرقم: {number}\nسيبدأ التشغيل الآن...")

    # تشغيل المهمة في خلفية أسينك
    running_task = asyncio.create_task(run_script(update, context, number))

    return ConversationHandler.END


async def run_script(update: Update, context: ContextTypes.DEFAULT_TYPE, number: str):
    chat_id = update.effective_chat.id

    # تسجيل الدخول على حساب owner و member2
    await context.bot.send_message(chat_id, "جار تسجيل الدخول...")
    access_owner = login(owner, password_owner)
    access_member2 = login(member2, password_member2)

    if not access_owner or not access_member2:
        await context.bot.send_message(chat_id, "فشل تسجيل الدخول. يرجى التأكد من البيانات.")
        return

    number_loop = 40

    for i in range(number_loop):
        # تحقق هل تم إلغاء المهمة
        if running_task.cancelled():
            await context.bot.send_message(chat_id, "تم إلغاء التنفيذ.")
            return

        # إرسال action typing (تفكير) 50 ثانية
        for _ in range(10):
            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(5)

        await context.bot.send_message(chat_id, f"بدء تنفيذ الدورة رقم {i + 1} من {number_loop} ...")

        time.sleep(10)
        send_invitation("send invitation member 2 =>", owner, member2, access_owner, quota="40")
        time.sleep(10)
        Change_quota("Change percentage member1 from 1300 to 5200 =>", owner, member1, access_owner, quota="40")
        time.sleep(10)
        Accept_invitation("Accept member 2=>", owner, member2, access_member2)
        time.sleep(10)
        Delete_member("Remove member 2=>", owner, member2, access_owner)
        time.sleep(10)
        info_felix(owner, password_owner, access_owner)

        await context.bot.send_message(chat_id, f"انتهت الدورة رقم {i + 1}.")

        time.sleep(11 * 60)

        Change_quota("Change percentage member1 1300=>", owner, member1, access_owner, quota="10")

    await context.bot.send_message(chat_id, "تم الانتهاء من تنفيذ جميع الدورات بنجاح ✅")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running_task
    if running_task:
        running_task.cancel()
        running_task = None
        await update.message.reply_text("تم إيقاف التنفيذ بنجاح.")
    else:
        await update.message.reply_text("لا توجد عملية تعمل حالياً.")


if __name__ == '__main__':
    import os

    TOKEN = os.getenv("6927966683:AAHGSfdNmM9aVB_F7qUnQv0KCuq_eGqaklY")  # ضع التوكن هنا أو في متغير بيئي

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTER_NUMBER: [MessageHandler(filters.TEXT & (~filters.COMMAND), receive_number)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('cancel', cancel))

    print("البوت يعمل ...")
    app.run_polling()
