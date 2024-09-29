#!/bin/bash

# Docker Management Script

# Set default values
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

# Function to display usage information
usage() {
    echo "Usage: $0 [option]"
    echo "Options:"
    echo "  start   - Start Docker containers"
    echo "  stop    - Stop Docker containers"
    echo "  restart - Restart Docker containers"
    echo "  logs    - View Docker logs"
    echo "  clean   - Remove stopped containers and unused images"
    echo "  help    - Display this help message"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo "Error: Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to start containers
start() {
    check_docker
    echo "Starting Docker containers..."
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
}

# Function to stop containers
stop() {
    check_docker
    echo "Stopping Docker containers..."
    docker-compose -f $COMPOSE_FILE down
}

# Function to restart containers
restart() {
    stop
    start
}

# Function to view logs
logs() {
    check_docker
    echo "Viewing Docker logs..."
    docker-compose -f $COMPOSE_FILE logs -f
}

# Function to clean up Docker environment
clean() {
    check_docker
    echo "Cleaning up Docker environment..."
    docker system prune -f
    docker volume prune -f
}

# Main script logic
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    clean)
        clean
        ;;
    help)
        usage
        ;;
    *)
        echo "Invalid option: $1"
        usage
        exit 1
        ;;
esac

exit 0