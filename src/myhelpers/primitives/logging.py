"""Quick logging setup
"""
from __future__ import annotations

import logging

import structlog


# TODO: Change TimeStamper to a custom made one to allow for timezone formatting
def configure_base_logging(level=logging.WARNING, time_fmt: str = "iso"):
    """Configures logging via structlog package
    and re-routes with native logging module
    """
    shared_processors = [
        # Add log level to event dict
        structlog.stdlib.add_log_level,
        structlog.stdlib.ExtraAdder(),
        structlog.processors.TimeStamper(fmt=time_fmt),
    ]

    # noinspection PyTypeChecker
    structlog.configure(
        processors=shared_processors + [
            # Prepare event dict for `ProcessorFormatter`.
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        # `logger_factory` is used to create wrapped loggers that are used for
        # OUTPUT. This one returns a `logging.Logger`. The final value (a JSON
        # string) from the final processor (`JSONRenderer`) will be passed to
        # the method of the same name as that you've called on the bound logger.
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Effectively freeze configuration after creating the first bound logger
        cache_logger_on_first_use=True,
    )

    # Configure log message formatter
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            # Add the name of the logger to event dict
            structlog.stdlib.add_logger_name,
            # Perform %-style formatting
            structlog.stdlib.PositionalArgumentsFormatter(),
            # If the "stack_info" key in the event dict is true, remove it and
            # render the current stack trace in the "stack" key
            structlog.processors.StackInfoRenderer(),
            # If some value is in bytes, decode it to a unicode str
            structlog.processors.UnicodeDecoder(),
            # Add call-site parameters
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
            # Remove _record & _from_structlog
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            # Render the final event dict as JSON
            structlog.dev.ConsoleRenderer(),
        ],
    )

    # Set up stdlib logging handler
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
