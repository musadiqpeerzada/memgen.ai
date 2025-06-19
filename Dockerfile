FROM python:3.11-slim

ENV OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    USER_AGENT=memgen/1.0 \
    HF_HUB_ENABLE_HF_XET=0 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

COPY requirements.txt .
RUN PIP_PROGRESS_BAR=off pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose app port
EXPOSE 8000

# Start FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "asyncio"]