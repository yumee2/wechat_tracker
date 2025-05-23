from starlette.staticfiles import StaticFiles
from starlette.responses import Response
import os

class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response: Response = await super().get_response(path, scope)
        if response.status_code == 200:
            # Добавляем кэширование на 1 год
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response
