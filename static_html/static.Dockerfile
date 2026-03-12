# declare what image to use
# FROM image_name:latest
FROM python:latest 

# making static web server to avoid seeing the docker system files 
# WORKDIR /app
# RUN echo "hello" > index.html

WORKDIR /app

# COPY local_folder container_folder
# COPY ./src ./app
COPY ./src .

# docker build -f Dockerfile -t pyapp .
# docker run -it pyapp

# docker build -f Dockerfile -t livis71/ai-py-app:latest .
# docker push livis71/ai-py-app:latest

# python -m http.server 8000
# docker run -it -p 3000:8000 pyapp
CMD [ "python", "-m", "http.server", "8000" ]