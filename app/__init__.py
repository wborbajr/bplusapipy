"""
aioHTTP Rest API
"""

from aiohttp import web
import json

async def handle(request):
    response_obj = { 'status' : 'success' }
    return web.Response(text=json.dumps(response_obj))

def init():
    app = web.Application()
    app.router.add_get('/', handle)
    return app

# if __name__ == '__main__':
web.run_app(init(), port=3000)
