#!/bin/bash

echo "================================================================"
echo "  Google Instant Indexer - Full Stack Setup"
echo "  Next.js Frontend + FastAPI Backend"
echo "================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Node.js
echo -e "${BLUE}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js not found. Please install Node.js 18+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js $(node --version) found${NC}"
echo ""

# Check Python
echo -e "${BLUE}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 not found. Please install Python 3.8+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python3 --version) found${NC}"
echo ""

# Setup Backend
echo "================================================================"
echo "  Setting up Backend (FastAPI)"
echo "================================================================"
cd backend

echo -e "${BLUE}Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f "google_indexer.py" ]; then
    echo -e "${BLUE}Copying indexing engine...${NC}"
    cp ../google_indexer.py .
fi

echo -e "${GREEN}✓ Backend setup complete!${NC}"
echo ""

# Setup Frontend
echo "================================================================"
echo "  Setting up Frontend (Next.js)"
echo "================================================================"
cd ../google-indexer-app

echo -e "${BLUE}Installing Node.js dependencies...${NC}"
npm install

echo -e "${BLUE}Creating environment file...${NC}"
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

echo -e "${GREEN}✓ Frontend setup complete!${NC}"
echo ""

# Create startup scripts
echo "================================================================"
echo "  Creating startup scripts"
echo "================================================================"

cd ..

# Backend start script
cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
echo "Starting FastAPI Backend on http://localhost:8000"
python api_server.py
EOF
chmod +x start-backend.sh

# Frontend start script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd google-indexer-app
echo "Starting Next.js Frontend on http://localhost:3000"
npm run dev
EOF
chmod +x start-frontend.sh

# Combined start script
cat > start-all.sh << 'EOF'
#!/bin/bash

echo "================================================================"
echo "  Starting Google Instant Indexer"
echo "================================================================"
echo ""

# Start backend in background
echo "Starting backend..."
cd backend
source venv/bin/activate
python api_server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd google-indexer-app
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "================================================================"
echo "  🚀 Application Started!"
echo "================================================================"
echo ""
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop both servers"
echo "================================================================"
echo ""

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF
chmod +x start-all.sh

echo -e "${GREEN}✓ Startup scripts created!${NC}"
echo ""

echo "================================================================"
echo "  🎉 Setup Complete!"
echo "================================================================"
echo ""
echo "To start the application:"
echo ""
echo "  Option 1 - Start everything:"
echo "    ${GREEN}./start-all.sh${NC}"
echo ""
echo "  Option 2 - Start separately:"
echo "    Terminal 1: ${GREEN}./start-backend.sh${NC}"
echo "    Terminal 2: ${GREEN}./start-frontend.sh${NC}"
echo ""
echo "  Option 3 - Manual start:"
echo "    Backend:  cd backend && source venv/bin/activate && python api_server.py"
echo "    Frontend: cd google-indexer-app && npm run dev"
echo ""
echo "Then open: ${BLUE}http://localhost:3000${NC}"
echo ""
echo "API Documentation: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo "================================================================"
