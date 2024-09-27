#!/bin/bash

# Default values
show_count=10  # Default value for --show-count
show_default=false  # Default is not to show default labels
purge_database=false  # Default is not to purge the database

# Function to show usage/help page
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --show-count N       Show N entries (default: 10)"
    echo "  --show-default       Show default labels (optional)"
    echo "  --purge-database     Empties all metrics (optional)"
    echo "  --help               Display this help message"
    exit 0
}

# Parse command-line arguments
while [[ "$1" != "" ]]; do
    case $1 in
        --show-count )
            shift
            show_count=$1
            ;;
        --show-default )
            show_default=true
            ;;
        --purge-database )
            purge_database=true
            ;;
        --help )
            usage
            ;;
        * )
            echo "Unknown option: $1"
            usage
            ;;
    esac
    shift
done

# Purge the database if requested
if [[ "$purge_database" == true ]]; then
    echo "Purging database..."
    docker compose exec sshtarpit python countit_console.py --purge-database
fi

# Construct the command for showing metrics
cmd="docker compose exec sshtarpit python countit_console.py --show-count=$show_count"

# Add the --show-default flag if requested
if [[ "$show_default" == true ]]; then
    cmd="$cmd --show-default"
fi

# Execute the final command
echo "Executing: $cmd"
$cmd
