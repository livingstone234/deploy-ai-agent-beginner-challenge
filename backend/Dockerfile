FROM python:latest 

# Create a virtual env
RUN python3 -m venv /opt/venv/
ENV PATH=/opt/venv/bin:$PATH

WORKDIR /app

# COPY local_folder container_destination
COPY requirements.txt /tmp/requirements.txt
# RUN within_within_container_while_building
RUN pip3 install -r /tmp/requirements.txt

COPY ./src .

# CMD [ "python", "-m", "http.server", "8000" ]