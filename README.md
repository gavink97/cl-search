# CL Search
Great premade scripts to scrape the "for sale" section of Craigslist!

## Features
* An easy to use launching script you can run on your crontab or with [Schedule](https://pypi.org/project/schedule/) py
* Transforms multiple pages of listings into a CSV file
* Premade SQL queries to get listings into a MySQL Database
* Supports [Cloudinary](https://cloudinary.com/) image optimization to easily get data in a web app
* Includes scripts to filter out trash & duplicates
* Includes a premade Dockerfile to get your webscraper into the cloud quicker

## How to install CL Search

### Running locally
1. Install the packages via requirements.txt

`pip install --no-cache-dir -r requirements.txt`

2. Place the [Geckodriver](https://github.com/mozilla/geckodriver) into the drivers/firefox directory

3. Profit

### Running in Docker

### With Docker Compose
You can use the following snippet to get started right away

**Under image add your DockerHub Username**

### docker-compose.yml
```
version: "3"
services:
  webscraper:
    image: [Your_Dockerhub_Username]/webscraper:latest
    container_name: webscraper
    volumes:
      - ${PWD}/webscraper:/app:rw
    environment:
      - TZ=${TZ}
    depends_on:
      - mysql
    networks:
      - webscraper
    healthcheck:
      test: [ "CMD", "ping", "-c", "1", "mysql:3306" ]
      interval: 90s
      timeout: 15s
      retries: 5
      start_period: 10s

  mysql:
    image: bitnami/mysql:8.2
    container_name: mysql
    restart: unless-stopped
    volumes:
      - mysql-db:/bitnami/mysql/data
    environment:
      - MYSQL_ROOT_USER=${MYSQL_ROOT_USER}
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_AUTHENTICATION_PLUGIN=caching_sha2_password
      - TZ=${TZ}
    expose:
      - 3306
    networks:
      - webscraper
    healthcheck:
      test: ['CMD', '/opt/bitnami/scripts/mysql/healthcheck.sh']
      interval: 15s
      timeout: 5s
      retries: 6

volumes:
  mysql-db:

networks:
  webscraper:
```
1. Copy the docker-compose.yml above and save it in the primary working directory
2. Place the [Geckodriver](https://github.com/mozilla/geckodriver) into the drivers/firefox directory
2. Run the Docker Compose Up command

`docker compose -f docker-compose.yml up -d`


### A note on Building
With the advent of cheap (sometimes free) & effecient arm64 cpus becoming readily available on major cloud platforms, it has never been more important to build multi-architecture Docker Images.

With that said, we can take advantage of [Docker Buildx](https://github.com/docker/buildx) to quickly build our images in one simple command.
```
# To build locally use:

docker buildx bake -f docker-compose.build.yml

# append the "--push" flag to build + push to docker hub

docker buildx bake -f docker-compose.build.yml --push
```

### docker-compose.build.yml
```
version: "3"
services:

  pyapp:
    image: [Your_Dockerhub_Username]/webscraper:latest
    build:
      context: ${PWD}/webscraper
      dockerfile: Dockerfile
      x-bake:
        platforms:
          - linux/amd64
          - linux/arm64
```
