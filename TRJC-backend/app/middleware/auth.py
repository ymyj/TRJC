from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.auth import decode_access_token

WHITELIST = [
    "/api/auth/login",
    "/api/auth/register",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/health",
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 允许 CORS 预检请求直接通过
        if request.method == "OPTIONS":
            return await call_next(request)

        if self._is_whitelisted(request.url.path):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"code": 401, "msg": "未提供认证信息"}
            )

        token = auth_header.replace("Bearer ", "")
        payload = decode_access_token(token)
        if not payload:
            return JSONResponse(
                status_code=401,
                content={"code": 401, "msg": "无效的认证令牌"}
            )

        request.state.user_id = payload.get("sub")
        return await call_next(request)

    def _is_whitelisted(self, path: str) -> bool:
        return any(path.startswith(prefix) for prefix in WHITELIST)
