# -*- coding:utf-8 -*-
import logging

import aiomysql

logging.basicConfig(level=logging.DEBUG)

import asyncio
from aiohttp import web

#首页
async def list(request):
    return web.Response(body="<h1>Welcom index</h1>",content_type="text/html",charset="utf-8")

#初始化
async def init():
    app = web.Application()
    app.router.add_get("/",list)
    # web.run_app(app, host="127.0.0.1", port=8000)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="127.0.0.1", port=8000)
    await site.start()
    print("Server started at 127.0.0.1:8000")
    return site

'''
注意！！！：由于Web框架使用了基于asyncio的aiohttp，这是基于协程的异步模型。在协程中，不能调用普通的同步IO操作，
因为所有用户都是由一个线程服务的，协程的执行速度必须非常快，才能处理大量用户的请求。
而耗时的IO操作不能在协程中以同步的方式调用，否则，等待一个IO操作时，系统无法响应任何其他用户。

这就是异步编程的一个原则：一旦决定使用异步，则系统每一层都必须是异步，“开弓没有回头箭”。
幸运的是aiomysql为MySQL数据库提供了异步IO的驱动。
'''

#创建连接池(db)
'''
我们需要创建一个全局的连接池，每个HTTP请求都可以从连接池中直接获取数据库连接。
使用连接池的好处是不必频繁地打开和关闭数据库连接，而是能复用就尽量复用。
连接池由全局变量__pool存储，缺省情况下将编码设置为utf8，自动提交事务：
'''
async def createPool(loop, **kw):
    logging.info("创建数据库连接池...")
    global __pool
    __pool = await aiomysql.create_pool(host=kw.get("host","localhost"),
                                        port=kw.get("port", 3306),
                                        user=kw["user"],
                                        password=kw["password"],
                                        db=kw["db"],
                                        charset=kw.get("charset","utf-8"),
                                        autocommit=kw.get("autocommit", True),
                                        maxsize=kw.get("maxsize", 10),
                                        minsize=kw.get("minsize", 1),
                                        loop=loop)

#SELECT语句
'''
SQL语句的占位符是?，而MySQL的占位符是%s，select()函数在内部自动替换。
注意要始终坚持使用带参数的SQL，而不是自己拼接SQL字符串，这样可以防止SQL注入攻击。
注意到await将调用一个子协程（也就是在一个协程中调用另一个协程）并直接获得子协程的返回结果。
如果传入size参数，就通过fetchmany()获取最多指定数量的记录，否则，通过fetchall()获取所有记录。
'''
async def select(sql, args, size=None):
    logging.info(sql,args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace("?", "%s"), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info("返回行记录：%s" % len(rs))
        return rs

#INSERT,UPDATE,DELETE
'''
要执行INSERT、UPDATE、DELETE语句，可以定义一个通用的execute()函数，
因为这3种SQL的执行都需要相同的参数，以及返回一个整数表示影响的行数：
execute()函数和select()函数所不同的是，cursor对象不返回结果集，而是通过rowcount返回结果数
'''
async def execute(sql, args):
    logging.info(sql)
    with (await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace("?","%s"), args)
            affected = cur.rowcount()
            await cur.close()
        except Exception as e:
            print("CUD执行异常：",e)
        return affected

#启动
loop = asyncio.get_event_loop()
loop.run_until_complete(init())
loop.run_forever()


