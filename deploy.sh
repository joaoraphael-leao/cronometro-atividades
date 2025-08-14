#!/bin/bash

# Script de Deploy para Ubuntu (Oracle Cloud)
# Execute este script na sua VM Ubuntu

echo "🚀 Iniciando deploy do Cronômetro de Atividades..."

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
echo "🔧 Instalando dependências do sistema..."
sudo apt install -y python3 python3-pip python3-venv git nginx ufw

# Clonar repositório (se não existir)
if [ ! -d "/home/ubuntu/cronometro-atividades" ]; then
    echo "📁 Clonando repositório..."
    cd /home/ubuntu
    git clone https://github.com/Pedrohsre/cronometro-atividades.git
    cd cronometro-atividades
else
    echo "📁 Atualizando repositório..."
    cd /home/ubuntu/cronometro-atividades
    git pull origin main
fi

# Criar ambiente virtual
echo "🐍 Configurando ambiente Python..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
echo "📚 Instalando dependências Python..."
pip install -r requirements.txt

# Criar diretórios necessários
echo "📂 Criando diretórios..."
sudo mkdir -p /var/log/gunicorn
sudo chown ubuntu:ubuntu /var/log/gunicorn

# Configurar Nginx
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/cronometro << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /home/ubuntu/cronometro-atividades/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Ativar site no Nginx
sudo ln -sf /etc/nginx/sites-available/cronometro /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# Configurar systemd service
echo "⚙️ Configurando serviço systemd..."
sudo tee /etc/systemd/system/cronometro.service << EOF
[Unit]
Description=Cronometro de Atividades
After=network.target

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/cronometro-atividades
Environment="PATH=/home/ubuntu/cronometro-atividades/venv/bin"
ExecStart=/home/ubuntu/cronometro-atividades/venv/bin/gunicorn --config gunicorn_config.py app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Configurar firewall
echo "🔒 Configurando firewall..."
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Iniciar serviços
echo "🎯 Iniciando serviços..."
sudo systemctl daemon-reload
sudo systemctl enable cronometro
sudo systemctl start cronometro
sudo systemctl enable nginx
sudo systemctl start nginx

# Verificar status
echo "✅ Verificando status dos serviços..."
sudo systemctl status cronometro --no-pager
sudo systemctl status nginx --no-pager

echo ""
echo "🎉 Deploy concluído!"
echo "🌐 Seu site estará disponível em: http://SEU_IP_PUBLICO"
echo ""
echo "📋 Comandos úteis:"
echo "  - Ver logs: sudo journalctl -u cronometro -f"
echo "  - Reiniciar app: sudo systemctl restart cronometro"
echo "  - Ver status: sudo systemctl status cronometro"
echo ""
echo "🔧 Para atualizar o código:"
echo "  cd /home/ubuntu/cronometro-atividades"
echo "  git pull origin main"
echo "  sudo systemctl restart cronometro"
