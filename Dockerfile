FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copy dependency files first (for better caching)
COPY pyproject.toml pdm.lock ./


#RUN apt-get update && apt-get install -y build-essential libffi-dev python3-dev
#RUN pip install --upgrade pip setuptools wheel
#RUN pip install --force-reinstall bcrypt==4.1.3


# Install pdm and dependencies
RUN pip install pdm
RUN pdm install 

# Copy application code
COPY . /app
COPY .env .env


# Expose the correct port


# Run the application (remove --reload for production)
CMD ["pdm", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
