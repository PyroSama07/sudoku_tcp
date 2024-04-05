FROM python:3.10-slim
# Set the working directory in the container
WORKDIR /acm

# RUN apk update && apk add tk
# Copy the Python script into the container
COPY . .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tk \
        libtcl8.6 \
        libtk8.6 \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install -r requirements.txt

# Expose the port your application runs on
EXPOSE 12345

# Run the Python script when the container launches
CMD ["python", "sudoku.py"]

