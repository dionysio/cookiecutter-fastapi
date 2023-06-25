from starlette_context import context
from starlette_context.header_keys import HeaderKeys


def get_pretty_context():
    try:
        return dict(
            (i.name, j) if isinstance(i, HeaderKeys) else (i, j)
            for i, j in context.items()
        )
    except Exception:
        return dict()
