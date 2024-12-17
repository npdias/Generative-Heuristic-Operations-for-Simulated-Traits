import logging
from nicegui import ui


class LogElementHandler(logging.Handler):
    """A custom logging handler that emits log messages to a NiceGUI log element."""

    def __init__(self, log_component: ui.log, level: int = logging.NOTSET) -> None:
        super().__init__(level)
        self.log_component = log_component

    def emit(self, record: logging.LogRecord) -> None:
        """Push formatted log messages to the NiceGUI log component."""
        try:
            message = self.format(record)
            self.log_component.push(message)
        except Exception:
            self.handleError(record)