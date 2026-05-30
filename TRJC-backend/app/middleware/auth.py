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

# 支持带前缀的路径（如 /trjcai/api/auth/login）
WHITELIST_PREFIXES = ["/trjcai"]

def _get_whitelist_patterns():
    """生成所有可能的白名单路径模式"""
    patterns = list(WHITELIST)
    for prefix in WHITELIST_PREFIXES:
        for path in WHITELIST:
            patterns.append(f"{prefix}{path}")
    return patterns


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
        patterns = _get_whitelist_patterns()
        return any(path.startswith(prefix) for prefix in patterns)
