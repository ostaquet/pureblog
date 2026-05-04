# Hacking with Opencode

This Docker setup provides a sandboxed environment with all tools needed to hack with OpenCode CLI

## Prerequisites

1. Docker and Docker Compose installed
2. A Claude Code account

## Getting Started

```bash
cd .opencode/safe-setup

# Edit .env to set your git identity (based on .env.example)
GIT_USER_NAME=Your Name
GIT_USER_EMAIL=your.email@example.com

# Build and start containers
make up

# Enter the dev environment
make shell
```

## Persistent Data

- **Git configuration**: Automatically set from `GIT_USER_NAME` and `GIT_USER_EMAIL` environment variables

## Inside the Container

You're now user `opencode` in `/workspace` (the project root).

## Commands

| Command         | Description                  |
| --------------- | ---------------------------- |
| `make up`       | Build and start containers   |
| `make down`     | Stop containers              |
| `make shell`    | Enter dev container          |
| `make restart`  | Restart everything           |
| `make logs`     | Follow container logs        |
| `make ps`       | Show container status        |
| `make clean`    | Remove containers and images |
| `make opencode` | Directly launch opencode     |
