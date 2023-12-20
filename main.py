import telebot
from config import keys, TOKEN
from extensions import ConversionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    bot.reply_to(message, "Чтобы приступить к работе введите команду боту в следующем формате:\n"
                          "<ВАЛЮТА> <в какую ВАЛЮТУ переводим> <КОЛ-ВО>\n"
                          "Команда /values покажет доступные валюты\n"
                          "Например:\n"
                          "Доллар Юань 10")


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


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
