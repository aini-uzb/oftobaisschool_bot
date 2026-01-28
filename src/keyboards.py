from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from src import config
from src import texts

def get_language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="lang_uz"))
    builder.row(InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="lang_ru"))
    return builder.as_markup()

def get_main_menu_keyboard(lang: str = "uz"):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=texts.Texts.get("menu_course", lang)))
    builder.row(
        KeyboardButton(text=texts.Texts.get("menu_tariffs", lang)),
        KeyboardButton(text=texts.Texts.get("menu_webinar", lang))
    )
    builder.row(
        KeyboardButton(text=texts.Texts.get("menu_mini_courses", lang)),
        KeyboardButton(text=texts.Texts.get("menu_lesson", lang))
    )
    builder.row(KeyboardButton(text=texts.Texts.get("menu_support", lang)))
    return builder.as_markup(resize_keyboard=True)

def get_subscription_keyboard(lang: str = "uz"):
    text_channel = "📢 Kanalga o'tish" if lang == "uz" else "📢 Перейти в канал"
    text_check = "✅ Obuna bo'ldim" if lang == "uz" else "✅ Я подписался"
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_channel, url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@', '')}"))
    builder.row(InlineKeyboardButton(text=text_check, callback_data="check_subscription"))
    return builder.as_markup()

def get_retry_subscription_keyboard(lang: str = "uz"):
    text_channel = "📢 Kanalga o'tish" if lang == "uz" else "📢 Перейти в канал"
    text_check = "🔄 Qayta tekshirish" if lang == "uz" else "🔄 Проверить снова"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_channel, url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@', '')}"))
    builder.row(InlineKeyboardButton(text=text_check, callback_data="check_subscription"))
    return builder.as_markup()

def get_lesson_1_watched_keyboard(lang: str = "uz"):
    text = "🔥 2-bepul darsni olish" if lang == "uz" else "🔥 Получить 2-й урок"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text, callback_data="get_lesson_2"))
    return builder.as_markup()

def get_lesson_2_watched_keyboard(lang: str = "uz"):
    text = "✅ 2-darsni ko'rdim" if lang == "uz" else "✅ Я посмотрел 2-й урок"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text, callback_data="watched_lesson"))
    return builder.as_markup()

def get_offer_keyboard(lang: str = "uz"):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🚀 Mini Kurs", callback_data="offer_mini"))
    builder.row(InlineKeyboardButton(text="🏆 Full Kurs (AI-Master)", callback_data="show_tariffs"))
    return builder.as_markup()

def get_lesson_watched_keyboard(lang: str = "uz"):
    # This is for the Survey Intro step
    text = texts.Texts.get("survey_btn_start", lang)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text, callback_data="start_survey_intro"))
    return builder.as_markup()

def get_survey_choice_keyboard(lang: str = "uz"):
    text_continue = texts.Texts.get("survey_btn_continue", lang)
    text_later = texts.Texts.get("survey_btn_later", lang)
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_continue, callback_data="survey_start_q1"))
    builder.row(InlineKeyboardButton(text=text_later, callback_data="survey_later"))
    return builder.as_markup()

def get_activity_keyboard(lang: str = "uz"):
    builder = ReplyKeyboardBuilder()
    options = [
        "Tadbirkor 💼" if lang == "uz" else "Предприниматель 💼",
        "Frilanser 💻" if lang == "uz" else "Фрилансер 💻",
        "SMM/Marketolog 📱" if lang == "uz" else "SMM/Маркетолог 📱",
        "Kontent-meyker 🎬" if lang == "uz" else "Контент-мейкер 🎬",
        "Ishlayman (yollanma) 👔" if lang == "uz" else "Работаю по найму 👔",
        "Talaba 🎓" if lang == "uz" else "Студент 🎓",
        "Boshqa" if lang == "uz" else "Другое"
    ]
    for opt in options:
        builder.row(KeyboardButton(text=opt))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_knowledge_keyboard(lang: str = "uz"):
    builder = ReplyKeyboardBuilder()
    options = [
        "Umuman bilmayman 🆕" if lang == "uz" else "Вообще не знаю 🆕",
        "Ozgina sinab ko'rganman 🔰" if lang == "uz" else "Немного пробовал 🔰",
        "Ba'zi instrumentlarni ishlataman ⚡" if lang == "uz" else "Использую некоторые инструменты ⚡",
        "Yaxshi bilaman, chuqurroq o'rganmoqchiman 🚀" if lang == "uz" else "Знаю хорошо, хочу углубить 🚀"
    ]
    for opt in options:
        builder.row(KeyboardButton(text=opt))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_goal_keyboard(lang: str = "uz"):
    builder = ReplyKeyboardBuilder()
    options = [
        "Shaxsiy blog/kontent uchun 📸" if lang == "uz" else "Для личного блога/контента 📸",
        "Biznesimga qo'llash uchun 💼" if lang == "uz" else "Для бизнеса 💼",
        "Yangi kasb/daromad uchun 💰" if lang == "uz" else "Для новой профессии/дохода 💰",
        "Vaqtimni tejash uchun ⏰" if lang == "uz" else "Для экономии времени ⏰",
        "Shunchaki qiziq 🤔" if lang == "uz" else "Просто интересно 🤔"
    ]
    for opt in options:
        builder.row(KeyboardButton(text=opt))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_contact_keyboard(lang: str = "uz"):
    text = "📱 Telefon raqamni yuborish" if lang == "uz" else "📱 Отправить номер телефона"
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=text, request_contact=True))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_main_choice_keyboard(lang: str = "uz"):
    text_tariffs = "💰 Kurs tariflarini ko'rish" if lang == "uz" else "💰 Посмотреть тарифы"
    text_webinar = "📅 Vebinarga yozilish" if lang == "uz" else "📅 Записаться на вебинар"
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_tariffs, callback_data="show_tariffs"))
    builder.row(InlineKeyboardButton(text=text_webinar, callback_data="register_webinar"))
    return builder.as_markup()

def get_tariffs_keyboard(lang: str = "uz"):
    help_text = "❓ Savolim bor" if lang == "uz" else "❓ Есть вопрос"
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💡 LITE — 3 млн", callback_data="select_lite"))
    builder.row(InlineKeyboardButton(text="⭐ PRO — 6 млн", callback_data="select_pro"))
    builder.row(InlineKeyboardButton(text="👑 VIP — 25 mln", callback_data="select_vip"))
    builder.row(InlineKeyboardButton(text=help_text, url="https://t.me/oftobaischoolsupport"))
    return builder.as_markup()

def get_pro_payment_options_keyboard(lang: str = "uz"):
    text_full = f"💳 To'liq to'lash — {config.PRICES['PRO']['full']//1000000} mln" if lang == "uz" else f"💳 Полная оплата — {config.PRICES['PRO']['full']//1000000} млн"
    text_half = f"📌 Rassrochka — {config.PRICES['PRO']['half']//1000000} mln hozir" if lang == "uz" else f"📌 Рассрочка — {config.PRICES['PRO']['half']//1000000} млн сейчас"
    text_back = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_full, callback_data="pay_pro_full"))
    builder.row(InlineKeyboardButton(text=text_half, callback_data="pay_pro_half"))
    builder.row(InlineKeyboardButton(text=text_back, callback_data="show_tariffs"))
    return builder.as_markup()

def get_lite_payment_options_keyboard(lang: str = "uz"):
    text_full = f"💳 To'liq to'lash — {config.PRICES['LITE']['full']//1000000} mln" if lang == "uz" else f"💳 Полная оплата — {config.PRICES['LITE']['full']//1000000} млн"
    text_half = f"📌 Rassrochka — {config.PRICES['LITE']['half']//1000000} mln hozir" if lang == "uz" else f"📌 Рассрочка — {config.PRICES['LITE']['half']//1000000} млн сейчас"
    text_back = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_full, callback_data="pay_lite_full"))
    builder.row(InlineKeyboardButton(text=text_half, callback_data="pay_lite_half"))
    builder.row(InlineKeyboardButton(text=text_back, callback_data="show_tariffs"))
    return builder.as_markup()

def get_vip_payment_options_keyboard(lang: str = "uz"):
    text_full = f"💳 To'liq to'lash — {config.PRICES['VIP']['full']//1000000} mln" if lang == "uz" else f"💳 Полная оплата — {config.PRICES['VIP']['full']//1000000} млн"
    text_half = f"📌 Bron (50%) — {config.PRICES['VIP']['half']//1000000} mln" if lang == "uz" else f"📌 Бронь (50%) — {config.PRICES['VIP']['half']//1000000} млн"
    text_back = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_full, callback_data="pay_vip_full"))
    builder.row(InlineKeyboardButton(text=text_half, callback_data="pay_vip_half"))
    builder.row(InlineKeyboardButton(text=text_back, callback_data="show_tariffs"))
    return builder.as_markup()

def get_payment_back_keyboard(back_target: str, lang: str = "uz"):
    text_back = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    text_help = "❓ Yordam kerak" if lang == "uz" else "❓ Нужна помощь"
    
    # Map back_target to callback
    if back_target == "pro":
        cb = "select_pro"
    elif back_target == "lite":
        cb = "select_lite"
    elif back_target == "vip":
        cb = "select_vip"
    else:
        cb = "show_tariffs"
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_help, url="https://t.me/oftobaischoolsupport"))
    builder.row(InlineKeyboardButton(text=text_back, callback_data=cb))
    return builder.as_markup()

def get_webinar_keyboard(lang: str = "uz"):
    text_register = "✅ Ro'yxatdan o'tish" if lang == "uz" else "✅ Зарегистрироваться"
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_register, callback_data="confirmed_webinar"))
    return builder.as_markup()

def get_admin_payment_keyboard(payment_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_pay_{payment_id}"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"reject_pay_{payment_id}")
    )
    return builder.as_markup()

def get_lesson_keyboard(module_id: int, lesson_id: int, lang: str = "uz"):
    # Previous/Next
    builder = InlineKeyboardBuilder()
    # ... Simplified for now
    return builder.as_markup()

def get_lesson_locked_keyboard(amount: int, lang: str = "uz"):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f"💳 To'lash: {amount} sum", callback_data="pay_remaining"))
    return builder.as_markup()

def get_mini_course_keyboard(lang: str = "uz"):
    text = "🚀 Mini Kurslar" if lang == "uz" else "🚀 Мини-курсы"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text, callback_data="list_mini_courses"))
    return builder.as_markup()

def get_mini_courses_list_keyboard(lang: str = "uz"):
    builder = InlineKeyboardBuilder()
    text_course = "1. Birinchi million prosmotr olgan AI videoyingiz"
    builder.row(InlineKeyboardButton(text=text_course, callback_data="mini_course_1"))
    
    text_back = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    builder.row(InlineKeyboardButton(text=text_back, callback_data="delete_msg")) 
    return builder.as_markup()

def get_course_modules_keyboard(lang: str = "uz"):
    from src.data.lessons import MODULE_NAMES
    builder = InlineKeyboardBuilder()
    
    # Sort modules by ID
    for mod_id in sorted(MODULE_NAMES.keys()):
        name = MODULE_NAMES[mod_id]
        text = f"Modul {mod_id}: {name}"
        builder.row(InlineKeyboardButton(text=text, callback_data=f"open_module_{mod_id}"))
        
    return builder.as_markup()

def get_module_lessons_keyboard(module_id: int, lang: str = "uz"):
    from src.data.lessons import LESSONS
    builder = InlineKeyboardBuilder()
    
    # Filter lessons by module
    module_lessons = []
    for lid, data in LESSONS.items():
        if data["module"] == module_id:
            module_lessons.append((lid, data))
            
    # Sort by lesson ID
    module_lessons.sort(key=lambda x: float(x[0]))
    
    for lid, data in module_lessons:
        text = f"{lid}. {data['title']}"
        builder.row(InlineKeyboardButton(text=text, callback_data=f"lesson_{lid}"))
        
    text_back = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    builder.row(InlineKeyboardButton(text=text_back, callback_data="open_course"))
    
    
    return builder.as_markup()

def get_broadcast_confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Ha, yuborish (Да, отправить)", callback_data="broadcast_confirm"),
        InlineKeyboardButton(text="❌ Bekor qilish (Отмена)", callback_data="broadcast_cancel")
    )
    return builder.as_markup()
