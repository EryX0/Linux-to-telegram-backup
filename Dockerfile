# Use the base Python image
FROM python:3.11.4-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary Python script files
COPY setup.py /app/
COPY main.py /app/

# Install the requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run setup.py and main.py using a shell
CMD ["sh", "-c", "python3 setup.py && python3 main.py"]

