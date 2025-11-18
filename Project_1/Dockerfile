FROM python:3.12-slim

# Set the working directory
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files and folders
COPY stops_coords.txt ./
COPY README.md ./
COPY templates/ templates/
COPY static/ static/
COPY routes.py test_routes.py ./

# Copies application files into the container
COPY . /code/

# Set file permissions (optional but can help debugging in some containers)
RUN chmod +rx stops_coords.txt routes.py test_routes.py && \
    chmod -R +rx templates static

# Set environment path (optional, useful if you have CLI tools)
ENV PATH="/code:$PATH"

# Default command to run the app
CMD ["python", "routes.py"]
