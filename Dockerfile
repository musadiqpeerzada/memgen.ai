FROM python:3.11-slim

# limit BLAS/OMP/MKL to 1 thread and identify your client
ENV OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    USER_AGENT=memgen/1.0

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN PIP_PROGRESS_BAR=off pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Expose port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]