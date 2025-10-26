#!/bin/bash

# Multi-Vault Dashboard - Service Shutdown Script
# Gracefully stops all running services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🛑 Stopping Multi-Vault Dashboard Services..."
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to stop a service by PID file
stop_service() {
    local pid_file=$1
    local service_name=$2

    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -n "Stopping $service_name (PID: $pid)..."
            kill "$pid" 2>/dev/null || true

            # Wait for process to stop (max 10 seconds)
            local count=0
            while ps -p "$pid" > /dev/null 2>&1 && [ $count -lt 10 ]; do
                sleep 1
                ((count++))
            done

            # Force kill if still running
            if ps -p "$pid" > /dev/null 2>&1; then
                echo -n " (force killing)..."
                kill -9 "$pid" 2>/dev/null || true
            fi

            echo -e " ${GREEN}✓${NC}"
        else
            echo -e "${YELLOW}$service_name not running (stale PID file)${NC}"
        fi
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}$service_name PID file not found${NC}"
    fi
}

# Create logs directory if it doesn't exist
mkdir -p logs

# Stop each service
stop_service "logs/rag-service.pid" "RAG Service"
stop_service "logs/chat-service.pid" "Chat Service"
stop_service "logs/dashboard.pid" "Dashboard"

# On Windows (Git Bash/MSYS), also try to kill by port
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo ""
    echo "Checking for any remaining processes on ports..."

    # Kill processes on port 3000 (Dashboard)
    netstat -ano | grep ":3000" | grep LISTENING | awk '{print $5}' | while read pid; do
        if [ ! -z "$pid" ]; then
            echo "Killing process on port 3000 (PID: $pid)"
            taskkill //F //PID "$pid" 2>/dev/null || true
        fi
    done

    # Kill processes on port 5000 (Chat)
    netstat -ano | grep ":5000" | grep LISTENING | awk '{print $5}' | while read pid; do
        if [ ! -z "$pid" ]; then
            echo "Killing process on port 5000 (PID: $pid)"
            taskkill //F //PID "$pid" 2>/dev/null || true
        fi
    done

    # Kill processes on port 5001 (RAG)
    netstat -ano | grep ":5001" | grep LISTENING | awk '{print $5}' | while read pid; do
        if [ ! -z "$pid" ]; then
            echo "Killing process on port 5001 (PID: $pid)"
            taskkill //F //PID "$pid" 2>/dev/null || true
        fi
    done
fi

echo ""
echo -e "${GREEN}✓ All services stopped${NC}"
echo ""
