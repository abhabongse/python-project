"""
This module provides tools for configuring logging in Python applications.
"""

from __future__ import annotations

import atexit
import datetime as dt
import json
import logging
import logging.config
import logging.handlers
import tomllib
import zoneinfo
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, override

from rich.style import Style
from rich.theme import Theme

if TYPE_CHECKING:
    from os import PathLike

__all__ = ['setup_logging', 'JSONFormatter']

_LOG_RECORD_BUILTIN_ATTRS = logging.LogRecord(  # Dummy log record
    "name", 0, "pathname", 0, "msg", (), None
).__dict__.keys() | ["asctime"]

THEME = Theme(
    {
        "log.timestamp": Style(color="cyan", dim=True),
        "log.level": Style.null(),
        "log.level.critical": Style(color="red"),
        "log.level.exception": Style(color="red"),
        "log.level.error": Style(color="red"),
        "log.level.warning": Style(color="yellow"),
        "log.level.info": Style(color="cyan"),
        "log.level.debug": Style(color="green"),
        "log.level.notset": Style(bgcolor="red"),
        "log.message": Style.null(),
        "log.logger_name": Style(color="blue"),
        "log.path": Style(dim=True),
        "log.extra.key": Style(color="cyan"),
        "log.extra.value": Style(color="magenta"),
    }
)


def setup_logging(config_file: str | PathLike[str] | None = None, fallback_level: int = logging.WARNING):
    """Configures logging for the main program.

    If the TOML config file is supplied, it is used to configure the logging system.
    Otherwise, a basic configuration is used with the specified fallback level.

    Args:
        config_file: Path to the TOML configuration file for logging
        fallback_level: Fallback logging level to use when config file is not supplied
    """
    if config_file is None:
        # Fallback when config file is not supplied
        logging.basicConfig(
            level=fallback_level,
            format="%(asctime)s [%(levelname)9s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        return
    with Path(config_file).expanduser().resolve(strict=True).open("rb") as f:
        config = tomllib.load(f)
    logging.config.dictConfig(config)
    for handler_name in logging.getHandlerNames():
        handler = logging.getHandlerByName(handler_name)
        if isinstance(handler, logging.handlers.QueueHandler):
            handler.listener.start()  # type: ignore[attr-defined]
            atexit.register(handler.listener.stop)  # type: ignore[attr-defined]


class RichFormatter(logging.Formatter):
    """
    Custom log formatter that outputs log records using the Rich library.
    """

    def __init__(self):
        # TODO: Implement RichFormatter
        #       Consult the Rich documentation (esp. on Table) for details on how to use it
        super().__init__()
        raise NotImplementedError("RichFormatter is not implemented yet.")

    def format(self, record: logging.LogRecord) -> str:
        raise NotImplementedError("RichFormatter is not implemented yet.")


class JSONFormatter(logging.Formatter):
    """
    Custom log formatter that outputs log records as JSON.
    This formatter is meant to be used with [`logging.config.dictConfig`][] compatible configuration.

    Attributes:
        fields: Mapping of JSON keys to internal [`logging.LogRecord`][] attributes
        timezone: Timezone string to use for formatting timestamps (must be compatible with [`zoneinfo.ZoneInfo`][])
        include_extra: Whether to include extra fields in the log record

            - `"nested"` to include them in a separate "extras" field
            - `"flatten"` to include them as top-level fields
            - `None` to exclude them
    """

    fields: dict[str, str]
    timezone: str
    include_extra: Literal["nested", "flatten"] | None

    def __init__(
        self,
        *,
        fields: dict[str, str] | None = None,
        datefmt: str = "%Y-%m-%dT%H:%M:%S%z",
        timezone: str = "UTC",
        include_extra: Literal["nested", "flatten", None] = None,
    ):
        super().__init__(datefmt=datefmt)
        self.fields = fields or {}
        self.timezone = timezone
        self.include_extra = include_extra

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord) -> dict[str, str]:
        # Four fields are always present in the log record: message, timestamp, exc_info, and stack_info
        always_fields = {
            "message": record.getMessage(),
            "timestamp": (
                dt.datetime.fromtimestamp(record.created, tz=dt.UTC)
                .astimezone(zoneinfo.ZoneInfo(self.timezone))
                .strftime(self.datefmt or "%Y-%m-%dT%H:%M:%S%z")
            ),
        }
        if record.exc_info:
            always_fields["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            name: (value if (value := always_fields.pop(field, None)) is not None else getattr(record, field))
            for name, field in self.fields.items()
        }
        message.update(always_fields)

        if self.include_extra == "nested":
            message["extras"] = self._prepare_extras(record)
        elif self.include_extra == "flatten":
            message.update(self._prepare_extras(record))

        return message

    def _prepare_extras(self, record: logging.LogRecord) -> dict[str, Any]:
        return {key: value for key, value in record.__dict__.items() if key not in _LOG_RECORD_BUILTIN_ATTRS}
