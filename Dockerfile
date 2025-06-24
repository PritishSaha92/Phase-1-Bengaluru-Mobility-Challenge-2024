FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6

# Copy the model
COPY models/best.pt models/best.pt

# Copy source code
COPY src/ src/

CMD ["python", "src/app.py"]
