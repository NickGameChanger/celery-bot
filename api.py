from aiohttp import web
import telegram
import config


async def bot_api_app(argv: list[str] = None) -> web.Application:
    app = web.Application()
    app['bot'] = telegram.Bot(
        token=config.TOKEN)
    app.router.add_routes([
        web.post('/api/send_reminder', tg_send_reminder),
    ])
    return app

async def tg_send_reminder(request: web.Request) -> web.Response:
    try:
        body = await request.json()
        text = body['text']
        chat_id = body['chat_id']
    except (ValueError, KeyError):
        raise web.HTTPBadRequest(text='text, chat_id')
    bot: telegram.Bot = request.app['bot']
    await bot.send_message(chat_id=chat_id, text=f' Ержан блядь! {text}')

    return web.Response()