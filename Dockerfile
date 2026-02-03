# -------- Base Image --------
FROM python:3.10-slim

# -------- Environment --------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# -------- System Dependencies --------
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# -------- Set Workdir --------
WORKDIR /app

# -------- Copy dependency files --------
COPY requirements.txt .
COPY setup.py .

# -------- Install Python dependencies (pip, NOT uv) --------
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -e .

# -------- Copy project code --------
COPY . .

# -------- Expose port --------
EXPOSE 8000

# -------- Run server --------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
