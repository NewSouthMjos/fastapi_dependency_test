## FastAPI dependency possible bug


## UPDATE:

Problem solved on python 3.11.2

If dependency function uses `yield`, injecting dependency with sync def function (`get_something_sync`), the error traceback will broke - it doesn't locate the place where it was rise (should be "/app/main.py", line 24):

```
fastapi_dependency  | INFO:     10.77.78.83:60070 - "GET /1 HTTP/1.1" 500 Internal Server Error
fastapi_dependency  | ERROR:    Exception in ASGI application
fastapi_dependency  | Traceback (most recent call last):
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 419, in run_asgi
fastapi_dependency  |     result = await app(  # type: ignore[func-returns-value]
fastapi_dependency  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
fastapi_dependency  |     return await self.app(scope, receive, send)
fastapi_dependency  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
fastapi_dependency  |     await super().__call__(scope, receive, send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
fastapi_dependency  |     await self.middleware_stack(scope, receive, send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
fastapi_dependency  |     raise exc
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
fastapi_dependency  |     await self.app(scope, receive, _send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
fastapi_dependency  |     raise exc
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
fastapi_dependency  |     await self.app(scope, receive, sender)
fastapi_dependency  |   File "/usr/local/lib/python3.11/contextlib.py", line 222, in __aexit__
fastapi_dependency  |     await self.gen.athrow(typ, value, traceback)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/fastapi/concurrency.py", line 36, in contextmanager_in_threadpool
fastapi_dependency  |     raise e
fastapi_dependency  | ValueError
```

When injecting dependency with async def function (`get_something_async`), the error traceback seems to be right:

```
fastapi_dependency  | INFO:     10.77.78.83:60067 - "GET /2 HTTP/1.1" 500 Internal Server Error
fastapi_dependency  | ERROR:    Exception in ASGI application
fastapi_dependency  | Traceback (most recent call last):
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 419, in run_asgi
fastapi_dependency  |     result = await app(  # type: ignore[func-returns-value]
fastapi_dependency  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
fastapi_dependency  |     return await self.app(scope, receive, send)
fastapi_dependency  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
fastapi_dependency  |     await super().__call__(scope, receive, send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
fastapi_dependency  |     await self.middleware_stack(scope, receive, send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
fastapi_dependency  |     raise exc
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
fastapi_dependency  |     await self.app(scope, receive, _send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
fastapi_dependency  |     raise exc
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
fastapi_dependency  |     await self.app(scope, receive, sender)
fastapi_dependency  |   File "/usr/local/lib/python3.11/contextlib.py", line 222, in __aexit__
fastapi_dependency  |     await self.gen.athrow(typ, value, traceback)
fastapi_dependency  |   File "/app/main.py", line 13, in get_something_async
fastapi_dependency  |     yield True
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
fastapi_dependency  |     raise e
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
fastapi_dependency  |     await self.app(scope, receive, send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
fastapi_dependency  |     await route.handle(scope, receive, send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
fastapi_dependency  |     await self.app(scope, receive, send)
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/routing.py", line 66, in app
fastapi_dependency  |     response = await func(request)
fastapi_dependency  |                ^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/fastapi/routing.py", line 235, in app
fastapi_dependency  |     raw_response = await run_endpoint_function(
fastapi_dependency  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/fastapi/routing.py", line 163, in run_endpoint_function
fastapi_dependency  |     return await run_in_threadpool(dependant.call, **values)
fastapi_dependency  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
fastapi_dependency  |     return await anyio.to_thread.run_sync(func, *args)
fastapi_dependency  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/anyio/to_thread.py", line 31, in run_sync
fastapi_dependency  |     return await get_asynclib().run_sync_in_worker_thread(
fastapi_dependency  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 937, in run_sync_in_worker_thread
fastapi_dependency  |     return await future
fastapi_dependency  |            ^^^^^^^^^^^^
fastapi_dependency  |   File "/usr/local/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 867, in run
fastapi_dependency  |     result = context.run(func, *args)
fastapi_dependency  |              ^^^^^^^^^^^^^^^^^^^^^^^^
fastapi_dependency  |   File "/app/main.py", line 24, in router_func
fastapi_dependency  |     raise ValueError
fastapi_dependency  | ValueError
```