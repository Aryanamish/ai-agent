from contextvars import ContextVar

_organization_slug = ContextVar("organization_slug", default=None)


def set_organization_slug(slug: str) -> None:
    _organization_slug.set(slug)


def get_organization_slug() -> str | None:
    return _organization_slug.get()


def clear_organization_slug() -> None:
    _organization_slug.set(None)
