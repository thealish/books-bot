from aiogram.dispatcher.filters.state import StatesGroup, State


# await add_item(name="Machine Learning with Spark and Python",
#                    category_name="Python 🐍", category_code="books",
#                    subcategory_name="Machine Learning", subcategory_code="ML",
#                    price=100, photo="-")

class NewItem(StatesGroup):
    Name = State()
    CategoryName = State()
    CategoryCode = State()
    SubCategoryName = State()
    SubCategoryCode = State()
    AddItem = State()
    Photo = State()
    Price = State()
    Confirm = State()
    Description = State()
