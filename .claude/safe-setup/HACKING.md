# Hacking with Claude Code

This Docker safe-setup provides a sandboxed environment with all tools needed to work with Claude Code.

## Prerequisites

1. Docker and Docker Compose installed
2. A Claude Code account

## Getting Started

```bash
cd .claude/safe-setup

# Edit .env to set your git identity (based on .env.example)
GIT_USER_NAME=Your Name
GIT_USER_EMAIL=your.email@example.com

# Build and start containers
make up

# Enter the dev environment
make claude
```

## Inside the Container

You're now user `claude` in `/workspace` (the project root).

Python and Go development environments are available. The container is also configured to support running Docker in a Docker (for E2E tests).

## Commands

| Command        | Description                  |
| -------------- | ---------------------------- |
| `make up`      | Build and start containers   |
| `make down`    | Stop containers              |
| `make shell`   | Enter dev container          |
| `make restart` | Restart everything           |
| `make logs`    | Follow container logs        |
| `make ps`      | Show container status        |
| `make clean`   | Remove containers and images |
| `make claude`  | Directly launch claude       |
