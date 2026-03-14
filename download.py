import asyncio
import logging

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from config import settings

logger = logging.getLogger(__name__)


async def download_file(
    context: BrowserContext, file_key: str, file_params: dict
):
    url = file_params["url"]
    logger.info(f"Starting download for {file_key} from {url}")

    page: Page = await context.new_page()

    try:
        # Start waiting for the download event
        async with page.expect_download() as download_info:
            try:
                # This will throw an error because the 'load' state is never reached
                await page.goto(url)
            except Exception as e:
                # We ignore the specific error that says navigation was interrupted by a download
                if "Download is starting" not in str(e):
                    raise e

        download = await download_info.value

        save_path = settings.DOWNLOAD_DIR / file_key
        # Ensure the download directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        await download.save_as(save_path)

        logger.info(f"Successfully downloaded {file_key} to {save_path}")

    except Exception as e:
        logger.error(f"Failed to download {file_key}: {e}")
    finally:
        await page.close()


async def download():
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context()

        # Create a list of tasks for all files in your settings
        tasks = [
            download_file(context, key, params)
            for key, params in settings.FILES.items()
        ]

        # Execute downloads concurrently
        await asyncio.gather(*tasks)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(download())
