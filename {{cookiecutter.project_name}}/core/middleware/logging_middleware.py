from typing import Optional, Union

from starlette.requests import HTTPConnection, Request
from starlette_context.plugins import Plugin


class URLPlugin(Plugin):
    key = "url"

    async def extract_value_from_header_by_key(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[str]:
        return str(request.url)
