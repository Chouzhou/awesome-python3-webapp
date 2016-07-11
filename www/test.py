import asyncio

import sys

import www.data_orm as orm
from www.models import User, Blog, Comment


async def test(loop):
    await orm.create_pool(loop=loop, user='root', password='zsw19941202', db='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    await u.save()


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
if loop.is_closed():
    sys.exit(0)
# for x in test():
#     pass
