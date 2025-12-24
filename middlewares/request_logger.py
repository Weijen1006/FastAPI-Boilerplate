from fastapi import Request
from fastapi.concurrency import iterate_in_threadpool
from starlette.responses import Response
from configs import settings
import time, json, uuid, http
from utils.logger import logger
from models.request_logger import LogRequest
from middlewares.exceptions import GlobalExceptionHandler

async def LogRequestHandler(request: Request, call_next):
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    start_time = time.time()
    body = (await request.body()).decode()
    if body and len(body) <= settings.LOG_MAX_LENGTH:
        body = json.dumps(json.loads(body))
    else:
        body = ""
    request.state.request_id = str(uuid.uuid4())
    request.state.start_time = start_time
    request.state.body = body
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    try:
        response: Response = await call_next(request)
    except Exception as e:
        logger.error(f"Exception in LogRequestHandler: {e}", exc_info=True)
        response = await GlobalExceptionHandler(request, e)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)

    try:
        status_phrase = http.HTTPStatus(response.status_code).phrase
    except ValueError:
        status_phrase = ""

    response_body = b""
    if hasattr(response, "body"):
        response_body_content = response.body
    elif hasattr(response, "body_iterator"):
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        if response_body:
            response_body_content = response_body[0].decode("utf-8")

    message = f"{host}:{port} - '{request.state.request_id} {request.method} {url}' {response.status_code} {status_phrase} {body} {formatted_process_time}ms {response_body_content}"
    if response.status_code >= 200 and response.status_code < 300:
        logger.info(message)
    else:
        logger.error(message)

    if url.startswith(settings.API_PREFIX):
        log = (LogRequest(
            request_id=request.state.request_id,
            request_header=str(dict(request.headers)),
            request_body=body,
            response_status=response.status_code,
            response_body=response_body_content,
            date_created=request.state.start_time,
            execution_time=formatted_process_time
            ))
        logger.info(log)

    return response