#!/bin/bash

# Configure git user/email from environment variables if provided
if [ -n "$GIT_USER_NAME" ]; then
    git config --global user.name "$GIT_USER_NAME"
fi

if [ -n "$GIT_USER_EMAIL" ]; then
    git config --global user.email "$GIT_USER_EMAIL"
fi

# Fix CRLF handling for Windows-mounted repos (no impact on Mac)
git config --global core.autocrlf input

# Mark /workspace as safe (owned by root, user is claude)
git config --global --unset-all safe.directory '^/workspace$' || true
git config --global --add safe.directory /workspace

# Ensure that the Docker socket has the correct permissions for the 'docker' group
# (to let Claude run integration tests in his own environment)
sudo chown root:docker /var/run/docker.sock

# Execute the command passed to the container
exec "$@"
