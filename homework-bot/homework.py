import logging
import os
import sys
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from telebot import apihelper, TeleBot

from exceptions import EmptyTokenError, RequestApiError, ResponseApiError


load_dotenv()


PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка существования обязательных токенов."""
    required_tokens = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID
    }
    empty_tokens = []
    for name, value in required_tokens.items():
        if not value:
            empty_tokens.append(name)
    if empty_tokens:
        logging.critical(f'Проверь {", ".join(empty_tokens)}'
                         ', сейчас там пусто!')
        raise EmptyTokenError(f'Проверь {", ".join(empty_tokens)}'
                              ', сейчас там пусто!')
    logging.info('Обязательные переменные окружения существуют!')


def send_message(bot, message):
    """Отправка сообщения в ТГ."""
    try:
        logging.debug(f'Начало отправки сообщения({message}) в Telegram')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.debug(f'Удачная отправка сообщения({message}) в Telegram')
    except (apihelper.ApiException, requests.RequestException) as error:
        logging.error(f'Сбой при отправке сообщения в тг: {error}')
        return False
    return True


def get_api_answer(timestamp):
    """Проверка запроса к API Практикума."""
    payload = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(ENDPOINT,
                                         headers=HEADERS, params=payload)
    except requests.RequestException as e:
        raise RequestApiError(f'Проверь запрос API, ошибка {e}')
    status = homework_statuses.status_code
    if status != HTTPStatus.OK:
        raise RequestApiError(f'Проблема: статус запроса = {status}')
    logging.debug('Успешный запрос к API!')
    return homework_statuses.json()


def check_response(response):
    """Проверка соответствия ответа запроса."""
    if not isinstance(response, dict):
        raise TypeError(f'API не вернул словарь (dict), тип: {type(response)}')
    if 'homeworks' not in response:
        raise ResponseApiError('Ответ API не содержит ключа homeworks')
    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise TypeError('homeworks не является списком')
    logging.info('Ответ запроса соответствует ожиданиям!')
    return homeworks


def parse_status(homework):
    """Проверка статуса и имени домашки."""
    if 'homework_name' not in homework:
        raise KeyError('В ответе нет ключа homework_name')
    if 'status' not in homework:
        raise KeyError('В ответе нет ключа status')
    status = homework.get('status')
    if status not in HOMEWORK_VERDICTS:
        raise ValueError(f'Неизвестный статус {status}')

    homework_name = homework.get('homework_name')
    verdict = HOMEWORK_VERDICTS.get(status)
    logging.info('Статус работы соответствует ожиданиям!')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()

    bot = TeleBot(token=TELEGRAM_TOKEN)
    logging.info('Bot начал работу!')
    timestamp = int(time.time())
    last_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)

            if homeworks:
                message = parse_status(homeworks[0])
                if send_message(bot, message):
                    timestamp = response.get('current_date', int(time.time()))
                    last_message = message

            logging.debug(f'Timestamp: {timestamp}')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.exception(message)
            if message != last_message:
                if send_message(bot, message):
                    last_message = message

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=logging.DEBUG,
        stream=sys.stdout
    )
    main()
