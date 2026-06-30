# QR Code Generator

A small command-line tool that encodes a URL into a QR code image. Output location and colors are configurable through environment variables, and the app is packaged as a Docker image for reproducible runs anywhere.

## Features

- Generates a QR code PNG from any valid URL
- Validates the URL before encoding and rejects malformed input
- Configurable output directory and colors via environment variables
- Timestamped filenames so repeated runs never overwrite each other
- Logs each run to both the console and a log file
- Containerized with Docker and published to DockerHub

## Requirements

- Python 3.12 (or run it through Docker, no local Python needed)
- Dependencies listed in `requirements.txt`

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run with the default URL:

```bash
python main.py
```

Encode a specific URL:

```bash
python main.py --url https://www.njit.edu
```

The QR code is saved to the `qr_codes/` directory by default.

## Configuration

The following environment variables override the defaults:

| Variable       | Default                          | Description                       |
| -------------- | -------------------------------- | --------------------------------- |
| `QR_CODE_DIR`  | `qr_codes`                       | Directory where images are saved  |
| `LOG_DIR`      | `logs`                           | Directory for the log file        |
| `FILL_COLOR`   | `#4a148c`                        | QR code foreground (dark) color   |
| `BACK_COLOR`   | `white`                          | QR code background (light) color  |

Note: keep the fill color dark and the background light. Scanners read dark modules on a light background, so inverting them produces a code that will not scan.

## Running with Docker

Build the image:

```bash
docker build -t qr-code-generator-app .
```

Run it (writes the QR code to a mounted host folder):

```bash
docker run --rm -v "$(pwd)/qr_codes:/app/qr_codes" qr-code-generator-app --url https://www.njit.edu
```

## Pull from DockerHub

The image is published at [`zyrielzero/qr-code-generator-app`](https://hub.docker.com/r/zyrielzero/qr-code-generator-app):

```bash
docker pull zyrielzero/qr-code-generator-app:latest
docker run --rm zyrielzero/qr-code-generator-app
```

## Continuous Integration

A GitHub Actions workflow (`.github/workflows/docker-image.yml`) builds the image and pushes it to DockerHub automatically on every push to `main`.
