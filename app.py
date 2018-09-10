from tgbotapi import TgBot
from bot import ApiFunctions
from config import config


def transmission_bot(response):
    chat_id = response['message']['chat']['id']
    api_answer = ApiFunctions(response)
    if api_answer.parse_mode:
        return bot.send_message(chat_id=chat_id, text=api_answer.answer, parse_mode=api_answer.parse_mode)
    return bot.send_message(chat_id=chat_id, text=api_answer.answer)


if __name__ == '__main__':
    bot = TgBot(config['telegram']['token'])
    bot.settings['proxies'] = config['telegram']['proxies']
    bot.loop(transmission_bot)
