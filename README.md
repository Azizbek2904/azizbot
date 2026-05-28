# 🤖 Konkurs & Reklama Boti

Telegram bot — kanallar uchun **referral konkurslar va aksiyalar tizimi**.
Uzum Market va boshqa do'konlar uchun mo'ljallangan.

---

## ✨ Imkoniyatlari

### 👤 Foydalanuvchi paneli
- 🌐 **Ikki tilli** — O'zbek va Rus
- 📢 **Majburiy obuna** — bir nechta kanallarga
- 🎁 **Aksiyalar** — rasm + matn + link (web/telegram/mobile)
- 🏆 **Konkurslar** — TOP-3 yoki "Birinchi N ta taklif"
- 🔗 **Shaxsiy referral havola** — har bir foydalanuvchiga
- 👥 **Mening do'stlarim** — taklif qilingan kishilar ro'yxati
- 📊 **TOP-10 reyting** — har bir konkurs uchun
- 🔔 **Avtomatik xabarnomalar** — yangi referral kelganda

### 👑 Admin paneli
- 📢 Reklama yaratish/o'chirish/kanalga yuborish
- 🏆 Konkurs yaratish va boshqarish, g'oliblarni e'lon qilish
- 📡 Kanallar boshqaruvi (qo'shish/uzish, majburiy/ixtiyoriy)
- 📊 Umumiy statistika
- 📨 Ommaviy xabar (broadcast)
- 👥 Foydalanuvchilarni izlash va bloklash

---

## 📋 O'rnatish (sozlash)

### 1. Python 3.10+ kerak

```bash
python --version
```

### 2. Loyihani yuklang va papkasiga kiring

```bash
cd bot
```

### 3. Virtual muhit yarating va aktivlashtiring

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Kerakli kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
```

### 5. `.env` faylini yarating

`.env.example` faylini `.env` ga nusxalang:

```bash
cp .env .env
```

So'ng `.env` faylini ochib quyidagilarni to'ldiring:

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMIN_IDS=123456789,987654321
DATABASE_URL=sqlite+aiosqlite:///bot_database.db
```

**Qanday olish kerak?**
- `BOT_TOKEN` — [@BotFather](https://t.me/BotFather) dan `/newbot`
- `ADMIN_IDS` — [@userinfobot](https://t.me/userinfobot) sizning Telegram ID'ingizni ko'rsatadi

### 6. Botni ishga tushiring

```bash
python main.py
```

Konsolda quyidagi ko'rinsa — tayyor:
```
🚀 Bot ishga tushmoqda...
✅ Database tayyor
✅ Bot @SizningBot (ID: 123456789) ishga tushdi!
👑 Adminlar: [123456789]
```

---

## 📱 Foydalanish

### Foydalanuvchi uchun
1. Botga `/start` yozadi
2. Til tanlaydi (Uz/Ru)
3. Majburiy kanallarga obuna bo'ladi
4. Asosiy menyudan kerakli bo'limni tanlaydi

### Admin uchun
1. Botga `/admin` yozadi
2. Admin panel ochiladi
3. **Birinchi navbatda kanal qo'shish kerak:**
   - "📡 Kanallar" → "➕ Kanal qo'shish"
   - Botni avval kanalga **admin qilib qo'shing**
   - Keyin kanaldan xabarni forward qiling YOKI `@kanalim` deb yozing
4. So'ng reklama / konkurs yaratish mumkin

---

## 🗂️ Loyiha tuzilishi

```
bot/
├── main.py                 # Asosiy ishga tushirish fayli
├── config.py               # .env dan sozlamalarni o'qish
├── database.py             # SQLAlchemy modellari va DB funksiyalari
├── locales.py              # Uz/Ru tarjimalar
├── keyboards.py            # Barcha klaviaturalar
├── utils.py                # Yordamchi funksiyalar (obuna tekshiruvi va h.k.)
├── states.py               # FSM states (ko'p qadamli formalar)
├── handlers/
│   ├── __init__.py         # Routerlarni birlashtirish
│   ├── user.py             # User tomonidagi handlerlar
│   └── admin.py            # Admin tomonidagi handlerlar
├── requirements.txt        # Dependencies
├── .env.example            # Misol uchun .env
└── README.md               # Shu fayl
```

---

## 🛠️ Texnologiyalar

- **Python 3.10+**
- **aiogram 3.13** — Telegram Bot Framework
- **SQLAlchemy 2.0** — ORM (async)
- **SQLite** (default) — yoki PostgreSQL
- **APScheduler** — vaqt bo'yicha vazifalar uchun

---

## 🚀 Production'ga deploy

### VPS (Ubuntu)

1. VPS oling (DigitalOcean, Hetzner, AWS va h.k.)
2. SSH orqali ulaning
3. Python o'rnating:
   ```bash
   sudo apt update && sudo apt install python3-pip python3-venv -y
   ```
4. Loyihani yuklang (git clone yoki rsync orqali)
5. Yuqoridagi o'rnatish bosqichlarini bajaring
6. **systemd service** yarating — bot doim ishlab tursin:

`/etc/systemd/system/telegram-bot.service`:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot
ExecStart=/root/bot/venv/bin/python /root/bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

So'ng:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

---

## 📞 Yordam

Kod bilan bog'liq savol bo'lsa — savolingizni yozing va Claude'dan yordam so'rang.

**Muvaffaqiyat tilaymiz!** 🚀
