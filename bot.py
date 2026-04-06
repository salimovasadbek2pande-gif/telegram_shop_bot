"""
╔══════════════════════════════════════════════════════════╗
║         🛒 TELEGRAM SHOP ORDER BOT                      ║
║         Built with aiogram 3.x + FSM                    ║
║         Ready-to-sell demo bot                          ║
╚══════════════════════════════════════════════════════════╝

Author  : Your Name
Version : 1.0.0
Stack   : Python 3.10+, aiogram 3.x, FSM
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# ──────────────────────────────────────────────
#  ⚙️  CONFIGURATION  (edit these values)
# ──────────────────────────────────────────────

BOT_TOKEN = "8733419389:AAF9y3jrrCLUQt4NYXJ95m0mL9IYlUOoJwY"   # 👈 Paste your BotFather token here
ADMIN_ID  = 6986558107               # 👈 Paste your Telegram numeric user-id here
ADMIN_USERNAME = "@Zephroth"    # 👈 Your Telegram @username for Contact section

# ──────────────────────────────────────────────
#  📦  PRODUCT CATALOG
#  To add/remove products — just edit this dict.
# ──────────────────────────────────────────────

PRODUCTS: dict[str, dict] = {
    "naushnik": {
        "name": "🎧 Naushnik",
        "price": "150 000 so'm",
        "description": (
            "🎧 <b>Naushnik</b>\n\n"
            "💰 Narxi: <b>150 000 so'm</b>\n\n"
            "📝 <i>Yuqori sifatli stereo naushnik. "
            "Bass kuchaytirilgan, quloqqa qulay o'tiradigan dizayn. "
            "Har qanday qurilma bilan ishlaydi. "
            "3.5mm jack + USB-C adapter kiritilgan.</i>"
        ),
    },
    "smartwatch": {
        "name": "⌚ Smart Watch",
        "price": "300 000 so'm",
        "description": (
            "⌚ <b>Smart Watch</b>\n\n"
            "💰 Narxi: <b>300 000 so'm</b>\n\n"
            "📝 <i>Zamonaviy aqlli soat. Yurak urishi monitoring, "
            "qadamlar hisoblagich, uyqu tahlili. "
            "Su o'tkazmaydigan korpus (IP67). "
            "Batareya 7 kungacha ishlaydi.</i>"
        ),
    },
    "powerbank": {
        "name": "🔋 Powerbank",
        "price": "120 000 so'm",
        "description": (
            "🔋 <b>Powerbank</b>\n\n"
            "💰 Narxi: <b>120 000 so'm</b>\n\n"
            "📝 <i>10 000 mAh quvvat sig'imi. "
            "Tez zaryadlash (22.5W) qo'llab-quvvatlaydi. "
            "USB-A + USB-C portlar. Engil va ko'tarishga qulay dizayn.</i>"
        ),
    },
}

# ──────────────────────────────────────────────
#  🔘  KEYBOARD BUILDERS
# ──────────────────────────────────────────────

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Main reply keyboard shown after /start."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Mahsulotlar"), KeyboardButton(text="📞 Aloqa")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Quyidagi menyudan tanlang 👇",
    )


def products_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard listing all products."""
    buttons = [
        [InlineKeyboardButton(text=f"{p['name']} — {p['price']}", callback_data=f"product:{key}")]
        for key, p in PRODUCTS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def order_inline_keyboard(product_key: str) -> InlineKeyboardMarkup:
    """'Place Order' button shown on each product card."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Buyurtma berish", callback_data=f"order:{product_key}")],
            [InlineKeyboardButton(text="⬅️ Orqaga",          callback_data="back_to_products")],
        ]
    )

# ──────────────────────────────────────────────
#  🧭  FSM — ORDER STATES
# ──────────────────────────────────────────────

class OrderState(StatesGroup):
    """States for the multi-step order flow."""
    waiting_for_name    = State()
    waiting_for_phone   = State()
    waiting_for_address = State()

# ──────────────────────────────────────────────
#  🚀  BOT & DISPATCHER SETUP
# ──────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(storage=MemoryStorage())

# ──────────────────────────────────────────────
#  /start  HANDLER
# ──────────────────────────────────────────────

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Handle /start — show welcome message and main menu."""
    await state.clear()   # reset any previous FSM state
    await message.answer(
        "Assalomu alaykum! Do'konimizga xush kelibsiz 😊\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang 👇",
        reply_markup=main_menu_keyboard(),
    )

# ──────────────────────────────────────────────
#  🛍  PRODUCTS SECTION
# ──────────────────────────────────────────────

@dp.message(F.text == "🛍 Mahsulotlar")
async def show_products(message: Message) -> None:
    """Show the product catalogue as an inline keyboard."""
    await message.answer(
        "🛍 <b>Bizning mahsulotlar</b>\n\n"
        "Qiziqtirgan mahsulotni tanlang 👇",
        reply_markup=products_inline_keyboard(),
    )


@dp.callback_query(F.data.startswith("product:"))
async def show_product_detail(callback: CallbackQuery) -> None:
    """Show individual product details with an 'Order' button."""
    product_key = callback.data.split(":")[1]
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.answer("Mahsulot topilmadi!", show_alert=True)
        return

    await callback.message.edit_text(
        product["description"],
        reply_markup=order_inline_keyboard(product_key),
    )
    await callback.answer()


@dp.callback_query(F.data == "back_to_products")
async def back_to_products(callback: CallbackQuery) -> None:
    """Go back to the product list."""
    await callback.message.edit_text(
        "🛍 <b>Bizning mahsulotlar</b>\n\n"
        "Qiziqtirgan mahsulotni tanlang 👇",
        reply_markup=products_inline_keyboard(),
    )
    await callback.answer()

# ──────────────────────────────────────────────
#  📋  ORDER FLOW  (FSM)
# ──────────────────────────────────────────────

@dp.callback_query(F.data.startswith("order:"))
async def start_order(callback: CallbackQuery, state: FSMContext) -> None:
    """
    User tapped 'Place Order'.
    Save the chosen product and ask for their name.
    """
    product_key = callback.data.split(":")[1]
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.answer("Mahsulot topilmadi!", show_alert=True)
        return

    # Persist selected product in FSM storage
    await state.update_data(product_key=product_key, product_name=product["name"])
    await state.set_state(OrderState.waiting_for_name)

    await callback.message.answer(
        "✍️ <b>Buyurtma rasmiylashtirish</b>\n\n"
        "Ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove(),   # hide main keyboard during order flow
    )
    await callback.answer()


@dp.message(OrderState.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    """Receive customer name → ask for phone number."""
    name = message.text.strip()

    # Basic validation
    if len(name) < 2:
        await message.answer("❗ Iltimos, to'liq ismingizni kiriting:")
        return

    await state.update_data(customer_name=name)
    await state.set_state(OrderState.waiting_for_phone)

    await message.answer(
        f"👍 Rahmat, <b>{name}</b>!\n\n"
        "📞 Telefon raqamingizni yuboring:\n"
        "<i>(Masalan: +998901234567)</i>"
    )


@dp.message(OrderState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    """Receive phone number → ask for delivery address."""
    phone = message.text.strip()

    # Basic validation — must be at least 7 characters
    if len(phone) < 7:
        await message.answer("❗ Iltimos, to'g'ri telefon raqam kiriting:")
        return

    await state.update_data(phone=phone)
    await state.set_state(OrderState.waiting_for_address)

    await message.answer(
        "📍 Manzilingizni yozing:\n"
        "<i>(Masalan: Toshkent sh., Yunusobod tumani, 5-mavze)</i>"
    )


@dp.message(OrderState.waiting_for_address)
async def process_address(message: Message, state: FSMContext) -> None:
    """
    Receive address → order is complete.
    1. Send confirmation to the customer.
    2. Send full order details to the admin.
    """
    address = message.text.strip()

    if len(address) < 5:
        await message.answer("❗ Iltimos, to'liqroq manzil kiriting:")
        return

    # ── Collect all order data ──
    data = await state.get_data()
    await state.clear()   # reset FSM

    product_name  = data.get("product_name",  "Noma'lum")
    customer_name = data.get("customer_name", "Noma'lum")
    phone         = data.get("phone",         "Noma'lum")
    username      = f"@{message.from_user.username}" if message.from_user.username else "Yo'q"

    # ── 1. Confirm to the customer ──
    await message.answer(
        "✅ <b>Buyurtmangiz qabul qilindi!</b>\n\n"
        "Tez orada siz bilan bog'lanamiz 📞\n\n"
        "Xarid uchun rahmat! 🙏",
        reply_markup=main_menu_keyboard(),
    )

    # ── 2. Notify the admin with full order details ──
    admin_text = (
        "🛒 <b>YANGI BUYURTMA!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 <b>Mahsulot:</b>  {product_name}\n"
        f"👤 <b>Ism:</b>       {customer_name}\n"
        f"📞 <b>Telefon:</b>   {phone}\n"
        f"📍 <b>Manzil:</b>    {address}\n"
        f"🔗 <b>Username:</b>  {username}\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text)
        logger.info("Order notification sent to admin %s", ADMIN_ID)
    except Exception as exc:
        # If admin notification fails, log it — don't break the user flow
        logger.error("Failed to notify admin: %s", exc)

# ──────────────────────────────────────────────
#  📞  CONTACT SECTION
# ──────────────────────────────────────────────

@dp.message(F.text == "📞 Aloqa")
async def show_contact(message: Message) -> None:
    """Show contact / admin info."""
    await message.answer(
        "📞 <b>Aloqa</b>\n\n"
        f"Admin: {ADMIN_USERNAME}\n\n"
        "Har qanday savol yoki muammo bo'lsa, "
        "admin bilan bog'laning. Doim yordamga tayyormiz! 😊"
    )

# ──────────────────────────────────────────────
#  🌐  ENTRY POINT
# ──────────────────────────────────────────────

async def main() -> None:
    logger.info("Bot ishga tushmoqda... 🚀")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
