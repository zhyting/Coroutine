1> 函数中带 yield 的就称之为生成器
2> 生成器进化为协程
    yield 关键字可以在表达式中使用
    生成器的调用方可以使用send 方法发送数据

协程是一种特殊的生成器，可以自动控制启动与停止的时机，也就是如果想停止那么就在这个位置添加 yield ，如果想继续
那么生成器的调用方就可以调用send，让其继续执行。 [按照自己的需求设置yield 让其停顿，同时调用send 让其继续，
从而实现调度。]
设置好yield 的位置，就是我们希望放弃控制权的位置，也就是在此处如果条件不满足，那么就可能发生阻塞，所以在这个
位置之前就需要注册好相应的事件，接着执行 yield 表达式，交出线程的控制权，接着当事件到来时，在注册的回调函数
中执行send ，让其进行执行。

最简单的协程
def simple_coroutine():
    print('-> coroutine started')
    x = yield 
    print('-> coroutine received: ',x)

simple_coroutine 中需要手动将其启动(手动调用next),可以使用装饰器对其进行简化(预激协程的装饰器)
from functools import wraps
def coroutine(func):
    @wraps(func)
    def primer(*args,**kwargs):
        gen = func(*args,**kwargs)
        next =(gen)
        return gen
    return primer

g = coroutine(simple_coroutine())

现在只是需要在函数前面加一个 async 即可
await 就相当于 yield from 



python 3.4 中使用 @asyncio.coroutine 装饰的函数称为协程(在python 3.8 中被移除)
coroutine 就是一个装饰器，其源码大致如下: 
import functools
import types
import inspect

import asyncio

def coroutine(func):
    # 判断是否是生成器
    if inspect.isgeneratorfunction(func):
        coro = func
        print('func is generator')
    else:
        # 将普通函数变成generator
        @functools.wraps(func)
        def coro(*args, **kw):
            res = func(*args, **kw)
            res = yield from res
            return res
        print('func is not generator')
    # 将generator转换成coroutine
    wrapper = types.coroutine(coro)
    # For iscoroutinefunction().
    wrapper._is_coroutine = True
    return wrapper
@coroutine
def func_test():
    print('hello world')
    return 'OK'


print(type(func_test))
#print(asyncio.iscoroutine(func_test()))
print(asyncio.iscoroutinefunction(func_test()))

此处 func_test 就是一个普通函数(内部没有 yield or  yield from)，然后通过 coroutine 的装饰，将其变成协程，


测试例子如下: 
import asyncio

@asyncio.coroutine
def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    yield from asyncio.sleep(1.0)
    return x + y

@asyncio.coroutine
def print_sum(x, y):
    result = yield from compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
print("start")
# 中断调用，直到协程执行结束
loop.run_until_complete(print_sum(1, 2))
print("end")
loop.close()




@asyncio.coroutine 在python 3.8 中不再支持
python 3.5 后开始引入 async & await ,
async 用于替换 @asyncio.coroutine 
await 用于替换 yield from 

上面的例子可以重新写成: 
import asyncio


async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y


async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))


loop = asyncio.get_event_loop()
print("start")
loop.run_until_complete(print_sum(1, 2))
print("end")
loop.close()




其他的一些内容: 
async with: 上下文管理器
async  for : 异步迭代器


参考
https://juejin.im/post/6844903737257885704