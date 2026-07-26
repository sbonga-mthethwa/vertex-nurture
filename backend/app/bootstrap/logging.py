from fastapi import FastAPI

from app.core.logging import (
    configure_logging as configure_structured_logging,
)
from app.core.logging import logger


def configure_logging(app: FastAPI) -> None:
    """
    Configure application logging.
    """

    configure_structured_logging()

    logger.info(
        "logging_configured",
        application="Vertex Nurture",
    )