# ---- Stage 1: Builder ----
# This stage installs build tools and Python dependencies. It will be discarded later.
FROM python:3.13-slim-bullseye AS builder

# Set environment variables to prevent writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build-time dependencies needed to compile certain Python packages (e.g., lxml).
# Combining commands and cleaning up reduces layers and image size.
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ libxml2-dev libxslt-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment. This isolates dependencies and makes them easy to copy.
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy ONLY the requirements file to leverage the build cache.
# This layer is only rebuilt if requirements.txt changes.
COPY requirements.txt .

# Install dependencies without caching to keep the image lean.
RUN pip install --no-cache-dir -r requirements.txt


# ---- Stage 2: Final Image ----
# This is the final, lean image that will be deployed.
FROM python:3.13-slim-bullseye

# Create a dedicated, non-root user for better security.
RUN useradd --create-home --shell /bin/bash appuser

# Install only the necessary RUNTIME dependencies.
# The "-dev" packages and compilers from the build stage are not needed here.
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg libxml2 libxslt1.1 && \
    rm -rf /var/lib/apt/lists/*

# Create and set permissions for a data directory as root before switching users.
ENV XDG_DATA_HOME=/data
RUN mkdir -p $XDG_DATA_HOME/spotdl && \
    chown -R appuser:appuser $XDG_DATA_HOME

# Copy the virtual environment with installed packages from the builder stage.
COPY --chown=appuser:appuser --from=builder /opt/venv /opt/venv

# Copy the application script into the user's home directory.
COPY --chown=appuser:appuser start.sh /home/appuser/app/start.sh

# Switch to the non-root user.
USER appuser
WORKDIR /home/appuser/app

# Add the virtual environment's bin directory to the PATH.
ENV PATH="/opt/venv/bin:$PATH"

# Make the application script executable.
RUN chmod +x start.sh

# The original command for a long-running container.
CMD ["sleep", "infinity"]