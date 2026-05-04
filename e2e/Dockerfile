FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

WORKDIR /app

# Install project runtime dependencies plus pytest-playwright. The base image
# already ships with Python, pytest, Playwright and all browsers preinstalled.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt pytest-playwright requests

# Copy the whole project (sources, posts, theme, seo, config, e2e tests).
COPY . /app

# Build the static site once at image build time so the container can boot
# directly into "serve + test" mode without an extra build step.
RUN python3 src/main.py

EXPOSE 8000

CMD ["/app/e2e/run.sh"]
