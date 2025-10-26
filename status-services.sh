#!/bin/bash

# Multi-Vault Dashboard - Service Status Script
# Check the status of all running services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "📊 Multi-Vault Dashboard - Service Status"
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to check service health
check_service() {
    local url=$1
    local name=$2
    local port=$3

    echo -n "$name (Port $port): "

    if curl -s "$url" > /dev/null 2>&1; then
        response=$(curl -s "$url")
        echo -e "${GREEN}Running ✓${NC}"

        # Try to extract additional info from JSON response
        if command -v python &> /dev/null; then
            status_info=$(echo "$response" | python -c "import sys, json; data=json.load(sys.stdin); print(f\"  Status: {data.get('status', 'N/A')}\")" 2>/dev/null || echo "")
            if [ ! -z "$status_info" ]; then
                echo "$status_info"
            fi
        fi
        return 0
    else
        echo -e "${RED}Not Running ✗${NC}"
        return 1
    fi
}

# Check each service
rag_running=0
chat_running=0
dashboard_running=0

check_service "http://localhost:5001/health" "RAG Service" "5001" && rag_running=1
check_service "http://localhost:5000/health" "Chat Service" "5000" && chat_running=1
check_service "http://localhost:3000/api/health" "Dashboard" "3000" && dashboard_running=1

echo ""

# Overall status
total_services=3
running_services=$((rag_running + chat_running + dashboard_running))

if [ $running_services -eq $total_services ]; then
    echo -e "${GREEN}✓ All services are running ($running_services/$total_services)${NC}"
elif [ $running_services -eq 0 ]; then
    echo -e "${RED}✗ No services are running ($running_services/$total_services)${NC}"
    echo ""
    echo "To start services, run: ./start-services.sh"
else
    echo -e "${YELLOW}⚠ Some services are not running ($running_services/$total_services)${NC}"
    echo ""
    echo "To start all services, run: ./start-services.sh"
fi

# Check for PID files
echo ""
echo "Process Information:"
mkdir -p logs

if [ -f "logs/rag-service.pid" ]; then
    pid=$(cat logs/rag-service.pid)
    if ps -p "$pid" > /dev/null 2>&1; then
        echo -e "  RAG Service PID: ${GREEN}$pid${NC}"
    else
        echo -e "  RAG Service PID: ${RED}$pid (stale)${NC}"
    fi
else
    echo "  RAG Service PID: Not found"
fi

if [ -f "logs/chat-service.pid" ]; then
    pid=$(cat logs/chat-service.pid)
    if ps -p "$pid" > /dev/null 2>&1; then
        echo -e "  Chat Service PID: ${GREEN}$pid${NC}"
    else
        echo -e "  Chat Service PID: ${RED}$pid (stale)${NC}"
    fi
else
    echo "  Chat Service PID: Not found"
fi

if [ -f "logs/dashboard.pid" ]; then
    pid=$(cat logs/dashboard.pid)
    if ps -p "$pid" > /dev/null 2>&1; then
        echo -e "  Dashboard PID: ${GREEN}$pid${NC}"
    else
        echo -e "  Dashboard PID: ${RED}$pid (stale)${NC}"
    fi
else
    echo "  Dashboard PID: Not found"
fi

# Additional RAG service stats if available
if [ $rag_running -eq 1 ]; then
    echo ""
    echo "RAG Service Details:"

    # Get collections
    collections=$(curl -s "http://localhost:5001/collections" 2>/dev/null || echo "")
    if [ ! -z "$collections" ]; then
        echo "  Collections:"
        echo "$collections" | python -c "import sys, json; data=json.load(sys.stdin); [print(f\"    • {c}\") for c in data.get('collections', [])]" 2>/dev/null || echo "    Unable to parse"
    fi

    # Check ThistleRidgeHall status
    vault_status=$(curl -s "http://localhost:5001/status?vault_name=ThistleRidgeHall" 2>/dev/null || echo "")
    if [ ! -z "$vault_status" ]; then
        doc_count=$(echo "$vault_status" | python -c "import sys, json; data=json.load(sys.stdin); print(data.get('document_count', 0))" 2>/dev/null || echo "0")
        if [ ! -z "$doc_count" ] && [ "$doc_count" != "0" ]; then
            echo "  ThistleRidgeHall: $doc_count documents indexed"
        fi
    fi
fi

echo ""
echo "Service URLs:"
echo "  • RAG Service:  http://localhost:5001"
echo "  • Chat Service: http://localhost:5000"
echo "  • Dashboard:    http://localhost:3000"
echo ""
