#!/usr/bin/env bash
# Entrypoint for the end-to-end test container.
#
# 1. Serves the already-built static site (see Dockerfile) on port 8000.
# 2. Waits for the HTTP server to become reachable.
# 3. Runs the Playwright test suite against http://localhost:8000.
# 4. Always tears the server down before exiting.

set -euo pipefail

BUILD_DIR="/app/build"
PORT="${E2E_PORT:-8000}"
BASE_URL="http://localhost:${PORT}"

if [[ ! -d "${BUILD_DIR}" ]]; then
    echo "build directory ${BUILD_DIR} not found; rebuilding" >&2
    python3 /app/src/main.py
fi

python3 -m http.server "${PORT}" --directory "${BUILD_DIR}" >/tmp/http.log 2>&1 &
SERVER_PID=$!

cleanup() {
    if kill -0 "${SERVER_PID}" 2>/dev/null; then
        kill "${SERVER_PID}" || true
        wait "${SERVER_PID}" 2>/dev/null || true
    fi
}
trap cleanup EXIT

# Wait up to ~10s for the server to come up.
for _ in $(seq 1 50); do
    if curl --silent --fail --output /dev/null "${BASE_URL}/en/"; then
        break
    fi
    sleep 0.2
done

export E2E_BASE_URL="${BASE_URL}"
exec pytest /app/e2e/test_e2e.py -v --tb=short
