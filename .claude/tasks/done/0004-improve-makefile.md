# Problem to solve

When I build the project inside the Docker (Linux Alpine), it works. All make steps are working well (build, serve and test). However, when I build the project on the host machine **without** performing a `make clean`, it failed due to dependencies.

I suspect that it is related to the different architecture and therefore the Python virtual env (`.venv`) is not compatible between the two environments.

# Idea of implementation

I was wondering if having 2 Pyhton virtual env will solve the issue; 1 `.venv_docker` and 1 `.venv_local`. The Makefile could be configured to detect if we are on a Docker environment of not and act properly.
