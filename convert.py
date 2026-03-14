import asyncio
import logging
import pypandoc
from pathlib import Path

from config import settings

logger = logging.getLogger(__name__)


async def convert_file(file_path: Path):
    """
    Converts a file to Markdown using pypandoc.
    """
    # Define the output path (changing extension to .md)
    output_filename = file_path.with_suffix(".md").name
    output_path = settings.CONVERT_DIR / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        logger.info(f"Converting {file_path.name} to Markdown...")

        # pypandoc is synchronous, so we run it in a thread to keep the loop free
        await asyncio.to_thread(
            pypandoc.convert_file,
            file_path,
            "commonmark_x",  # Use 'commonmark_x' or 'gfm' for modern Markdown
            outputfile=output_path,
        )

        logger.info(f"Successfully converted to {output_path}")
    except Exception as e:
        logger.error(f"Failed to convert {file_path.name}: {e}")


async def convert():
    # Check if download directory exists
    if not settings.DOWNLOAD_DIR.exists():
        logger.error(
            f"Download directory {settings.DOWNLOAD_DIR} does not exist."
        )
        return

    tasks = []
    # Iterate through files that match our configuration
    for downloaded_file in settings.DOWNLOAD_DIR.rglob("*"):
        if downloaded_file.name in settings.FILES:
            tasks.append(convert_file(downloaded_file))

    if tasks:
        await asyncio.gather(*tasks)
    else:
        logger.warning("No matching files found to convert.")


if __name__ == "__main__":
    asyncio.run(convert())
