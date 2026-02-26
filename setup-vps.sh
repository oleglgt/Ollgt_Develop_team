#!/bin/bash
# ============================================
# AI Development Team — VPS Setup Script
# Run this on a fresh Ubuntu 22.04+ server
# ============================================

set -e

echo "🚀 Setting up AI Development Team..."

# ── System packages ──
echo "📦 Installing system packages..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip git curl

# ── Clone repo ──
echo "📂 Cloning repository..."
cd ~
git clone https://github.com/oleglgt/Ollgt_Develop_team.git
cd Ollgt_Develop_team

# ── Python environment ──
echo "🐍 Setting up Python environment..."
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ── Environment file ──
echo "⚙️ Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env with your API keys:"
    echo "    nano .env"
    echo ""
    echo "  Required keys:"
    echo "    - ANTHROPIC_API_KEY"
    echo "    - GITHUB_TOKEN"
    echo "    - TELEGRAM_BOT_TOKEN"
    echo "    - TELEGRAM_CHAT_ID"
fi

# ── Systemd service (optional) ──
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/ai-dev-team.service > /dev/null << EOF
[Unit]
Description=AI Development Team Orchestrator
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/Ollgt_Develop_team
Environment=PATH=$HOME/Ollgt_Develop_team/venv/bin:/usr/bin
ExecStart=$HOME/Ollgt_Develop_team/venv/bin/python agents/orchestrator.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env:           nano .env"
echo "  2. Test manually:       source venv/bin/activate && python agents/orchestrator.py"
echo "  3. Enable service:      sudo systemctl enable ai-dev-team"
echo "  4. Start service:       sudo systemctl start ai-dev-team"
echo "  5. Check logs:          sudo journalctl -u ai-dev-team -f"
