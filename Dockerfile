FROM python:3.12.2

# Set the working directory in the container
WORKDIR /usr/src/app
# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt to the container
COPY requirements.txt ./

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt
# Copy the folder to the container
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
