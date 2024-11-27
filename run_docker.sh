#docker run --rm -it --env-file .env klassenarbeiten

docker run -d --restart unless-stopped --name klassenarbeiten --env-file .env klassenarbeiten