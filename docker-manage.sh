#!/bin/bash

# Docker Management Script

# Set default values
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

# Function to display usage information
usage() {
    echo "Usage: $0 [option]"
    echo "Options:"
    echo "  build   - Build or rebuild Docker images"
    echo "  start   - Start Docker containers"
    echo "  stop    - Stop Docker containers"
    echo "  restart - Restart Docker containers"
    echo "  logs    - View Docker logs"
    echo "  clean   - Remove stopped containers and unused images"
    echo "  exec    - Execute a command in the main container"
    echo "           For Python scripts in src/scraper, just use the script name"
    echo "           Example: $0 exec python script.py"
    echo "  help    - Display this help message"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo "Error: Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

#Function to build containers
build() {
    echo "Building Docker images..."
    docker-compose build
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

# Function to execute a command in the main container
exec_command() {
    check_docker
    echo "Executing command in main container..."
    if [[ "$1" == "python" ]]; then
        command="python /opt/airflow/BWF-PredictionSystem/src/scraper/$2 ${@:3}"
        echo "Executing: $command"
        docker-compose -f $COMPOSE_FILE exec airflow-webserver $command
    else
        echo "Executing: $@"
        docker-compose -f $COMPOSE_FILE exec airflow-webserver "$@"
    fi
}

# Main script logic
case "$1" in
    build)
            build
            ;;
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
    exec)
        shift
        exec_command "$@"
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