"""
BTX Texture Converter Bot — main.py
Telegram-бот для конвертации изображений в .btx и обратно.

Переменные окружения (.env или системные):
  BOT_TOKEN   — токен бота (обязательно)
  LOG_CHAT_ID — chat_id куда пересылать ВСЕ входящие сообщения (опционально)
                Может быть числом (личка/канал) или username (@mychan)
"""

import os
import sys
import logging
import tempfile
import html
from pathlib import Path
from datetime import datetime, timezone

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode, MessageOriginType
from telegram.error import TelegramError

from btx_converter import image_to_btx, btx_to_image, check_dependencies, btx_info, _BACKEND

# ─────────────────────────────────────────────────────────────────────────────
# Логирование в файл + stdout
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("btx_bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("btx_bot")

# ─────────────────────────────────────────────────────────────────────────────
# Конфигурация
# ─────────────────────────────────────────────────────────────────────────────

SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".tga"}

COMPRESS_OPTIONS = {
    "4x4": "Лучшее качество, больший файл",
    "6x6": "Баланс",
    "8x8": "Меньший файл, ниже качество",
}
QUALITY_OPTIONS = {
    "fast":       "Быстро, ниже качество",
    "medium":     "Баланс (рекомендуется)",
    "thorough":   "Высокое качество, медленнее",
    "exhaustive": "Максимум качества, очень медленно",
}

user_settings: dict[int, dict] = {}
LOG_CHAT_ID: str | int | None = None


def get_settings(uid: int) -> dict:
    if uid not in user_settings:
        user_settings[uid] = {"compress": "4x4", "quality": "medium"}
    return user_settings[uid]


# ─────────────────────────────────────────────────────────────────────────────
# Система логирования — пересылка ВСЕГО в LOG_CHAT_ID
# ─────────────────────────────────────────────────────────────────────────────

def _user_tag(user) -> str:
    """Формирует красивую подпись пользователя."""
    if user is None:
        return "Unknown"
    parts = [f"<b>{html.escape(user.full_name)}</b>"]
    if user.username:
        parts.append(f"@{user.username}")
    parts.append(f"[<code>{user.id}</code>]")
    return " ".join(parts)


def _chat_tag(chat) -> str:
    """Формирует подпись чата."""
    if chat is None:
        return "?"
    name = chat.title or chat.username or chat.full_name or "—"
    return f"{html.escape(name)} [<code>{chat.id}</code>]"


def _msg_type_and_content(msg: Message) -> tuple[str, str]:
    """
    Определяет тип и текстовое описание содержимого сообщения.
    Возвращает (тип_эмодзи_и_название, описание_или_caption).
    """
    caption = html.escape(msg.caption or "")

    if msg.text:
        return "💬 Текст", f"<code>{html.escape(msg.text)}</code>"

    if msg.sticker:
        s = msg.sticker
        emoji = s.emoji or ""
        name  = html.escape(s.set_name or "без набора")
        kind  = "Анимированный" if s.is_animated else ("Видео" if s.is_video else "Обычный")
        return "🎭 Стикер", f"{kind} стикер {emoji} из набора <b>{name}</b>"

    if msg.animation:
        a = msg.animation
        desc = f"GIF/Анимация  {a.width}×{a.height}  {a.duration}с"
        if caption:
            desc += f"\n<i>Подпись:</i> {caption}"
        return "🎞 GIF", desc

    if msg.photo:
        p = msg.photo[-1]  # берём наибольшее разрешение
        desc = f"Фото  {p.width}×{p.height}  ({p.file_size or 0} б)"
        if caption:
            desc += f"\n<i>Подпись:</i> {caption}"
        return "🖼 Фото", desc

    if msg.video:
        v = msg.video
        desc = f"Видео  {v.width}×{v.height}  {v.duration}с  {html.escape(v.mime_type or '')}"
        if caption:
            desc += f"\n<i>Подпись:</i> {caption}"
        return "🎬 Видео", desc

    if msg.video_note:
        vn = msg.video_note
        return "⭕ Видеосообщение", f"Кружок  {vn.duration}с  {vn.length}px"

    if msg.voice:
        v = msg.voice
        return "🎤 Голосовое", f"Голосовое  {v.duration}с"

    if msg.audio:
        a = msg.audio
        title = html.escape(a.title or "")
        artist = html.escape(a.performer or "")
        desc = f"Аудио  {a.duration}с"
        if title or artist:
            desc += f"  <b>{artist} — {title}</b>"
        if caption:
            desc += f"\n<i>Подпись:</i> {caption}"
        return "🎵 Аудио", desc

    if msg.document:
        d = msg.document
        name = html.escape(d.file_name or "файл")
        size = f"{d.file_size or 0} б" if d.file_size else ""
        desc = f"Документ  <code>{name}</code>  {size}"
        if caption:
            desc += f"\n<i>Подпись:</i> {caption}"
        return "📎 Документ", desc

    if msg.poll:
        p = msg.poll
        q = html.escape(p.question)
        opts = "  |  ".join(html.escape(o.text) for o in p.options)
        kind = "Викторина" if p.type == "quiz" else "Опрос"
        return f"📊 {kind}", f"<b>{q}</b>\n{opts}"

    if msg.dice:
        emoji_map = {"🎲": "кубик", "🎯": "дартс", "🏀": "баскетбол",
                     "⚽": "футбол", "🎳": "боулинг", "🎰": "слоты"}
        name = emoji_map.get(msg.dice.emoji, msg.dice.emoji)
        return f"🎲 Игра", f"{msg.dice.emoji} {name}  выпало: <b>{msg.dice.value}</b>"

    if msg.location:
        loc = msg.location
        return "📍 Геолокация", f"lat={loc.latitude}  lon={loc.longitude}"

    if msg.venue:
        v = msg.venue
        return "🏛 Место", (
            f"<b>{html.escape(v.title)}</b>\n"
            f"{html.escape(v.address)}\n"
            f"lat={v.location.latitude}  lon={v.location.longitude}"
        )

    if msg.contact:
        c = msg.contact
        name = html.escape(f"{c.first_name} {c.last_name or ''}".strip())
        phone = html.escape(c.phone_number)
        return "👤 Контакт", f"<b>{name}</b>  {phone}"

    if msg.game:
        return "🕹 Игра", html.escape(msg.game.title)

    if msg.invoice:
        i = msg.invoice
        return "🧾 Счёт", f"<b>{html.escape(i.title)}</b>  {i.total_amount/100:.2f} {i.currency}"

    if msg.successful_payment:
        sp = msg.successful_payment
        return "✅ Платёж", f"{sp.total_amount/100:.2f} {sp.currency}"

    if msg.new_chat_members:
        names = ", ".join(html.escape(u.full_name) for u in msg.new_chat_members)
        return "➕ Вошли", names

    if msg.left_chat_member:
        return "➖ Вышел", html.escape(msg.left_chat_member.full_name)

    if msg.new_chat_title:
        return "✏️ Новый заголовок", html.escape(msg.new_chat_title)

    if msg.pinned_message:
        return "📌 Закреплено", "(сообщение)"

    if msg.story:
        return "📖 История", "Пользователь поделился историей"

    if msg.forum_topic_created:
        return "📂 Тема", html.escape(msg.forum_topic_created.name)

    if getattr(msg, "giveaway", None):
        return "🎁 Розыгрыш", "(giveaway)"

    if getattr(msg, "boost_added", None):
        return "⚡ Буст", f"добавлено бустов: {msg.boost_added.boost_count}"

    # Неизвестный тип — просто сообщаем что пришло что-то
    return "❓ Неизвестный тип", str(msg)


async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Универсальный обработчик-логгер.
    Запускается для ЛЮБОГО входящего сообщения ПЕРЕД другими хендлерами.
    Пересылает сообщение (если возможно) и/или отправляет аннотацию в LOG_CHAT_ID.
    """
    if not LOG_CHAT_ID:
        return

    msg = update.effective_message
    if not msg:
        return

    user = update.effective_user
    chat = update.effective_chat

    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    msg_type, content = _msg_type_and_content(msg)

    # Заголовок аннотации
    header = (
        f"<b>{msg_type}</b>\n"
        f"👤 {_user_tag(user)}\n"
        f"💬 Чат: {_chat_tag(chat)}\n"
        f"🕐 {now}\n"
        f"🆔 msg_id: <code>{msg.message_id}</code>"
    )

    # Содержимое
    annotation = f"{header}\n\n{content}" if content else header

    try:
        # Пробуем переслать оригинальное сообщение
        forwarded = False
        try:
            await context.bot.forward_message(
                chat_id=LOG_CHAT_ID,
                from_chat_id=chat.id,
                message_id=msg.message_id,
            )
            forwarded = True
        except TelegramError as fe:
            logger.debug(f"Не удалось переслать сообщение: {fe}")

        # Всегда отправляем аннотацию
        # Если переслали — аннотация уточняет метаданные
        # Если нет (защищённый чат и т.д.) — аннотация это всё что есть
        prefix = "" if forwarded else "⚠️ <i>Пересылка заблокирована</i>\n\n"
        await context.bot.send_message(
            chat_id=LOG_CHAT_ID,
            text=prefix + annotation,
            parse_mode=ParseMode.HTML,
        )

    except TelegramError as e:
        logger.error(f"Ошибка логирования сообщения: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Команды бота
# ─────────────────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    backend_note = f"\n⚙️ Бэкенд: <code>{_BACKEND}</code>" if _BACKEND != "none" else ""
    await update.message.reply_text(
        "👋 <b>BTX Texture Converter</b>\n\n"
        "Отправь мне файл:\n"
        "• <b>PNG / JPG / BMP / WEBP / TIFF / TGA</b> → получишь <code>.btx</code>\n"
        "• <b>.btx</b> → получишь PNG\n\n"
        "<b>Команды:</b>\n"
        "/settings — текущие настройки\n"
        "/setmode — размер ASTC блока\n"
        "/setquality — качество кодирования"
        + backend_note,
        parse_mode=ParseMode.HTML,
    )


async def cmd_settings(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    s = get_settings(update.effective_user.id)
    await update.message.reply_text(
        f"⚙️ <b>Настройки</b>\n\n"
        f"Блок ASTC: <code>{s['compress']}</code>  —  {COMPRESS_OPTIONS[s['compress']]}\n"
        f"Качество: <code>{s['quality']}</code>  —  {QUALITY_OPTIONS[s['quality']]}\n"
        f"Бэкенд: <code>{_BACKEND}</code>",
        parse_mode=ParseMode.HTML,
    )


async def cmd_setmode(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(f"{m} — {desc}", callback_data=f"mode:{m}")]
        for m, desc in COMPRESS_OPTIONS.items()
    ]
    await update.message.reply_text(
        "Выбери размер ASTC блока:\n"
        "<i>4×4 — максимальное качество, но самый большой файл.\n"
        "8×8 — минимальный размер, но ниже чёткость.</i>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML,
    )


async def cmd_setquality(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(f"{q} — {desc}", callback_data=f"quality:{q}")]
        for q, desc in QUALITY_OPTIONS.items()
    ]
    await update.message.reply_text(
        "Выбери качество кодирования ASTC:\n"
        "<i>medium достаточно для большинства текстур.</i>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML,
    )


async def cmd_info(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Информация о BTX файле (без декодирования)."""
    msg = update.message
    if not msg.document or not msg.document.file_name.endswith(".btx"):
        await msg.reply_text("Отправь .btx файл с командой /info в подписи.")
        return
    with tempfile.TemporaryDirectory(prefix="btxbot_") as tmp:
        p = Path(tmp) / msg.document.file_name
        f = await msg.document.get_file()
        await f.download_to_drive(str(p))
        try:
            info = btx_info(str(p))
            await msg.reply_text(
                f"📦 <b>BTX Info</b>\n"
                f"Размер: {info['width']}×{info['height']}\n"
                f"ASTC блок: {info['block_w']}×{info['block_h']}\n"
                f"Mip уровней: {info['mip_levels']}\n"
                f"Файл: {info['file_size']} байт",
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            await msg.reply_text(f"❌ {e}")


async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    s = get_settings(query.from_user.id)
    key, value = query.data.split(":", 1)
    if key == "mode":
        s["compress"] = value
        await query.edit_message_text(
            f"✅ ASTC блок установлен: <b>{value}</b>\n"
            f"<i>{COMPRESS_OPTIONS[value]}</i>",
            parse_mode=ParseMode.HTML,
        )
    elif key == "quality":
        s["quality"] = value
        await query.edit_message_text(
            f"✅ Качество установлено: <b>{value}</b>\n"
            f"<i>{QUALITY_OPTIONS[value]}</i>",
            parse_mode=ParseMode.HTML,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Обработчик файлов (конвертация)
# ─────────────────────────────────────────────────────────────────────────────

async def handle_file(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message

    # Если пришло фото (сжатое Telegram'ом) — объясняем
    if msg.photo:
        await msg.reply_text(
            "📎 Отправь файл через <b>Файл / Документ</b> (не как фото) — "
            "иначе Telegram сжимает изображение и теряет расширение.",
            parse_mode=ParseMode.HTML,
        )
        return

    doc = msg.document
    if not doc:
        return

    filename = doc.file_name or "file"
    ext = Path(filename).suffix.lower()
    s = get_settings(update.effective_user.id)

    with tempfile.TemporaryDirectory(prefix="btxbot_") as tmp:
        tmp = Path(tmp)
        input_path = tmp / filename

        status = await msg.reply_text("⬇️ Загружаю…")
        tg_file = await doc.get_file()
        await tg_file.download_to_drive(str(input_path))

        try:
            if ext == ".btx":
                await status.edit_text("🔄 BTX → PNG…")
                out_path = str(tmp / (Path(filename).stem + ".png"))
                btx_to_image(str(input_path), out_path)

                # Инфо о файле
                info = btx_info(str(input_path))
                await msg.reply_document(
                    document=open(out_path, "rb"),
                    filename=Path(out_path).name,
                    caption=(
                        f"✅ <code>{filename}</code> → PNG\n"
                        f"Размер: {info['width']}×{info['height']}  "
                        f"ASTC: {info['block_w']}×{info['block_h']}  "
                        f"Mips: {info['mip_levels']}"
                    ),
                    parse_mode=ParseMode.HTML,
                )

            elif ext in SUPPORTED_IMAGE_EXTS:
                out_name = Path(filename).stem + ".btx"
                out_path = str(tmp / out_name)
                await status.edit_text(
                    f"🔄 Конвертирую в BTX…\n"
                    f"Блок: <code>{s['compress']}</code>  "
                    f"Качество: <code>{s['quality']}</code>",
                    parse_mode=ParseMode.HTML,
                )
                image_to_btx(str(input_path), out_path, s["compress"], s["quality"])

                size_kb = Path(out_path).stat().st_size / 1024
                await msg.reply_document(
                    document=open(out_path, "rb"),
                    filename=out_name,
                    caption=(
                        f"✅ <code>{filename}</code> → <code>{out_name}</code>\n"
                        f"Блок: {s['compress']}  Качество: {s['quality']}  "
                        f"Размер: {size_kb:.1f} KB"
                    ),
                    parse_mode=ParseMode.HTML,
                )

            else:
                await status.edit_text(
                    f"❌ Неподдерживаемый формат: <code>{ext}</code>\n\n"
                    f"Поддерживаются: {', '.join(sorted(SUPPORTED_IMAGE_EXTS))} "
                    f"и <code>.btx</code>",
                    parse_mode=ParseMode.HTML,
                )
                return

        except Exception as e:
            logger.exception("Ошибка конвертации")
            await status.edit_text(
                f"❌ Ошибка конвертации:\n<code>{html.escape(str(e))}</code>",
                parse_mode=ParseMode.HTML,
            )
            return

        await status.delete()


# ─────────────────────────────────────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────────────────────────────────────

def _load_env() -> None:
    """Загрузить .env файл если есть."""
    env = Path(__file__).parent / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        val = val.strip().strip("\"'")
        os.environ.setdefault(key.strip(), val)


def main() -> None:
    global LOG_CHAT_ID

    _load_env()

    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token:
        sys.exit("Укажи BOT_TOKEN в переменной окружения или в файле .env")

    # Лог-чат (опционально)
    log_chat_raw = os.environ.get("LOG_CHAT_ID", "").strip()
    if log_chat_raw:
        try:
            LOG_CHAT_ID = int(log_chat_raw)
        except ValueError:
            LOG_CHAT_ID = log_chat_raw   # username типа @mychan
        logger.info(f"Логирование сообщений в: {LOG_CHAT_ID}")
    else:
        logger.info("LOG_CHAT_ID не задан — логирование сообщений отключено")

    # Проверка зависимостей
    try:
        check_dependencies()
        logger.info(f"ASTC бэкенд: {_BACKEND} — OK")
    except Exception as e:
        sys.exit(f"Зависимости не установлены: {e}")

    app = Application.builder().token(token).build()

    # ── Логирование: группа -1 (выполняется ПЕРВОЙ, до всех остальных хендлеров) ──
    app.add_handler(
        MessageHandler(filters.ALL, log_message),
        group=-1,
    )

    # ── Команды ──
    app.add_handler(CommandHandler("start",      cmd_start))
    app.add_handler(CommandHandler("settings",   cmd_settings))
    app.add_handler(CommandHandler("setmode",    cmd_setmode))
    app.add_handler(CommandHandler("setquality", cmd_setquality))
    app.add_handler(CommandHandler("info",       cmd_info))

    # ── Inline кнопки ──
    app.add_handler(CallbackQueryHandler(on_callback))

    # ── Файлы и фото ──
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))

    logger.info("Бот запущен ✓")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
