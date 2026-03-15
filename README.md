# spn2-docs-gd2md

This experimental project automates the workflow of exporting Google Docs to Markdown. It uses a headless browser to trigger exports and Pandoc to ensure high-fidelity conversion.

- [SPN2 API Docs](https://docs.google.com/document/d/1Nsv52MvSjbLb2PCpHlat0gkzw0EvtSgpKHu4mk0MnrA)
- [SPN2 Change Log](https://docs.google.com/document/d/19RJsRncGUw2qHqGGg9lqYZYf7KKXMDL1Mro5o1Qw6QI)

---

## 🚀 How it Works

The pipeline follows a three-step automated process:

1.  **Download**: Uses `playwright` to navigate to Google Doc export URLs and save them as `.odt` files.
2.  **Convert**: Uses `pypandoc` to transform the `.odt` files into Markdown.
3.  **Automate**: A GitHub Action runs daily (or on-demand) to sync changes back to the repository.

---

## 🛠 Project Structure

- **`main.py`**: The entry point that orchestrates the download and conversion tasks.
- **`download.py`**: Handles asynchronous browser interactions to fetch files.
- **`convert.py`**: Manages the Pandoc conversion logic and directory handling.
- **`config.py`**: Centralized configuration for file URLs and output paths using `pydantic-settings`.

---

## ⚙️ Setup & Usage

### Prerequisites

- Python 3.13
- Pandoc (system-level)
- Playwright Chromium

### Local Execution

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```
2.  **Run the pipeline**:
    ```bash
    python main.py
    ```

The converted files will be generated in the `converted/` directory as specified in the configuration.
