# flake8: noqa: E501
from simple.settings.base import *

DEBUG = False
ENV = "test"
SECRET_KEY = "TEST_SECRET_KEY"

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.stub.StubBroker",
    "OPTIONS": {},
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Pipelines",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
    ],
}
# StubBroker - это имитация брокера, которая работает в памяти без внешних зависимостей.
# class ProcessesAccountTests(BaseTestSet, DramatiqTestCase):
# stat = StatisticsProcess(call_id=call_5.id).execute()

BASE_URL = "https://base.url.intra"


TELEGRAM_TOKEN = "TEST_TELEGRAM_TOKEN"
TELEGRAM_MONITOR_CHAT_ID = "TEST_TELEGRAM_CHAT_ID"
TELEGRAM_BLOCKS_CHAT_ID = "TEST_TELEGRAM_CHAT_ID"
