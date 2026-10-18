
from contextvars import ContextVar

session_user = ContextVar("session_user", default=None)
