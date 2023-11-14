# Use the base Python image
FROM python:3.11.4-slim

# Set the working directory inside the container
WORKDIR /app

# Install the requirements (layer caching applied)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Run setup.py and main.py using a shell
CMD ["sh", "-c", "python3 setup.py && python3 main.py"]

