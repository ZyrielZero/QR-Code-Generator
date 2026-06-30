# Use the official slim Python image as the base
FROM python:3.12-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first so this layer caches unless dependencies change
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and the output directories it owns
RUN useradd -m myuser && mkdir logs qr_codes && chown myuser:myuser logs qr_codes

# Copy the application source, owned by the non-root user
COPY --chown=myuser:myuser . .

# Drop root privileges before running
USER myuser

# Default command; --url can be overridden at `docker run`
ENTRYPOINT ["python", "main.py"]
CMD ["--url", "https://github.com/ZyrielZero"]