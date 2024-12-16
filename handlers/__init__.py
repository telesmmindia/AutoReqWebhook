from aiogram import Router

def get_handlers_router() -> Router:
    from . import  user_handler,add_channel,my_channels,broadcast_handler,req_handler
    router = Router()
    router.include_router(user_handler.router)
    router.include_router(add_channel.router)
    router.include_router(my_channels.router)
    router.include_router(broadcast_handler.router)
    router.include_router(req_handler.router)

    return router
