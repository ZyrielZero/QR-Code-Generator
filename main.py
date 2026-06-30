"""Command-line QR code generator.

Encodes a validated link into a QR image and records each run. Output
directory and colors are read from the environment so the container can
mount them as volumes, while a --url flag overrides the encoded link at
runtime.
"""

import argparse
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import qrcode
import validators
from dotenv import load_dotenv

load_dotenv()

# Configuration
OUTPUT_DIR = Path(os.getenv("QR_CODE_DIR", "qr_codes"))
LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
FOREGROUND = os.getenv("FILL_COLOR", "#4a148c")
BACKGROUND = os.getenv("BACK_COLOR", "white")
DEFAULT_LINK = "https://github.com/ZyrielZero"


def configure_logging() -> None:
    """Log to stdout (so `docker logs` sees it) and to a file under LOG_DIR."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_DIR / "generator.log", encoding="utf-8"),
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a QR code for a link.")
    parser.add_argument(
        "--url",
        default=DEFAULT_LINK,
        help="The link to encode in the QR code.",
    )
    return parser.parse_args()


def link_is_valid(link: str) -> bool:
    if validators.url(link):
        return True
    logging.error("Rejected malformed link: %s", link)
    return False


def build_qr(link: str) -> Path:
    """Encode the link and write a timestamped image, returning its path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    code = qrcode.QRCode(version=1, box_size=10, border=5)
    code.add_data(link)
    code.make(fit=True)

    image = code.make_image(fill_color=FOREGROUND, back_color=BACKGROUND)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    target = OUTPUT_DIR / f"QRCode_{stamp}.png"
    with target.open("wb") as handle:
        image.save(handle)
    return target


def main() -> None:
    configure_logging()
    args = parse_args()

    if not link_is_valid(args.url):
        sys.exit(1)

    logging.info("Encoding link: %s", args.url)
    try:
        saved = build_qr(args.url)
    except Exception as err:
        logging.error("QR generation failed: %s", err)
        sys.exit(1)

    logging.info("Saved QR code to %s", saved)


if __name__ == "__main__":
    main()