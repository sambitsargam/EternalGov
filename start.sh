#!/bin/bash
# Quick start script for EternalGov with real Membase

echo "🚀 EternalGov Startup Script"
echo "=============================="

# Check if .env exists, if not prompt user
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo ""
    echo "Create .env file with:"
    echo "  MEMBASE_ID=eternalgov_delegate"
    echo "  MEMBASE_ACCOUNT=0x..."
    echo "  MEMBASE_SECRET_KEY=your_key"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ .env file found"
    source .env
fi

echo ""
echo "📋 Pre-flight checks:"
echo "---"

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python: $python_version"

# Check dependencies
echo -n "✅ Checking dependencies..."
python -c "import streamlit; import plotly; import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " ❌"
    echo "Installing dependencies..."
    pip install streamlit plotly pandas python-dotenv
else
    echo " ✅"
fi

# Run integration test
echo ""
echo "🔍 Running integration test:"
echo "---"
python test_membase_integration.py

echo ""
echo "🎨 Starting Streamlit UI..."
echo "---"
echo "Visit: http://localhost:8501"
echo ""
echo "Next steps:"
echo "1. Go to Settings → Setup page"
echo "2. Verify Membase connection"
echo "3. Click 'Initialize EternalGov'"
echo "4. Click 'Start Data Ingestion'"
echo "5. Check Memory page to see synced data"
echo ""

streamlit run ui.py
