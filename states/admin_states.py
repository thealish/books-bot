from aiogram.dispatcher.filters.state import StatesGroup, State



class NewItem(StatesGroup):
    Name = State()
    CategoryName = State()
    AddItem = State()
    Photo = State()
    Price = State()
    Confirm = State()
    Description = State()
    DBConfirm = State()
