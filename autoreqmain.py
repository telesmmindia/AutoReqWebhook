import logging,sys
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import TokenBasedRequestHandler, setup_application

from core.config import WEB_SERVER_HOST, WEB_SERVER_PORT, OTHER_BOTS_PATH
from handlers import get_handlers_router


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    session = AiohttpSession()
    bot_settings = {"session": session,"default":DefaultBotProperties(parse_mode=ParseMode.HTML)}
    storage = MemoryStorage()
    multibot_dispatcher = Dispatcher(storage=storage)
    multibot_dispatcher.include_router(get_handlers_router())
    app = web.Application()
    TokenBasedRequestHandler(
        dispatcher=multibot_dispatcher,
        bot_settings=bot_settings,
    ).register(app, path=OTHER_BOTS_PATH)
    setup_application(app, multibot_dispatcher)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()