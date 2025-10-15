#!/bin/bash

# Scientific Writing Training Interface - Setup Script
# This script sets up the development environment

set -e

echo "🎓 Setting up Scientific Writing Training Interface..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    print_warning "MySQL is not installed. Please install MySQL/MariaDB and try again."
    print_warning "You can install it with:"
    print_warning "  Ubuntu/Debian: sudo apt-get install mysql-server"
    print_warning "  macOS: brew install mysql"
    print_warning "  Windows: Download from https://dev.mysql.com/downloads/"
fi

print_step "1. Setting up Python backend..."

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

print_status "Backend setup complete ✓"

print_step "2. Setting up React frontend..."

cd ../frontend/react-flask-app

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install

print_status "Frontend setup complete ✓"

cd ../..

print_step "3. Setting up MySQL database..."

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    print_error "MySQL is not installed or not in PATH. Please install MySQL/MariaDB and try again."
    print_warning "You can install it with:"
    print_warning "  Ubuntu/Debian: sudo apt-get install mysql-server"
    print_warning "  macOS: brew install mysql"
    print_warning "  Windows: Download from https://dev.mysql.com/downloads/"
    exit 1
fi

print_status "Creating database 'tcc_sw'..."
if mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS tcc_sw CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null; then
    print_status "Database 'tcc_sw' created successfully ✓"
else
    print_warning "Failed to create database. Please ensure MySQL is running and root password is correct."
    print_warning "You can manually create the database later with:"
    echo -e "${YELLOW}mysql -u root -p -e \"CREATE DATABASE tcc_sw CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\"${NC}"
    echo ""
fi

print_status "Loading database schema..."
if mysql -u root -p tcc_sw < backend/flaskr/schema.sql 2>/dev/null; then
    print_status "Database schema loaded successfully ✓"
else
    print_warning "Failed to load schema. Please ensure the database exists and root password is correct."
    print_warning "You can manually load the schema later with:"
    echo -e "${YELLOW}mysql -u root -p tcc_sw < backend/flaskr/schema.sql${NC}"
    echo ""
fi

print_status "Loading database data..."
if mysql -u root -p tcc_sw < backend/inserts.sql 2>/dev/null; then
    print_status "Database data loaded successfully ✓"
else
    print_warning "Failed to load data. Please ensure the database exists and root password is correct."
    print_warning "You can manually load the data later with:"
    echo -e "${YELLOW}mysql -u root -p tcc_sw < backend/inserts.sql${NC}"
    echo ""
fi

print_status "Database setup complete ✓"
echo ""

print_step "4. Starting the application..."

print_status "To start the application:"
echo ""
echo -e "${GREEN}# Terminal 1 - Backend:${NC}"
echo -e "${YELLOW}cd backend${NC}"
echo -e "${YELLOW}source venv/bin/activate${NC}"
echo -e "${YELLOW}python app.py${NC}"
echo ""
echo -e "${GREEN}# Terminal 2 - Frontend:${NC}"
echo -e "${YELLOW}cd frontend/react-flask-app${NC}"
echo -e "${YELLOW}npm start${NC}"
echo ""

print_status "🎉 Setup complete!"
print_status "Backend will be available at: http://localhost:5000"
print_status "Frontend will be available at: http://localhost:3000"
