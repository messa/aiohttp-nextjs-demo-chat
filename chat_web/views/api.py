from aiohttp import web
from aiohttp_session import get_session
import asyncio
from datetime import datetime
from itertools import count
import logging
from uuid import uuid4


logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

messages = []
message_subcriptions = {}
subscription_id_counter = count()


@routes.get('/api/chat')
async def chat_data(req):
    session = await get_session(req)
    if not session.get('user'):
        raise web.HTTPUnauthorized()
    return web.json_response({
        'user': {
            'name': session['user']['name'],
        },
        'messages': export_messages(),
    })


def export_messages():
    return [export_message(msg) for msg in messages[-20:]]


def export_message(msg):
    return {
        'id': msg['id'],
        'date': msg['date'].strftime('%Y-%m-%dT%H:%M:%SZ'),
        'author': msg['author'],
        'body': msg['body'],
    }


@routes.post('/api/send-message')
async def send_message(req):
    data = await req.json()
    logger.debug('POST data: %r', data)
    session = await get_session(req)
    if not session.get('user'):
        raise web.HTTPUnauthorized()
    messages.append({
        'id': uuid4().hex,
        'date': datetime.utcnow(),
        'author': {
            'name': session['user']['name'],
        },
        'body': data['body'],
    })
    for ev in message_subcriptions.values():
        ev.set()
    return web.json_response({
        'messages': export_messages(),
    })


@routes.get('/api/ws')
async def websockets_handler(req):
    logger.debug('Websockets handler')

    ws = web.WebSocketResponse()
    await ws.prepare(req)

    subscription_id = next(subscription_id_counter)
    msg_event = message_subcriptions[subscription_id] = asyncio.Event()
    try:
        task_msg_wait = asyncio.create_task(msg_event.wait())
        task_receive = asyncio.create_task(ws.receive())
        while True:
            done, pending = await asyncio.wait(
                [task_msg_wait, task_receive],
                return_when=asyncio.FIRST_COMPLETED)
            for task in done:

                if task is task_msg_wait:
                    # new message has been added
                    msg_event.clear()
                    logger.debug('Sending messages to WS client')
                    await ws.send_json({
                        'type': 'messages',
                        'messages': export_messages(),
                    })
                    task_msg_wait = asyncio.create_task(msg_event.wait())

                elif task is task_receive:
                    # websocket message has been received
                    msg = task.result()
                    logger.debug('Received message from WS client: %r', msg)
                    task_receive = asyncio.create_task(ws.receive())

                else:
                    raise Exception('unknown done object')

    finally:
        del message_subcriptions[subscription_id]

    await ws.close()
    return ws
