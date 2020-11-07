from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


menu_cd = CallbackData("show_menu", "level", "category", "item_id")
buy_item = CallbackData("buy", "item_id")

def make_callback_data(level, category="0", item_id="0"):
    return menu_cd.new(level=level, category=category, item_id=item_id)


async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMrkup()

    categories = await get_categories()

    for category in categories:
        number_of_items = await count_items(category.category_code)
        button_text = f"{category.category_name}({number_of_items} шт)"
        callback_data = make_callback_data(level=CURRENT_LEVEL+1,category=category.category_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    return markup

async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    subcategories = await get_subcategories(category)

    for subcategory in subcategories:
        number_of_items = await count_items(category_code=category, subcategory_code=subcategory)
        button_text = f"{subcategory.subcategory_code}({number_of_items} шт)"
        callback_data = make_callback_data(level=CURRENT_LEVEL+2,category=category, subcategory=subcategory.subcategory_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

      markup.row(
        InlineKeyboardButton(text='Назад',
        callback_data = make_callback_data(level=CURRENT_LEVEL-1)
        )
        
    )

async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)

    items = await get_items(category, subcategory)

    for item in items:
        button_text = f"{item.name} - ${item.price}"
        callback_data = make_callback_data(level=CURRENT_LEVEL+1,category=category, subcategory=subcategory, item_id=item.id)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text='Назад',
        callback_data = make_callback_data(level=CURRENT_LEVEL-1, category=category)
        )
        
    )
    return markup

def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL=3
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(text='Купить',callback_data=but_item.new(item_id=item_id))
    )
    markup.row(
    InlineKeyboardButton(text="Назад",callback_data=make_callback_data(level=CURRENT_LEVEL-1,category=category,subcategory=subcategory))
    )
    return markup

