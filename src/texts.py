from src import config

class Texts:
    TEXTS = {
        "uz": {
            "welcome": (
                "👋 <b>Salom! Men {name} — AI-kontent eksperti.</b>\n\n"
                "Dekabrda neyrosetlar bilan <b>$7,000</b> topdim. Mening videolarim millionlab ko'rishlar olmoqda.\n\n"
                "Sizga <b>BEPUL dars</b> tayyorladim:\n"
                "<i>\"$200 lik AI-rolik sirlari — 2.7 mln ko'rishli rolik qanday yaratilgan\"</i>\n\n"
                "📥 Olish uchun Telegram kanalimga <b>obuna bo'ling:</b>"
            ),
            "not_subscribed": (
                "❌ <b>Siz hali kanalga obuna bo'lmagansiz.</b>\n\n"
                "Obuna bo'ling va qaytadan tekshiring 👇"
            ),
            "lesson_intro": "🎉 <b>Ajoyib! Mana sizning 1-bepul darsingiz:</b>",
            "lesson_1_ask": (
                "😎 <b>1-dars qanday bo'ldi?</b>\n\n"
                "Agar yoqgan bo'lsa, pastdagi tugmani bosing va men sizga <b>2-bepul darsni</b> yuboraman 👇"
            ),
            "lesson_2_intro": "🚀 <b>Mana 2-bepul dars!</b>\n\nBunisida yanada ko'proq praktika:",
            "lesson_materials": (
                "🎁 <b>Mana va'da qilingan materiallar:</b>\n\n"
                "1️⃣ <b>Prezentatsiya</b> (Barcha foydali havolalar ichida)\n"
                "2️⃣ <b>Tayyor Promptlar</b> (Darsda ishlatilgan)\n\n"
                "📥 Yuklab oling 👇"
            ),
            "lesson_outro": (
                "⏱ <b>2-darsni ham ko'rib bo'lganingizdan keyin pastdagi tugmani bosing.</b>\n\n"
                "Qo'shimча savollar bo'lsa — yozing, javob beraman!"
            ),
            "after_lesson": (
                "💪 <b>Zo'r! Qanday bo'ldi? Foydali bo'ldimi?</b>\n\n"
                "Endi sizda 2 ta yo'l bor:\n\n"
                "1️⃣ <b>Kursga hoziroq kirish</b>\n"
                "   → 16 ta instrument, 40 ta dars, sertifikat\n   \n"
                "2️⃣ <b>Bepul vebinarni kutish</b>\n"
                "   → 12 fevral, 18:00 da ko'proq ko'rsataman\n\n"
                "<b>Nima qilmoqchisiz?</b>"
            ),
            "offer_text": (
                "💪 <b>Zo'r! Darslar qanday bo'ldi?</b>\n\n"
                "Endi sizda tanlov bor:\n\n"
                "🚀 <b>MINI KURS</b>\n"
                "Qisqa va tez natija uchun.\n\n"
                "🏆 <b>FULL KURS (AI-Master)</b>\n"
                "To'liq kasb o'rganish va professional daraja.\n\n"
                "<b>Qaysi birini tanlaysiz?</b>"
            ),
            "tariffs_desc": (
                "📚 <b>AI-Kontent Master kursi</b>\n\n"
                "🔥 <b>RAMAZON CHEGIRMASI — 40% OFF</b>\n"
                "⏰ <i>Faqat Ramazon oxirigacha!</i>\n\n"
                "━━━━━━━━━━━━━━━\n"
                "💡 <b>LITE</b>\n"
                "━━━━━━━━━━━━━━━\n"
                f"~~{config.PRICES['LITE']['original']:,}~~ → <b>{config.PRICES['LITE']['full']:,} so'm</b>\n".replace(',', ' ') + 
                f"<i>Tejadingiz: {config.PRICES['LITE']['original'] - config.PRICES['LITE']['full']:,} so'm</i>\n\n".replace(',', ' ') +
                "✅ 40 ta dars zapisda\n"
                "✅ 100+ tayyor promptlar\n"
                "✅ Shablonlar\n"
                "✅ Umumiy chat\n"
                "✅ 6 oy dostup\n"
                "✅ Sertifikat\n\n"
                "━━━━━━━━━━━━━━━\n"
                "⭐ <b>PRO — TAVSIYA QILAMIZ</b>\n"
                "━━━━━━━━━━━━━━━\n"
                f"~~{config.PRICES['PRO']['original']:,}~~ → <b>{config.PRICES['PRO']['full']:,} so'm</b>\n".replace(',', ' ') +
                f"<i>Tejadingiz: {config.PRICES['PRO']['original'] - config.PRICES['PRO']['full']:,} so'm</i>\n\n".replace(',', ' ') +
                "LITE + yana:\n"
                "✅ <b>DZ tekshiruvi va fidbek</b>\n"
                "✅ Oyiga 1-2 jonli efir\n"
                "✅ Tayyor avtomatizatsiyalar\n"
                "✅ Jamoaga kirish imkoniyati\n\n"
                "━━━━━━━━━━━━━━━\n"
                "👑 <b>VIP</b>\n"
                "━━━━━━━━━━━━━━━\n"
                f"~~{config.PRICES['VIP']['original']:,}~~ → <b>{config.PRICES['VIP']['full']:,} so'm</b>\n".replace(',', ' ') +
                f"<i>Tejadingiz: {config.PRICES['VIP']['original'] - config.PRICES['VIP']['full']:,} so'm</i>\n\n".replace(',', ' ') +
                "PRO + yana:\n"
                "✅ 2 ta kechki ovqat avtor bilan\n"
                "✅ 60 daqiqa shaxsiy so'zlashuv (sozvon)\n"
                "✅ <b>Avtor bilan to'g'ridan aloqa</b>\n"
                "✅ Jamoaga prioritet\n\n"
                "⚠️ <b>Faqat 10 ta o'rin!</b>\n\n"
                "━━━━━━━━━━━━━━━\n"
                "💳 <b>Rassrochka: 50% hozir, 50% keyin</b>\n\n"
                "<b>Qaysini tanlaysiz?</b>"
            ),
            "selected_tariff_pro": (
                "⭐ <b>Siz PRO tarifini tanladingiz!</b>\n\n"
                f"Narx: <b>{config.PRICES['PRO']['full']:,} so'm</b>\n\n".replace(',', ' ') +
                "Qanday to'laysiz?\n\n"
                "━━━━━━━━━━━━━━━\n"
                "💳 <b>To'liq to'lash:</b> {config.PRICES['PRO']['full']:,} so'm\n".replace(',', ' ') +
                "→ Barcha modullarga dostup\n"
                "━━━━━━━━━━━━━━━\n"
                "📌 <b>Rassrochka:</b> 2 qismda\n"
                f"→ 1-qism: {config.PRICES['PRO']['half']:,} so'm (Modul 1-3)\n".replace(',', ' ') +
                f"→ 2-qism: {config.PRICES['PRO']['half']:,} so'm (Modul 4-8)\n".replace(',', ' ') +
                "━━━━━━━━━━━━━━━"
            ),
            "payment_instructions": (
                "💳 <b>To'lov ma'lumotlari</b>\n\n"
                "Tarif: <b>{tariff} ({type})</b>\n"
                "Summa: <b>{amount} so'm</b>\n\n"
                "━━━━━━━━━━━━━━━\n"
                "📱 <b>Click/Payme:</b>\n"
                f"Karta: <code>{config.CARD_NUMBER}</code>\n"
                f"Egasi: <b>{config.CARD_HOLDER}</b>\n"
                "━━━━━━━━━━━━━━━\n\n"
                "📝 <b>To'lovdan keyin:</b>\n"
                "1. Chek skrinshotini shu yerga yuboring\n"
                "2. Biz 24 soat ichida dostup ochamiz\n"
                "3. Kurs materiallarini olasiz\n\n"
                "⏳ <i>Chekni kutamiz...</i>"
            ),
            "receipt_accepted": (
                "✅ <b>Chek qabul qilindi!</b>\n\n"
                "Rahmat! Biz to'lovni tekshiramiz va 24 soat ichida dostup ochamiz.\n\n"
                "Sizga alohida xabar yuboramiz.\n\n"
                "Savollar bo'lsa — yozing!"
            ),
            "webinar_info": (
                "📅 <b>VEBINAR: 5-FEVRAL (Payshanba)</b>\n"
                "⏰ 19:00 Toshkent vaqti\n\n"
                "📍 Zoom / Google meets (linkni botga yoboramiz usha kuni)\n\n"
                "━━━━━━━━━━━━━━━━━━━\n\n"
                "<b>VEBINARLARDA NIMALAR KUTMOQDA:</b>\n\n"
                "🎯 20 ta AI instrument — jonli ko'rsataman\n"
                "🎯 10K obunachi kontent-plani — o'zingiz uchun tuzasiz\n"
                "🎯 $7000/oy sirlari — yashirmasdan aytaman\n"
                "🎯 Har bir videoga $200 olish yo'li\n\n"
                "━━━━━━━━━━━━━━━━━━━\n\n"
                "🎁 <b>5-FEVRAL SOVG'ALARI:</b>\n"
                "(kurs xaridorlari orasida)\n\n"
                "🎧 AirPods — 1 ta\n"
                "💵 1 000 000 so'm keshbek — 2 ta o'rin\n\n"
                "+ Maxfiy bonus vebinar ishtirokchilari uchun!"
            ),
            "webinar_confirmed": (
                "🎉 <b>Tabriklayman! Siz vebinarga muvaffaqiyatli ro'yxatdan o'tdingiz.</b>\n\n"
                "Siz <b>{num}-ishtirokchisiz</b> (Jami 1000 ta joy bor).\n\n"
                f"📅 <b>{config.WEBINAR_DATE}, {config.WEBINAR_TIME}</b> (Toshkent vaqti)\n\n"
                "Kuting! Biz albatta eslatamiz."
            ),
            "payment_confirmed_partial": (
                "🎉 <b>Tabriklaymiz! To'lov (1-qism) tasdiqlandi!</b>\n\n"
                "Sizga ochildi:\n"
                "✅ Modul 1: AI asoslari\n"
                "✅ Modul 2: Rasmlar generatsiyasi\n"
                "✅ Modul 3: Video generatsiya (asoslar)\n\n"
                f"📱 <b>Kurs platformasi:</b> {config.COURSE_PLATFORM_LINK}\n"
                f"💬 <b>Chat:</b> {config.CHAT_LINK}\n\n"
                "O'qishda omad! 🚀"
            ),
            "payment_confirmed_full": (
                "🎉 <b>Tabriklaymiz! To'liq to'lov tasdiqlandi!</b>\n\n"
                "Sizga <b>BARCHA MODULLAR</b> va <b>BONUSLAR</b> ochildi:\n"
                "✅ Modul 1-8 (Barcha darslar)\n"
                "✅ 100+ Promptlar bazasi\n"
                "✅ Yopiq VIP kanalga kirish\n\n"
                f"📱 <b>Kurs platformasi:</b> {config.COURSE_PLATFORM_LINK}\n"
                f"💬 <b>Chat:</b> {config.CHAT_LINK}\n\n"
                "Katta natijalar tilaymiz! 🚀"
            ),
            "language_select": "🇷🇺 Тилни танланг / Выберите язык:",
            "main_menu_text": "🏠",
            "menu_tariffs": "💰 Tariflar",
            "menu_webinar": "📅 Vebinar",
            "menu_lesson": "🎓 Bepul dars",
            "menu_support": "❓ Yordam",
            "menu_course": "📚 Mening kursim",
            "menu_mini_courses": "🚀 Mini kurslar",
            "course_menu_title": (
                "📚 <b>AI-KONTENT MASTER</b>\n\n"
                "Sizning progress: {progress}\n\n"
                "✅ Modul 0: Kirish\n"
                "✅ Modul 1: AI Asoslari\n"
                "🔄 Modul 2: Rasmlar\n"
                "...\n\n"
                "━━━━━━━━━━━━━━━\n"
                "Joriy dars: <b>{current_lesson}</b>\n"
                "━━━━━━━━━━━━━━━"
            ),
            "lesson_locked": (
                "🔒 <b>Bu modulga kirish cheklangan</b>\n\n"
                "Siz 50% to'lov qilgansiz va faqat Modul 1-3 ga dostupingiz bor.\n\n"
                "Modul 4-8 ni ochish uchun qolgan qismini to'lang:\n\n"
                "💰 Qolgan summa: <b>{amount} so'm</b>"
            ),
            "homework_prompt": (
                "━━━━━━━━━━━━━━━\n"
                "📝 <b>UYGA VAZIFA</b>\n"
                "━━━━━━━━━━━━━━━\n\n"
                "{text}\n\n"
                "━━━━━━━━━━━━━━━\n"
                "⚠️ DZ tekshirilgandan keyin keyingi modulga o'tasiz\n"
                "━━━━━━━━━━━━━━━"
            ),
            "submit_homework_btn": "📤 DZ yuborish",
            "homework_submit_instruction": (
                "📤 <b>DZ yuborish</b>\n\n"
                "Modul {module}, Dars {lesson} uchun vazifangizni yuboring.\n\n"
                "Qabul qilinadi:\n"
                "- 📷 Rasm (skrinshot)\n"
                "- 📄 Fayl (.txt, .doc, .pdf)\n"
                "- 🎬 Video\n"
                "- 🔗 Havola (matn sifatida)\n\n"
                "👇 Hozir yuboring:"
            ),
            "homework_received": (
                "✅ <b>DZ qabul qilindi!</b>\n\n"
                "Kurator 24-48 soat ichida tekshiradi.\n"
                "Natija haqida xabar beramiz."
            ),
            "homework_approved": (
                "🎉 <b>DZ tasdiqlandi!</b>\n\n"
                "Modul {module} muvaffaqiyatli tugallandi!\n\n"
                "Tabriklaymiz! Keyingi modulga o'tishingiz mumkin 👇"
            ),
            "homework_rejected": (
                "🔄 <b>DZni qayta topshirish kerak</b>\n\n"
                "Kurator fikri:\n"
                "━━━━━━━━━━━━━━━\n"
                "<i>\"{feedback}\"</i>\n"
                "━━━━━━━━━━━━━━━\n\n"
                "Iltimos, tuzatib qayta yuboring 👇"
            ),
            "course_finished": (
                "🎉🎉🎉 <b>TABRIKLAYMIZ!</b> 🎉🎉🎉\n\n"
                "Siz \"AI-Content Master\" kursini muvaffaqiyatli tugatdingiz!\n\n"
                "🏆 Sertifikat tayyorlanmoqda...\n"
                "24-48 soat ichida yuboramiz."
            ),
            "survey_intro_1": (
                "🎉 <b>Tabriklayman! Siz bepul darsni ko'rib bo'ldingiz!</b>\n\n"
                "Qanday bo'ldi? Foydali bo'ldimi?\n\n"
                "Fikringizni yozing — men har bir xabarni o'qiyman 👇"
            ),
            "survey_btn_start": "✍️ OPROSNIKKA O'TISH",
            "survey_intro_2": (
                "Rahmat fikringiz uchun! 🙏\n\n"
                "Sizga <b>MAXSUS TAKLIF</b> bor.\n\n"
                "2 ta <b>BEPUL VEBINAR</b> o'tkazaman:\n\n"
                "📅 5-FEVRAL — 1-qism\n"
                "📅 12-FEVRAL — 2-qism\n\n"
                "Bu oddiy vebinar emas. Bu sizning hayotingizni o'zgartirishi mumkin.\n\n"
                "⚠️ <b>O'rinlar cheklangan!</b>\n\n"
                "Joy band qilish uchun 6 ta savolga javob bering.\n"
                "Menejerimiz siz bilan bog'lanadi.\n\n"
                "Tayyormisiz?"
            ),
            "survey_btn_continue": "✅ Davom etish",
            "survey_btn_later": "🕐 Keyinroq",
            "survey_q1": "📝 <b>Savol 1/6</b>\n\nIsmingiz nima?",
            "survey_q2": "📝 <b>Savol 2/6</b>\n\nAsosiy faoliyatingiz nima?",
            "survey_q3": "📝 <b>Savol 3/6</b>\n\nAI bilan qanchalik tanishsiz?",
            "survey_q4": "📝 <b>Savol 4/6</b>\n\nAI o'rganishdan asosiy maqsadingiz nima?",
            "survey_q5": (
                "📝 <b>Savol 5/6 (YANGI — Nuqta A va Nuqta B)</b>\n\n"
                "Hozir qanday holatdasiz va AI bilan qanday holatga yetishni xohlaysiz?\n\n"
                "Misol: <i>\"Hozir oyiga 500$ topaman, AI bilan 2000$ topmoqchiman\"</i>\n"
                "Yoki: <i>\"Hozir kontent qilishga 5 soat ketadi, AI bilan 1 soatga tushirmoqchiman\"</i>\n\n"
                "O'zingizning A nuqtangiz va B nuqtangizni yozing 👇"
            ),
            "survey_q6": (
                "📝 <b>Savol 6/6</b>\n\n"
                "Telefon raqamingiz?\n\n"
                "(Menejerimiz siz bilan bog'lanadi va vebinarga qo'shadi)"
            ),
            "survey_completed": (
                "✅ <b>Rahmat! Ma'lumotlaringiz qabul qilindi.</b>\n\n"
                "Quyida vebinar haqida ma'lumot 👇"
            )
        },
        "ru": {
            "welcome": (
                "👋 <b>Привет! Я {name} — AI-контент эксперт.</b>\n\n"
                "В декабре я заработал <b>$7,000</b> с помощью нейросетей. Мои ролики набирают миллионы просмотров.\n\n"
                "Я приготовил для вас <b>БЕСПЛАТНЫЙ урок</b>:\n"
                "<i>\"Секреты AI-ролика за $200 — как создан ролик с 2.7 млн просмотров\"</i>\n\n"
                "📥 Чтобы получить, подпишитесь на Telegram канал:"
            ),
            "not_subscribed": (
                "❌ <b>Вы еще не подписались на канал.</b>\n\n"
                "Подпишитесь и проверьте снова 👇"
            ),
            "lesson_intro": "🎉 <b>Отлично! Вот ваш 1-й бесплатный урок:</b>\n\n📹 <i>\"Секреты AI-ролика за $200\"</i>",
            "lesson_1_ask": (
                "😎 <b>Как вам 1-й урок?</b>\n\n"
                "Если понравилось, нажмите кнопку ниже, и я отправлю <b>2-й бесплатный урок</b> 👇"
            ),
            "lesson_2_intro": "🚀 <b>Вот 2-й бесплатный урок!</b>\n\nЗдесь еще больше практики:",
            "lesson_materials": (
                "🎁 <b>Вот обещанные материалы:</b>\n\n"
                "1️⃣ <b>Презентация</b> (Все полезные ссылки внутри)\n"
                "2️⃣ <b>Готовые Промпты</b> (Использованные в уроке)\n\n"
                "📥 Скачивайте 👇"
            ),
            "lesson_outro": (
                 "⏱ <b>После просмотра 2-го урока нажмите кнопку ниже.</b>\n\n"
                 "Если есть вопросы — пишите, отвечу!"
            ),
            "after_lesson": (
                "💪 <b>Круто! Как вам? Было полезно?</b>\n\n"
                "Теперь у вас 2 пути:\n\n"
                "1️⃣ <b>Зайти на курс прямо сейчас</b>\n"
                "   → 16 инструментов, 40 уроков, сертификат\n   \n"
                "2️⃣ <b>Ждать бесплатный вебинар</b>\n"
                "   → 12 февраля, 18:00 покажу больше\n\n"
                "<b>Что выберете?</b>"
            ),
            "tariffs_desc": (
                "📚 <b>Курс AI-Контент Мастер</b>\n\n"
                "🔥 <b>СКИДКА В РАМАДАН — 40% OFF</b>\n"
                "⏰ <i>Только до конца Рамадана!</i>\n\n"
                "━━━━━━━━━━━━━━━\n"
                "💡 <b>LITE</b>\n"
                "━━━━━━━━━━━━━━━\n"
                f"~~{config.PRICES['LITE']['original']:,}~~ → <b>{config.PRICES['LITE']['full']:,} сум</b>\n".replace(',', ' ') + 
                f"<i>Экономия: {config.PRICES['LITE']['original'] - config.PRICES['LITE']['full']:,} сум</i>\n\n".replace(',', ' ') +
                "✅ 40 уроков в записи\n"
                "✅ 100+ готовых промптов\n"
                "✅ Шаблоны\n"
                "✅ Общий чат\n"
                "✅ 6 месяцев доступа\n"
                "✅ Сертификат\n\n"
                "━━━━━━━━━━━━━━━\n"
                "⭐ <b>PRO — РЕКОМЕНДУЕМ</b>\n"
                "━━━━━━━━━━━━━━━\n"
                f"~~{config.PRICES['PRO']['original']:,}~~ → <b>{config.PRICES['PRO']['full']:,} сум</b>\n".replace(',', ' ') +
                f"<i>Экономия: {config.PRICES['PRO']['original'] - config.PRICES['PRO']['full']:,} сум</i>\n\n".replace(',', ' ') +
                "LITE + еще:\n"
                "✅ <b>Проверка ДЗ и фидбек</b>\n"
                "✅ 1-2 прямых эфира в месяц\n"
                "✅ Готовые автоматизации\n"
                "✅ Возможность попасть в команду\n\n"
                "━━━━━━━━━━━━━━━\n"
                "👑 <b>VIP</b>\n"
                "━━━━━━━━━━━━━━━\n"
                f"~~{config.PRICES['VIP']['original']:,}~~ → <b>{config.PRICES['VIP']['full']:,} сум</b>\n".replace(',', ' ') +
                f"<i>Экономия: {config.PRICES['VIP']['original'] - config.PRICES['VIP']['full']:,} сум</i>\n\n".replace(',', ' ') +
                "PRO + еще:\n"
                "✅ 2 ужина с автором\n"
                "✅ 60 минут личный созвон\n"
                "✅ <b>Прямая связь с автором</b>\n"
                "✅ Приоритет в команду\n\n"
                "⚠️ <b>Только 10 мест!</b>\n\n"
                "━━━━━━━━━━━━━━━\n"
                "💳 <b>Рассрочка: 50% сейчас, 50% потом</b>\n\n"
                "<b>Какой выберете?</b>"
            ),
            "selected_tariff_pro": (
                "⭐ <b>Вы выбрали тариф PRO!</b>\n\n"
                f"Цена: <b>{config.PRICES['PRO']['full']:,} сум</b>\n\n".replace(',', ' ') +
                "Как будете платить?\n\n"
                "━━━━━━━━━━━━━━━\n"
                "💳 <b>Полная оплата:</b> {config.PRICES['PRO']['full']:,} сум\n".replace(',', ' ') +
                "→ Доступ ко всем модулям\n"
                "━━━━━━━━━━━━━━━\n"
                "📌 <b>Рассрочка:</b> в 2 этапа\n"
                f"→ 1 часть: {config.PRICES['PRO']['half']:,} сум (Модули 1-3)\n".replace(',', ' ') +
                f"→ 2 часть: {config.PRICES['PRO']['half']:,} сум (Модули 4-8)\n".replace(',', ' ') +
                "━━━━━━━━━━━━━━━"
            ),
             "payment_instructions": (
                "💳 <b>Информация об оплате</b>\n\n"
                "Тариф: <b>{tariff} ({type})</b>\n"
                "Сумма: <b>{amount} сум</b>\n\n"
                "━━━━━━━━━━━━━━━\n"
                "📱 <b>Click/Payme:</b>\n"
                f"Карта: <code>{config.CARD_NUMBER}</code>\n"
                f"Владелец: <b>{config.CARD_HOLDER}</b>\n"
                "━━━━━━━━━━━━━━━\n\n"
                "📝 <b>После оплаты:</b>\n"
                "1. Отправьте скриншот чека сюда\n"
                "2. Мы откроем доступ в течение 24 часов\n"
                "3. Вы получите материалы курса\n\n"
                "⏳ <i>Ждем чек...</i>"
            ),
            "receipt_accepted": (
                "✅ <b>Чек принят!</b>\n\n"
                "Спасибо! Мы проверим оплату и откроем доступ в течение 24 часов.\n\n"
                "Мы пришлем вам отдельное сообщение.\n\n"
                "Если есть вопросы — пишите!"
            ),
            "webinar_info": (
                "📅 <b>VEBINAR: 5-FEVRAL (Payshanba)</b>\n"
                "⏰ 19:00 Toshkent vaqti\n\n"
                "📍 Zoom / Google meets (linkni botga yoboramiz usha kuni)\n\n"
                "━━━━━━━━━━━━━━━━━━━\n\n"
                "<b>VEBINARLARDA NIMALAR KUTMOQDA:</b>\n\n"
                "🎯 20 ta AI instrument — jonli ko'rsataman\n"
                "🎯 10K obunachi kontent-plani — o'zingiz uchun tuzasiz\n"
                "🎯 $7000/oy sirlari — yashirmasdan aytaman\n"
                "🎯 Har bir videoga $200 olish yo'li\n\n"
                "━━━━━━━━━━━━━━━━━━━\n\n"
                "🎁 <b>5-FEVRAL SOVG'ALARI:</b>\n"
                "(kurs xaridorlari orasida)\n\n"
                "🎧 AirPods — 1 ta\n"
                "💵 1 000 000 so'm keshbek — 2 ta o'rin\n\n"
                "+ Maxfiy bonus vebinar ishtirokchilari uchun!"
            ),
            "webinar_confirmed": (
                "🎉 <b>Поздравляем! Вы успешно зарегистрировались на вебинар.</b>\n\n"
                "Вы <b>{num}-й участник</b> (Всего 1000 мест).\n\n"
                f"📅 <b>{config.WEBINAR_DATE}, {config.WEBINAR_TIME}</b> (Ташкент)\n\n"
                "Мы напомним!"
            ),
            "payment_confirmed_partial": (
                "🎉 <b>Поздравляем! Частичная оплата подтверждена!</b>\n\n"
                "Вам открыто (Модули 1-3):\n"
                "✅ Модуль 1: Основы AI\n"
                "✅ Модуль 2: Генерация изображений\n"
                "✅ Модуль 3: Генерация видео (основы)\n\n"
                f"📱 <b>Платформа курса:</b> {config.COURSE_PLATFORM_LINK}\n"
                f"💬 <b>Чат:</b> {config.CHAT_LINK}\n\n"
                "Удачи в обучении! 🚀"
            ),
            "payment_confirmed_full": (
                "🎉 <b>Поздравляем! Полная оплата подтверждена!</b>\n\n"
                "Вам открыт <b>ПОЛНЫЙ ДОСТУП</b>:\n"
                "✅ Модули 1-8 (Все уроки)\n"
                "✅ 100+ База промптов\n"
                "✅ Доступ в VIP канал\n\n"
                f"📱 <b>Платформа курса:</b> {config.COURSE_PLATFORM_LINK}\n"
                f"💬 <b>Чат:</b> {config.CHAT_LINK}\n\n"
                "Добро пожаловать в команду! 🚀"
            ),
            "language_select": "🇷🇺 Тилни танланг / Выберите язык:",
            "main_menu_text": "🏠 <b>Главное меню / Асосий меню</b>",
            "menu_tariffs": "💰 Тарифы",
            "menu_webinar": "📅 Вебинар",
            "menu_lesson": "🎓 Урок",
            "menu_support": "❓ Помощь",
            "menu_course": "📚 Мой курс",
            "menu_mini_courses": "🚀 Мини-курсы",
            "course_menu_title": (
                "📚 <b>AI-CONTENT MASTER</b>\n\n"
                "Ваш прогресс: {progress}\n\n"
                "✅ Модуль 0: Введение\n"
                "✅ Модуль 1: Основы AI\n"
                "🔄 Модуль 2: Картинки\n"
                "...\n\n"
                "━━━━━━━━━━━━━━━\n"
                "Текущий урок: <b>{current_lesson}</b>\n"
                "━━━━━━━━━━━━━━━"
            ),
            "lesson_locked": (
                "🔒 <b>Доступ к этому модулю ограничен</b>\n\n"
                "Вы оплатили 50% и у вас есть доступ к Модулям 1-3.\n\n"
                "Чтобы открыть Модули 4-8, оплатите остаток:\n\n"
                "💰 Остаток: <b>{amount} сум</b>"
            ),
             "homework_prompt": (
                "━━━━━━━━━━━━━━━\n"
                "📝 <b>ДОМАШНЕЕ ЗАДАНИЕ</b>\n"
                "━━━━━━━━━━━━━━━\n\n"
                "{text}\n\n"
                "━━━━━━━━━━━━━━━\n"
                "⚠️ Вы перейдете к следующему модулю после проверки ДЗ\n"
                "━━━━━━━━━━━━━━━"
            ),
            "submit_homework_btn": "📤 Отправить ДЗ",
            "homework_submit_instruction": (
                "📤 <b>Отправка ДЗ</b>\n\n"
                "Отправьте задание для Модуля {module}, Урок {lesson}.\n\n"
                "Принимаем:\n"
                "- 📷 Фото (скриншот)\n"
                "- 📄 Файл (.txt, .doc, .pdf)\n"
                "- 🎬 Видео\n"
                "- 🔗 Ссылку (текстом)\n\n"
                "👇 Отправьте сейчас:"
            ),
            "homework_received": (
                "✅ <b>ДЗ принято!</b>\n\n"
                "Куратор проверит в течение 24-48 часов.\n"
                "Мы сообщим о результате."
            ),
            "homework_approved": (
                "🎉 <b>ДЗ принято!</b>\n\n"
                "Модуль {module} успешно завершен!\n\n"
                "Поздравляем! Можете переходить к следующему модулю 👇"
            ),
            "homework_rejected": (
                "🔄 <b>ДЗ нужно переделать</b>\n\n"
                "Комментарий куратора:\n"
                "━━━━━━━━━━━━━━━\n"
                "<i>\"{feedback}\"</i>\n"
                "━━━━━━━━━━━━━━━\n\n"
                "Пожалуйста, исправьте и отправьте снова 👇"
            ), 
            "course_finished": (
                "🎉🎉🎉 <b>ПОЗДРАВЛЯЕМ!</b> 🎉🎉🎉\n\n"
                "Вы успешно завершили курс \"AI-Content Master\"!\n\n"
                "🏆 Сертификат готовится...\n"
                "Мы пришлем его в течение 24-48 часов."
            ),

            "survey_intro_1": (
                "🎉 <b>Поздравляю! Вы посмотрели бесплатный урок!</b>\n\n"
                "Как вам? Было полезно?\n\n"
                "Напишите ваше мнение — я читаю каждое сообщение 👇"
            ),
            "survey_btn_start": "✍️ ПРОЙТИ ОПРОС",
            "survey_intro_2": (
                "Спасибо за отзыв! 🙏\n\n"
                "У меня есть <b>СПЕЦИАЛЬНОЕ ПРЕДЛОЖЕНИЕ</b>.\n\n"
                "Я проведу 2 <b>БЕСПЛАТНЫХ ВЕБИНАРА</b>:\n\n"
                "📅 5 ФЕВРАЛЯ — 1-я часть\n"
                "📅 12 ФЕВРАЛЯ — 2-я часть\n\n"
                "Это не просто вебинар. Это может изменить вашу жизнь.\n\n"
                "⚠️ <b>Места ограничены!</b>\n\n"
                "Чтобы занять место, ответьте на 6 вопросов.\n"
                "Наш менеджер свяжется с вами.\n\n"
                "Готовы?"
            ),
            "survey_btn_continue": "✅ Продолжить",
            "survey_btn_later": "🕐 Позже",
            "survey_q1": "📝 <b>Вопрос 1/6</b>\n\nКак вас зовут?",
            "survey_q2": "📝 <b>Вопрос 2/6</b>\n\nВаша основная деятельность?",
            "survey_q3": "📝 <b>Вопрос 3/6</b>\n\nНасколько вы знакомы с AI?",
            "survey_q4": "📝 <b>Вопрос 4/6</b>\n\nКакова ваша цель изучения AI?",
            "survey_q5": (
                "📝 <b>Вопрос 5/6 (НОВЫЙ — Точка А и Точка Б)</b>\n\n"
                "Какова ваша текущая ситуация и к чему вы хотите прийти с AI?\n\n"
                "Пример: <i>\"Сейчас зарабатываю $500, хочу $2000 с помощью AI\"</i>\n"
                "Или: <i>\"Трачу 5 часов на контент, хочу тратить 1 час\"</i>\n\n"
                "Напишите вашу точку А и точку Б 👇"
            ),
            "survey_q6": (
                "📝 <b>Вопрос 6/6</b>\n\n"
                "Ваш номер телефона?\n\n"
                "(Наш менеджер свяжется с вами и добавит на вебинар)"
            ),
            "survey_completed": (
                "✅ <b>Спасибо! Ваши данные приняты.</b>\n\n"
                "━━━━━━━━━━━━━━━━━━━\n\n"
                "📅 <b>ВЕБИНАР: 5 ФЕВРАЛЯ (Четверг)</b>\n"
                "⏰ 19:00 по Ташкенту\n\n"
                "📍 Zoom / Google meets (ссылку пришлем в бота в тот же день)\n\n"
                "━━━━━━━━━━━━━━━━━━━\n\n"
                "<b>ЧТО ВАС ЖДЕТ НА ВЕБИНАРАХ:</b>\n\n"
                "🎯 20 AI инструментов — покажу вживую\n"
                "🎯 Контент-план на 10K подписчиков — составите для себя\n"
                "🎯 Секреты $7000/мес — расскажу честно\n"
                "🎯 Как брать $200 за один ролик\n\n"
                "━━━━━━━━━━━━━━━━━━━\n\n"
                "🎁 <b>ПОДАРКИ 5 ФЕВРАЛЯ:</b>\n"
                "(среди покупателей курса)\n\n"
                "🎧 AirPods — 1 шт\n"
                "💵 1 000 000 сум кэшбек — 2 места\n\n"
                "+ Секретный бонус для участников вебинара!"
            ),

        }
    }

    @classmethod
    def get(cls, key: str, lang: str = "uz") -> str:
        return cls.TEXTS.get(lang, cls.TEXTS["uz"]).get(key, "")
