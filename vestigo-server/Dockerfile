
FROM python:latest
EXPOSE 8020

# Install needed libraries
RUN mkdir /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
RUN pip3 install gunicorn

# Copy app code over
COPY . /app
WORKDIR /app

# Run Gunicorn with the log file
CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":8020", "--log-file", "/var/vestigo-server/vestigo.log", "--capture-output", "main:app"]