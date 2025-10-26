#!/bin/bash

# Multi-Vault Dashboard - Service Startup Script
# Starts all three required services: RAG, Chat, and Dashboard

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 Starting Multi-Vault Dashboard Services..."
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Python should now be from Miniconda (fixed via PATH)
PYTHON_CMD="python"

# Function to check if a port is in use
check_port() {
    local port=$1
    if command -v netstat &> /dev/null; then
        netstat -ano | grep ":$port" | grep LISTENING &> /dev/null
    elif command -v lsof &> /dev/null; then
        lsof -i ":$port" &> /dev/null
    else
        # Fallback: try to connect
        (echo > /dev/tcp/localhost/$port) &> /dev/null
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=0

    echo -n "Waiting for $name to start..."
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e " ${GREEN}✓${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
        ((attempt++))
    done
    echo -e " ${RED}✗${NC}"
    echo -e "${RED}Failed to start $name after ${max_attempts}s${NC}"
    return 1
}

# Check if services are already running
if check_port 5001; then
    echo -e "${YELLOW}⚠ RAG Service already running on port 5001${NC}"
else
    echo "Starting RAG Service (Port 5001)..."
    cd "$SCRIPT_DIR/rag-service"
    "$PYTHON_CMD" app.py > ../logs/rag-service.log 2>&1 &
    echo $! > ../logs/rag-service.pid
    cd "$SCRIPT_DIR"
fi

if check_port 5000; then
    echo -e "${YELLOW}⚠ Chat Service already running on port 5000${NC}"
else
    echo "Starting Chat Service (Port 5000)..."
    cd "$SCRIPT_DIR/ollama-service"
    "$PYTHON_CMD" app.py > ../logs/chat-service.log 2>&1 &
    echo $! > ../logs/chat-service.pid
    cd "$SCRIPT_DIR"
fi

if check_port 3000; then
    echo -e "${YELLOW}⚠ Dashboard already running on port 3000${NC}"
else
    echo "Starting Dashboard (Port 3000)..."
    node server.js > logs/dashboard.log 2>&1 &
    echo $! > logs/dashboard.pid
fi

echo ""
echo "⏳ Waiting for services to be ready..."
echo ""

# Wait for each service
wait_for_service "http://localhost:5001/health" "RAG Service"
wait_for_service "http://localhost:5000/health" "Chat Service"
wait_for_service "http://localhost:3000/api/health" "Dashboard"

echo ""
echo -e "${GREEN}✓ All services started successfully!${NC}"
echo ""

# Start file watchers for all vaults
echo "🔍 Starting file watchers for auto-update..."
echo ""

VAULTS=("Study" "Creative-Incubator" "Business-Incubator" "Red-White" "ThistleRidgeHall" "SickRabbit" "Library" "Life-Systems" "Praxis")

for vault in "${VAULTS[@]}"; do
    echo -n "  Starting watcher for $vault..."
    response=$(curl -s -X POST http://localhost:5001/watcher/start \
        -H "Content-Type: application/json" \
        -d "{\"vault_name\": \"$vault\"}")

    if echo "$response" | grep -q "started"; then
        echo -e " ${GREEN}✓${NC}"
    else
        echo -e " ${YELLOW}⚠${NC}"
    fi
done

echo ""
echo -e "${GREEN}✓ File watchers activated - auto-update enabled!${NC}"
echo ""
echo "Service URLs:"
echo "  • RAG Service:  http://localhost:5001"
echo "  • Chat Service: http://localhost:5000"
echo "  • Dashboard:    http://localhost:3000"
echo ""
echo "Log files:"
echo "  • RAG Service:  logs/rag-service.log"
echo "  • Chat Service: logs/chat-service.log"
echo "  • Dashboard:    logs/dashboard.log"
echo ""
echo "Auto-Update: ${GREEN}ENABLED${NC} for all 9 vaults"
echo ""
echo "To stop services, run: ./stop-services.sh"
echo ""
