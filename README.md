
# FastAPI PostgreSQL Dockerized App

This is a FastAPI application connected to a PostgreSQL database, containerized with Docker and orchestrated using Docker Compose. The app is deployed on AWS EC2 and uses GitHub Actions for continuous deployment.

## Table of Contents
- [Project Description](#project-description)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Docker Setup](#docker-setup)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [CI/CD Pipeline](#cicd-pipeline)
- [Project Structure](#project-structure)
- [License](#license)

---

## Project Description

This project is a web application built with **FastAPI** and connected to a **PostgreSQL** database. The application and database are containerized using **Docker** and managed with **Docker Compose**. The app provides a simple API, and it interacts with the database to handle persistent data.

The application is hosted on an **AWS EC2** instance and is automatically deployed using **GitHub Actions**.
For openAPI documentation, visit

```bash
 http://18.205.107.171:8000/docs/
```

---

## Technologies Used
- **FastAPI**: Web framework for building APIs.
- **PostgreSQL**: Database for storing persistent data.
- **Docker**: Containerization of both the FastAPI app and PostgreSQL database.
- **Docker Compose**: Orchestrates the multi-container application.
- **GitHub Actions**: Automates CI/CD pipeline to deploy the app to AWS EC2.
- **AWS EC2**: Hosting the application in the cloud.

---

## Prerequisites

Before setting up the project, ensure you have the following installed:
- **Docker**: To containerize the application and database.
- **Docker Compose**: To orchestrate the containers.
- **Git**: For cloning the repository.
- **AWS EC2**: An EC2 instance to deploy the app.
- **GitHub account**: To configure GitHub Actions for CI/CD.

You will also need:
- AWS SSH key for deploying to EC2.
- Database credentials (POSTGRES_USER, POSTGRES_PASSWORD, etc.).

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/akuldevali/Blockhouse.git
cd Blockhouse
```

### 2. Set up environment variables

Create `.env` file and add the database credentials as needed.

```bash
DATABASE_URL=postgresql://<User>:<password>@localhost:5432/Blockhouse
```

### 3. Build the Docker containers

If you are running Docker Compose, use the following command to build the containers:

```bash
docker-compose build
```

This will build the FastAPI application container and the PostgreSQL container.

### 4. Start the containers

To start both containers (FastAPI and PostgreSQL), use:

```bash
docker-compose up
```

The FastAPI app will be accessible at `http://localhost:8000` and the PostgreSQL database will be accessible at `localhost:5432`.

---

## Docker Setup

### Docker Compose Configuration

The `docker-compose.yml` file defines two services:

- **app**: The FastAPI application container.
- **db**: The PostgreSQL database container.

**`docker-compose.yml`**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    volumes:
      - ./:/app:ro
    environment:
      DATABASE_URL: "postgresql://postgres:meowmeow@db:5432/Blockhouse"

  db:
    image: postgres:17
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: meowmeow
      POSTGRES_DB: Blockhouse
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Deployment

This project uses **GitHub Actions** to automate the deployment process to **AWS EC2**. When you push changes to the `main` branch, the following steps are triggered:

1. **SSH into EC2**: The action logs into the EC2 instance using SSH and deploys the latest code.
2. **Build the Docker containers**: The app container and the database container are built and started.
3. **Clean up**: Old Docker images are removed to free up space.

### Deployment Workflow

The GitHub Actions workflow is defined in the `.github/workflows/deploy.yml` file. It includes steps for:

- Checking out the code.
- SSHing into EC2 and running deployment commands.
- Building Docker images and starting containers.


### GitHub Secrets for Deployment

For secure deployment via GitHub Actions, you need to set the following secrets in your GitHub repository:

- **EC2_HOST**: The public IP or domain of your EC2 instance.
- **EC2_SSH_KEY**: Your EC2 SSH private key (ensure it is saved in GitHub as a secret).

---

## CI/CD Pipeline

The **GitHub Actions** pipeline is set up to automate the process of deploying the app every time there is a push to the `main` branch.

The workflow file `.github/workflows/deploy.yml` contains the following key steps:

1. **Checkout the code**: Pull the latest code from the GitHub repository.
2. **SSH into EC2**: Securely access your AWS EC2 instance.
3. **Stop and remove the previous container**: Ensure the old container is stopped and removed.
4. **Build and deploy the containers**: Rebuild and redeploy the Docker containers with the latest code.
5. **Cleanup**: Remove unused Docker images and containers.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
