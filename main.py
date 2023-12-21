import telebot
from config import keys, TOKEN # Тут лежит токен для бота и словарь с валютами (можно добавлять новые)
from extensions import ConversionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


# Обработчик команд /start и /help
@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    bot.reply_to(message, "Чтобы приступить к работе введите команду боту в следующем формате:\n"
                          "<ВАЛЮТА> <в какую ВАЛЮТУ переводим> <КОЛ-ВО>\n"
                          "Команда /values покажет доступные валюты\n"
                          "Например:\n"
                          "Доллар Юань 10")


# Обработчик команды /values
@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


# Здесь основная работа бота:
# Обработка сообщений от пользователя, вывод результата
# Обработчик ошибок (делит их на пользовательские и на программные)
@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) > 3:
            raise ConversionException("Присутствуют лишние параметры!")

        elif len(values) < 3:
            raise ConversionException("Недостаточно параметров!")

        quote, base, amount = values
        cost = CurrencyConverter.get_price(quote, base, amount)
        cost = float(cost) * float(amount)
    except ConversionException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}\nПопробуйте снова.")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}\nПопробуйте снова.")
    else:
        text = f"{amount} {keys[quote]} = {round(cost, 2)} {keys[base]}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
