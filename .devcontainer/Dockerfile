FROM debian:bookworm-slim
USER root
WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    libopencv-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*

# Download the latest installer
ADD https://astral.sh/uv/0.5.10/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy the shell configuration
COPY .devcontainer/.bashrc /root/.bashrc

RUN git config --global --add safe.directory /workspace

COPY . /workspace/
