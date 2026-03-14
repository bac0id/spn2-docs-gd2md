import asyncio
import logging
import time

from download import download
from convert import convert

logger = logging.getLogger(__name__)


async def main():
    start_time = time.perf_counter()

    logger.info("Pipeline Started.")

    try:
        logger.info("Downloading files...")
        await download()

        logger.info("Converting files...")
        await convert()

        end_time = time.perf_counter()
        elapsed = end_time - start_time
        logger.info(
            f"Pipeline Completed Successfully in {elapsed:.2f} seconds."
        )

    except Exception as e:
        logger.critical(f"Pipeline failed during execution: {e}")


if __name__ == "__main__":
    asyncio.run(main())
