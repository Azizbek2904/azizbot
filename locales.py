"""
Tarjimalar (O'zbek va Rus tillari).
Foydalanish: t("key", lang)
"""

TRANSLATIONS = {
    # ──────────── UMUMIY ────────────
    "choose_language": {
        "uz": "🌐 Tilni tanlang / Выберите язык:",
        "ru": "🌐 Tilni tanlang / Выберите язык:",
    },
    "language_set": {
        "uz": "✅ Til o'zbek tiliga o'rnatildi",
        "ru": "✅ Язык установлен на русский",
    },
    "welcome": {
        "uz": "👋 Salom, {name}!\n\nBotimizga xush kelibsiz! Bu yerda eng zo'r <b>aksiyalar</b> va sovg'ali <b>konkurslar</b> sizni kutmoqda 🎁",
        "ru": "👋 Привет, {name}!\n\nДобро пожаловать! Здесь вас ждут лучшие <b>акции</b> и <b>конкурсы</b> с призами 🎁",
    },
    "welcome_referral": {
        "uz": "🎉 Sizni do'stingiz taklif qildi! Botdan foydalanish uchun pastdagi shartlarni bajaring.",
        "ru": "🎉 Вас пригласил друг! Чтобы пользоваться ботом, выполните условия ниже.",
    },
    "back": {"uz": "⬅️ Orqaga", "ru": "⬅️ Назад"},
    "cancel": {"uz": "❌ Bekor qilish", "ru": "❌ Отменить"},
    "confirm": {"uz": "✅ Tasdiqlash", "ru": "✅ Подтвердить"},
    "yes": {"uz": "✅ Ha", "ru": "✅ Да"},
    "no": {"uz": "❌ Yo'q", "ru": "❌ Нет"},
    "skip": {"uz": "⏭ O'tkazib yuborish", "ru": "⏭ Пропустить"},
    "main_menu": {"uz": "🏠 Asosiy menyu", "ru": "🏠 Главное меню"},
    "cancelled": {"uz": "❌ Bekor qilindi", "ru": "❌ Отменено"},
    "error": {"uz": "❌ Xatolik yuz berdi", "ru": "❌ Произошла ошибка"},
    "success": {"uz": "✅ Muvaffaqiyatli", "ru": "✅ Успешно"},

    # ──────────── MAJBURIY OBUNA ────────────
    "subscription_required": {
        "uz": "📢 <b>Botdan foydalanish uchun quyidagi kanal(lar)ga obuna bo'ling:</b>\n\nObuna bo'lgach <b>✅ Tekshirish</b> tugmasini bosing.",
        "ru": "📢 <b>Для использования бота подпишитесь на каналы ниже:</b>\n\nПосле подписки нажмите <b>✅ Проверить</b>.",
    },
    "check_subscription": {"uz": "✅ Tekshirish", "ru": "✅ Проверить"},
    "subscription_failed": {
        "uz": "⚠️ Siz hali barcha kanallarga obuna bo'lmagansiz!\nIltimos, obuna bo'ling va qaytadan tekshiring.",
        "ru": "⚠️ Вы ещё не подписались на все каналы!\nПодпишитесь и проверьте снова.",
    },
    "subscription_success": {
        "uz": "✅ Ajoyib! Endi botdan to'liq foydalanishingiz mumkin 🎉",
        "ru": "✅ Отлично! Теперь вы можете использовать бота 🎉",
    },

    # ──────────── ASOSIY MENYU ────────────
    "btn_ads": {"uz": "🎁 Aksiyalar", "ru": "🎁 Акции"},
    "btn_contests": {"uz": "🏆 Konkurslar", "ru": "🏆 Конкурсы"},
    "btn_my_link": {"uz": "🔗 Mening havolam", "ru": "🔗 Моя ссылка"},
    "btn_my_friends": {"uz": "👥 Mening do'stlarim", "ru": "👥 Мои друзья"},
    "btn_top": {"uz": "📊 TOP reyting", "ru": "📊 ТОП рейтинг"},
    "btn_info": {"uz": "ℹ️ Ma'lumot", "ru": "ℹ️ Информация"},
    "btn_settings": {"uz": "⚙️ Sozlamalar", "ru": "⚙️ Настройки"},

    # ──────────── AKSIYALAR ────────────
    "ads_title": {
        "uz": "🎁 <b>Faol aksiyalar:</b>\n\nQuyida sizni kutayotgan eng yaxshi takliflar:",
        "ru": "🎁 <b>Активные акции:</b>\n\nЛучшие предложения, которые ждут вас:",
    },
    "no_ads": {
        "uz": "📭 Hozircha faol aksiyalar yo'q. Tez orada yangi aksiyalar bo'ladi!",
        "ru": "📭 Пока нет активных акций. Скоро появятся новые!",
    },
    "btn_get": {"uz": "🛒 Olish", "ru": "🛒 Получить"},
    "btn_share": {"uz": "📢 Ulashish", "ru": "📢 Поделиться"},

    # ──────────── KONKURSLAR ────────────
    "contests_title": {
        "uz": "🏆 <b>Faol konkurslar:</b>\n\nDo'stlaringizni taklif qiling va sovg'a yutib oling!",
        "ru": "🏆 <b>Активные конкурсы:</b>\n\nПриглашайте друзей и выигрывайте призы!",
    },
    "no_contests": {
        "uz": "📭 Hozircha faol konkurslar yo'q. Kuting, tez orada qiziqarli konkurslar bo'ladi!",
        "ru": "📭 Пока нет активных конкурсов. Скоро появятся интересные конкурсы!",
    },
    "btn_participate": {"uz": "🚀 Ishtirok etish", "ru": "🚀 Участвовать"},
    "contest_ends": {"uz": "⏰ Tugaydi:", "ru": "⏰ Заканчивается:"},
    "contest_participants": {"uz": "👥 Ishtirokchilar:", "ru": "👥 Участников:"},
    "contest_prizes": {"uz": "🎁 <b>Sovg'alar:</b>", "ru": "🎁 <b>Призы:</b>"},
    "joined_contest": {
        "uz": "🎉 <b>Tabriklaymiz! Siz konkurs ishtirokchisisiz!</b>\n\n👉 Mana sizning shaxsiy havolangiz:\n<code>{link}</code>\n\nBu havolani do'stlaringizga yuboring. Har bir yangi obunachi = <b>+1 ball</b>",
        "ru": "🎉 <b>Поздравляем! Вы участник конкурса!</b>\n\n👉 Ваша персональная ссылка:\n<code>{link}</code>\n\nОтправьте её друзьям. Каждый новый подписчик = <b>+1 балл</b>",
    },
    "already_in_contest": {
        "uz": "ℹ️ Siz allaqachon bu konkursda ishtirok etyapsiz.\nSizning ballaringiz: <b>{count}</b>",
        "ru": "ℹ️ Вы уже участвуете в этом конкурсе.\nВаши баллы: <b>{count}</b>",
    },

    # ──────────── MENING HAVOLAM ────────────
    "my_link_title": {
        "uz": "🔗 <b>Sizning shaxsiy havolangiz:</b>\n\n<code>{link}</code>\n\n📊 Statistika:\n👥 Taklif qilingan: <b>{count}</b> ta\n\nBu havolani do'stlaringizga ulashing va sovg'alar yutib oling!",
        "ru": "🔗 <b>Ваша персональная ссылка:</b>\n\n<code>{link}</code>\n\n📊 Статистика:\n👥 Приглашено: <b>{count}</b>\n\nПоделитесь ссылкой с друзьями и выигрывайте призы!",
    },
    "btn_share_link": {"uz": "📤 Ulashish", "ru": "📤 Поделиться"},
    "btn_copy_link": {"uz": "📋 Nusxa olish", "ru": "📋 Скопировать"},
    "share_text": {
        "uz": "🎁 Sovg'a yutib oling! Bu botda ajoyib aksiyalar va konkurslar bor:\n\n",
        "ru": "🎁 Выиграйте призы! В этом боте отличные акции и конкурсы:\n\n",
    },

    # ──────────── MENING DO'STLARIM ────────────
    "my_friends_title": {
        "uz": "👥 <b>Sizning do'stlaringiz</b>\n\n✅ Jami taklif qilingan: <b>{total}</b> ta\n✅ Faol (tasdiqlangan): <b>{verified}</b> ta\n\n📋 <b>So'nggi taklif qilinganlar:</b>\n{list}",
        "ru": "👥 <b>Ваши друзья</b>\n\n✅ Всего приглашено: <b>{total}</b>\n✅ Активных (подтверждено): <b>{verified}</b>\n\n📋 <b>Последние приглашённые:</b>\n{list}",
    },
    "no_friends_yet": {
        "uz": "Hali do'stlar yo'q. Havolangizni ulashing!",
        "ru": "Пока нет друзей. Поделитесь ссылкой!",
    },

    # ──────────── TOP REYTING ────────────
    "top_title": {
        "uz": "📊 <b>TOP-10 reyting</b>\n\nKonkursni tanlang:",
        "ru": "📊 <b>ТОП-10 рейтинг</b>\n\nВыберите конкурс:",
    },
    "top_contest_results": {
        "uz": "🏆 <b>{title}</b>\n\n{rows}\n\n⏰ Tugaydi: {end_date}",
        "ru": "🏆 <b>{title}</b>\n\n{rows}\n\n⏰ Заканчивается: {end_date}",
    },
    "no_participants": {
        "uz": "Hali ishtirokchilar yo'q. Birinchi bo'ling!",
        "ru": "Пока нет участников. Будьте первым!",
    },

    # ──────────── SOZLAMALAR ────────────
    "settings_title": {"uz": "⚙️ <b>Sozlamalar</b>", "ru": "⚙️ <b>Настройки</b>"},
    "btn_change_lang": {"uz": "🌐 Tilni o'zgartirish", "ru": "🌐 Сменить язык"},
    "btn_notifications": {"uz": "🔔 Bildirishnomalar", "ru": "🔔 Уведомления"},
    "btn_help": {"uz": "📞 Yordam", "ru": "📞 Помощь"},
    "notifications_on": {"uz": "🔔 Bildirishnomalar yoqildi", "ru": "🔔 Уведомления включены"},
    "notifications_off": {"uz": "🔕 Bildirishnomalar o'chirildi", "ru": "🔕 Уведомления отключены"},

    # ──────────── MA'LUMOT ────────────
    "info_text": {
        "uz": (
            "ℹ️ <b>Bot haqida ma'lumot</b>\n\n"
            "Bu bot orqali siz:\n"
            "🎁 Eng so'nggi <b>aksiyalar</b>dan xabardor bo'lasiz\n"
            "🏆 <b>Konkurslar</b>da ishtirok etib sovg'alar yutib olasiz\n"
            "👥 Do'stlaringizni taklif qilib ko'proq imkoniyatlar olasiz\n\n"
            "<b>Qanday ishlaydi?</b>\n"
            "1️⃣ Konkursga qo'shiling\n"
            "2️⃣ Shaxsiy havolangizni do'stlaringizga yuboring\n"
            "3️⃣ Ko'p taklif qiling — sovg'a yuting!"
        ),
        "ru": (
            "ℹ️ <b>О боте</b>\n\n"
            "Через этот бот вы:\n"
            "🎁 Узнаёте о новых <b>акциях</b>\n"
            "🏆 Участвуете в <b>конкурсах</b> и выигрываете призы\n"
            "👥 Приглашаете друзей и получаете больше возможностей\n\n"
            "<b>Как это работает?</b>\n"
            "1️⃣ Присоединяйтесь к конкурсу\n"
            "2️⃣ Отправьте свою ссылку друзьям\n"
            "3️⃣ Приглашайте больше — выигрывайте призы!"
        ),
    },
    "help_text": {
        "uz": "📞 Yordam kerakmi? Admin bilan bog'laning: @admin",
        "ru": "📞 Нужна помощь? Свяжитесь с админом: @admin",
    },

    # ──────────── REFERRAL NOTIFICATION ────────────
    "new_referral_notification": {
        "uz": "🎉 <b>Yangi do'stingiz qo'shildi!</b>\n\n👤 {name}\n📊 Sizdagi jami: <b>{count}</b> ta\n\nDavom eting va sovg'a yutib oling! 🎁",
        "ru": "🎉 <b>Новый друг добавлен!</b>\n\n👤 {name}\n📊 Всего у вас: <b>{count}</b>\n\nПродолжайте и выиграйте приз! 🎁",
    },

    # ──────────── ADMIN PANEL ────────────
    "admin_welcome": {"uz": "👑 <b>Admin panel</b>", "ru": "👑 <b>Админ-панель</b>"},
    "admin_only": {"uz": "⛔ Sizda admin huquqlari yo'q", "ru": "⛔ У вас нет прав администратора"},
    "admin_btn_ads": {"uz": "📢 Reklamalar", "ru": "📢 Реклама"},
    "admin_btn_contests": {"uz": "🏆 Konkurslar", "ru": "🏆 Конкурсы"},
    "admin_btn_channels": {"uz": "📡 Kanallar", "ru": "📡 Каналы"},
    "admin_btn_stats": {"uz": "📊 Statistika", "ru": "📊 Статистика"},
    "admin_btn_broadcast": {"uz": "📨 Ommaviy xabar", "ru": "📨 Рассылка"},
    "admin_btn_users": {"uz": "👥 Foydalanuvchilar", "ru": "👥 Пользователи"},
    "admin_back": {"uz": "⬅️ Admin menyuga", "ru": "⬅️ В админ-меню"},

    # ─── Admin: Reklamalar ───
    "admin_ads_menu": {
        "uz": "📢 <b>Reklamalar boshqaruvi</b>\n\nNima qilmoqchisiz?",
        "ru": "📢 <b>Управление рекламой</b>\n\nЧто хотите сделать?",
    },
    "admin_btn_new_ad": {"uz": "➕ Yangi reklama", "ru": "➕ Новая реклама"},
    "admin_btn_ads_list": {"uz": "📋 Reklamalar ro'yxati", "ru": "📋 Список реклам"},
    "ad_step_photo": {
        "uz": "📷 <b>1/6.</b> Reklama rasmini yuboring:\n\n(Yoki <b>⏭ O'tkazib yuborish</b>ni bosing — rasmsiz reklama)",
        "ru": "📷 <b>1/6.</b> Отправьте фото рекламы:\n\n(Или нажмите <b>⏭ Пропустить</b> — без фото)",
    },
    "ad_step_title": {
        "uz": "📝 <b>2/6.</b> Reklama nomini kiriting:\n\nMasalan: <i>🔥 Samsung A54 — 50% chegirma!</i>",
        "ru": "📝 <b>2/6.</b> Введите название рекламы:\n\nНапример: <i>🔥 Samsung A54 — скидка 50%!</i>",
    },
    "ad_step_description": {
        "uz": "📄 <b>3/6.</b> Reklama tavsifini kiriting:\n\n(HTML formatlash mumkin: &lt;b&gt;qalin&lt;/b&gt;, &lt;i&gt;qiyshiq&lt;/i&gt;)",
        "ru": "📄 <b>3/6.</b> Введите описание:\n\n(Можно HTML: &lt;b&gt;жирный&lt;/b&gt;, &lt;i&gt;курсив&lt;/i&gt;)",
    },
    "ad_step_promo": {
        "uz": "🔥 <b>4/6.</b> Aksiya matnini kiriting (ixtiyoriy):\n\nMasalan: <i>Faqat shu hafta!</i>\n\nKerak emas bo'lsa — <b>⏭ O'tkazib yuborish</b>",
        "ru": "🔥 <b>4/6.</b> Введите текст акции (необязательно):\n\nНапример: <i>Только на этой неделе!</i>\n\nЕсли не нужно — <b>⏭ Пропустить</b>",
    },
    "ad_step_link_type": {
        "uz": "🔗 <b>5/6.</b> Link turini tanlang:",
        "ru": "🔗 <b>5/6.</b> Выберите тип ссылки:",
    },
    "ad_link_web": {"uz": "🌐 Veb-sayt", "ru": "🌐 Веб-сайт"},
    "ad_link_telegram": {"uz": "📱 Telegram", "ru": "📱 Telegram"},
    "ad_link_mobile": {"uz": "📲 Mobil app", "ru": "📲 Мобильное приложение"},
    "ad_step_link_url": {
        "uz": "🔗 <b>5/6.</b> Link manzilini kiriting:\n\nMisol: https://uzum.uz/product/123",
        "ru": "🔗 <b>5/6.</b> Введите URL:\n\nПример: https://uzum.uz/product/123",
    },
    "ad_step_button": {
        "uz": "🔘 <b>6/6.</b> Tugma yozuvini kiriting:\n\nDefault: <i>🛒 Olish</i>\n\nO'zgartirmoqchi bo'lmasangiz — <b>⏭ O'tkazib yuborish</b>",
        "ru": "🔘 <b>6/6.</b> Введите текст кнопки:\n\nПо умолчанию: <i>🛒 Получить</i>\n\nЕсли оставить как есть — <b>⏭ Пропустить</b>",
    },
    "ad_preview": {
        "uz": "👀 <b>Ko'rib chiqing:</b>\n\nReklama tayyor. Saqlashni xohlaysizmi?",
        "ru": "👀 <b>Предпросмотр:</b>\n\nРеклама готова. Сохранить?",
    },
    "ad_saved": {"uz": "✅ Reklama saqlandi!", "ru": "✅ Реклама сохранена!"},
    "ad_send_now": {"uz": "📤 Hozir kanalga jo'natish", "ru": "📤 Отправить в канал"},
    "ads_list_empty": {"uz": "📭 Reklamalar yo'q", "ru": "📭 Реклам нет"},
    "ad_deleted": {"uz": "✅ Reklama o'chirildi", "ru": "✅ Реклама удалена"},
    "ad_btn_delete": {"uz": "❌ O'chirish", "ru": "❌ Удалить"},
    "ad_btn_send_channel": {"uz": "📤 Kanalga jo'natish", "ru": "📤 Отправить в канал"},
    "ad_select_channel": {"uz": "📡 Qaysi kanalga jo'natamiz?", "ru": "📡 В какой канал отправить?"},
    "ad_sent_to_channel": {"uz": "✅ Kanalga jo'natildi!", "ru": "✅ Отправлено в канал!"},

    # ─── Admin: Konkurslar ───
    "admin_contests_menu": {
        "uz": "🏆 <b>Konkurslar boshqaruvi</b>",
        "ru": "🏆 <b>Управление конкурсами</b>",
    },
    "admin_btn_new_contest": {"uz": "➕ Yangi konkurs", "ru": "➕ Новый конкурс"},
    "admin_btn_contests_list": {"uz": "📋 Konkurslar ro'yxati", "ru": "📋 Список конкурсов"},
    "contest_step_title": {
        "uz": "🏆 <b>1/6.</b> Konkurs nomini kiriting:\n\nMisol: <i>iPhone 15 yutib ol!</i>",
        "ru": "🏆 <b>1/6.</b> Введите название конкурса:\n\nПример: <i>Выиграй iPhone 15!</i>",
    },
    "contest_step_description": {
        "uz": "📄 <b>2/6.</b> Konkurs tavsifini kiriting:",
        "ru": "📄 <b>2/6.</b> Введите описание конкурса:",
    },
    "contest_step_photo": {
        "uz": "📷 <b>3/6.</b> Sovg'a rasmini yuboring (yoki ⏭ o'tkazib yuborish):",
        "ru": "📷 <b>3/6.</b> Отправьте фото приза (или ⏭ пропустить):",
    },
    "contest_step_type": {
        "uz": "🎯 <b>4/6.</b> Konkurs turini tanlang:",
        "ru": "🎯 <b>4/6.</b> Выберите тип конкурса:",
    },
    "contest_type_top3": {"uz": "🥇 TOP-3 g'olib", "ru": "🥇 ТОП-3 победителя"},
    "contest_type_first_n": {"uz": "⚡ Birinchi N ta", "ru": "⚡ Первые N человек"},
    "contest_step_prizes": {
        "uz": "🎁 <b>5/6.</b> Sovg'alar ro'yxatini kiriting (har biri yangi qatordan):\n\nMisol:\n<code>1-o'rin: iPhone 15\n2-o'rin: AirPods Pro\n3-o'rin: 500 000 so'm</code>",
        "ru": "🎁 <b>5/6.</b> Введите список призов (каждый с новой строки):\n\nПример:\n<code>1 место: iPhone 15\n2 место: AirPods Pro\n3 место: 500 000 сум</code>",
    },
    "contest_step_required_refs": {
        "uz": "🔢 Nechta obunachi kerak (g'olib bo'lish uchun)?\n\nMisol: <code>10</code>",
        "ru": "🔢 Сколько подписчиков нужно (для победы)?\n\nПример: <code>10</code>",
    },
    "contest_step_end_date": {
        "uz": "📅 <b>6/6.</b> Konkurs tugash sanasini kiriting (DD.MM.YYYY):\n\nMisol: <code>30.06.2026</code>",
        "ru": "📅 <b>6/6.</b> Введите дату окончания (DD.MM.YYYY):\n\nПример: <code>30.06.2026</code>",
    },
    "contest_saved": {"uz": "✅ Konkurs yaratildi!", "ru": "✅ Конкурс создан!"},
    "contest_btn_end": {"uz": "🏁 Yakunlash", "ru": "🏁 Завершить"},
    "contest_btn_winners": {"uz": "🏆 G'oliblarni e'lon qilish", "ru": "🏆 Объявить победителей"},
    "contest_ended": {"uz": "✅ Konkurs yakunlandi", "ru": "✅ Конкурс завершён"},
    "winners_announced": {
        "uz": "🎉 <b>KONKURS YAKUNLANDI!</b>\n\n<b>{title}</b>\n\n🏆 <b>G'oliblar:</b>\n{winners}\n\nTabriklaymiz! 🎊",
        "ru": "🎉 <b>КОНКУРС ЗАВЕРШЁН!</b>\n\n<b>{title}</b>\n\n🏆 <b>Победители:</b>\n{winners}\n\nПоздравляем! 🎊",
    },

    # ─── Admin: Kanallar ───
    "admin_channels_menu": {
        "uz": "📡 <b>Kanallar boshqaruvi</b>",
        "ru": "📡 <b>Управление каналами</b>",
    },
    "admin_btn_add_channel": {"uz": "➕ Kanal qo'shish", "ru": "➕ Добавить канал"},
    "admin_btn_channels_list": {"uz": "📋 Kanallar ro'yxati", "ru": "📋 Список каналов"},
    "channel_add_instruction": {
        "uz": (
            "📡 <b>Kanal qo'shish</b>\n\n"
            "1️⃣ Botni kanalingizga admin qilib qo'shing\n"
            "2️⃣ Kanaldan xabarni botga forward qiling YOKI kanal username'ini yuboring (@kanalim)\n\n"
            "Bekor qilish — <b>❌ Bekor qilish</b>"
        ),
        "ru": (
            "📡 <b>Добавление канала</b>\n\n"
            "1️⃣ Добавьте бота администратором в канал\n"
            "2️⃣ Перешлите боту сообщение из канала ИЛИ отправьте username (@kanalim)\n\n"
            "Для отмены — <b>❌ Отменить</b>"
        ),
    },
    "channel_mandatory_q": {
        "uz": "Bu kanal majburiy obunami? (User botdan foydalanish uchun obuna bo'lishi shartmi?)",
        "ru": "Этот канал обязателен для подписки?",
    },
    "channel_added": {"uz": "✅ Kanal qo'shildi: <b>{title}</b>", "ru": "✅ Канал добавлен: <b>{title}</b>"},
    "channel_error": {
        "uz": "❌ Kanal qo'shilmadi. Bot kanalda admin emas yoki kanal username noto'g'ri.",
        "ru": "❌ Канал не добавлен. Бот не админ в канале или неверный username.",
    },
    "channels_list_empty": {"uz": "📭 Kanallar yo'q", "ru": "📭 Каналов нет"},
    "channel_removed": {"uz": "✅ Kanal o'chirildi", "ru": "✅ Канал удалён"},
    "channel_btn_remove": {"uz": "❌ Uzish", "ru": "❌ Отключить"},
    "channel_btn_toggle_mandatory": {"uz": "🔄 Majburiylik", "ru": "🔄 Обязательность"},

    # ─── Admin: Statistika ───
    "admin_stats_text": {
        "uz": (
            "📊 <b>Umumiy statistika</b>\n\n"
            "👥 Jami userlar: <b>{total_users}</b>\n"
            "✅ Faol userlar: <b>{active_users}</b>\n"
            "🔗 Tasdiqlangan referrallar: <b>{total_referrals}</b>\n"
            "📢 Reklamalar: <b>{total_ads}</b>\n"
            "🏆 Konkurslar (jami): <b>{total_contests}</b>\n"
            "▶️ Faol konkurslar: <b>{active_contests}</b>"
        ),
        "ru": (
            "📊 <b>Общая статистика</b>\n\n"
            "👥 Всего пользователей: <b>{total_users}</b>\n"
            "✅ Активных: <b>{active_users}</b>\n"
            "🔗 Подтверждённых рефералов: <b>{total_referrals}</b>\n"
            "📢 Реклам: <b>{total_ads}</b>\n"
            "🏆 Конкурсов (всего): <b>{total_contests}</b>\n"
            "▶️ Активных конкурсов: <b>{active_contests}</b>"
        ),
    },

    # ─── Admin: Broadcast ───
    "broadcast_instruction": {
        "uz": "📨 <b>Ommaviy xabar</b>\n\nUserlarga yubormoqchi bo'lgan xabarni yuboring (matn, rasm, video — har qanday):",
        "ru": "📨 <b>Рассылка</b>\n\nОтправьте сообщение для рассылки (текст, фото, видео — любое):",
    },
    "broadcast_confirm": {
        "uz": "📊 Quyidagi xabar <b>{count}</b> ta foydalanuvchiga jo'natiladi. Davom etamizmi?",
        "ru": "📊 Сообщение будет отправлено <b>{count}</b> пользователям. Продолжить?",
    },
    "broadcast_started": {
        "uz": "📤 Yuborilmoqda...\n\nTayyor bo'lganda xabar beraman.",
        "ru": "📤 Идёт отправка...\n\nСообщу когда закончится.",
    },
    "broadcast_finished": {
        "uz": "✅ <b>Yuborish yakunlandi</b>\n\n✓ Muvaffaqiyatli: {success}\n✗ Xato: {failed}",
        "ru": "✅ <b>Рассылка завершена</b>\n\n✓ Успешно: {success}\n✗ Ошибок: {failed}",
    },

    # ─── Admin: Userlar ───
    "users_menu": {
        "uz": "👥 <b>Foydalanuvchilarni boshqarish</b>\n\nUser ID yoki @username yuboring:",
        "ru": "👥 <b>Управление пользователями</b>\n\nОтправьте ID или @username:",
    },
    "user_info": {
        "uz": (
            "👤 <b>Foydalanuvchi haqida</b>\n\n"
            "ID: <code>{tg_id}</code>\n"
            "Ism: {name}\n"
            "Username: @{username}\n"
            "Til: {lang}\n"
            "Status: {status}\n"
            "Qo'shilgan: {joined}\n"
            "Takliflar: <b>{refs}</b> ta"
        ),
        "ru": (
            "👤 <b>О пользователе</b>\n\n"
            "ID: <code>{tg_id}</code>\n"
            "Имя: {name}\n"
            "Username: @{username}\n"
            "Язык: {lang}\n"
            "Статус: {status}\n"
            "Присоединился: {joined}\n"
            "Рефералов: <b>{refs}</b>"
        ),
    },
    "user_not_found": {"uz": "❌ Foydalanuvchi topilmadi", "ru": "❌ Пользователь не найден"},
    "user_btn_block": {"uz": "🚫 Bloklash", "ru": "🚫 Заблокировать"},
    "user_btn_unblock": {"uz": "✅ Blokdan chiqarish", "ru": "✅ Разблокировать"},
    "user_blocked": {"uz": "✅ User bloklandi", "ru": "✅ Пользователь заблокирован"},
    "user_unblocked": {"uz": "✅ User blokdan chiqarildi", "ru": "✅ Пользователь разблокирован"},
    "status_active": {"uz": "✅ Faol", "ru": "✅ Активен"},
    "status_blocked": {"uz": "🚫 Bloklangan", "ru": "🚫 Заблокирован"},
}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    """Tarjima olish"""
    text = TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get("uz", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
