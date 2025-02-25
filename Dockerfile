# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy project files

COPY requirements.txt .
COPY .env .env
# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

