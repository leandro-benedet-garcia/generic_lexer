import logging
import os
import pathlib
import sys
import tempfile
from typing import Optional

DEBUG: Optional[str] = os.getenv("DEBUG_GENERIC_LEXER")

tmp_log_folder = pathlib.Path(tempfile.gettempdir()) / "generic_lexer" / "logs"
tmp_log_folder.mkdir(parents=True, exist_ok=True)

log_stream = logging.StreamHandler(stream=sys.stdout)
log_file = logging.FileHandler(tmp_log_folder / "run.log.rst")

logger: logging.Logger = logging.getLogger("generic_lexer")
logger.addHandler(log_stream)
logger.addHandler(log_file)

if DEBUG:
    logger.setLevel(logging.DEBUG)

__all__ = ["logger"]
