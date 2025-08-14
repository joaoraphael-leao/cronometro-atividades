# 🚀 Guia Completo: Deploy na Oracle Cloud (Ubuntu)

## 📋 Pré-requisitos na Oracle Cloud

### 1. Criar Instance Ubuntu
1. Acesse o Oracle Cloud Console
2. **Compute > Instances > Create Instance**
3. **Configurações recomendadas:**
   - **Image**: Ubuntu 22.04 LTS
   - **Shape**: VM.Standard.E2.1.Micro (Always Free)
   - **Network**: VCN default
   - **SSH Keys**: Adicione sua chave pública

### 2. Configurar Security List
1. **Networking > Virtual Cloud Networks**
2. Selecione sua VCN
3. **Security Lists > Default Security List**
4. **Add Ingress Rules:**

   **Regra 1 - HTTP:**
   - Source CIDR: `0.0.0.0/0`
   - IP Protocol: `TCP`
   - Destination Port Range: `80`

   **Regra 2 - HTTPS:**
   - Source CIDR: `0.0.0.0/0`
   - IP Protocol: `TCP`
   - Destination Port Range: `443`

## 🖥️ Deploy Automatizado

### Opção 1: Script Automatizado (Recomendado)

1. **Conecte-se à VM:**
```bash
ssh -i sua_chave_privada.pem ubuntu@SEU_IP_PUBLICO
```

2. **Execute o deploy automatizado:**
```bash
# Baixar e executar script
wget https://raw.githubusercontent.com/Pedrohsre/cronometro-atividades/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

3. **Aguarde a conclusão** (aproximadamente 5-10 minutos)

4. **Acesse seu site:**
```
http://SEU_IP_PUBLICO
```

## 🔧 Deploy Manual (Passo a Passo)

### Passo 1: Conectar à VM
```bash
ssh -i sua_chave_privada.pem ubuntu@SEU_IP_PUBLICO
```

### Passo 2: Atualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### Passo 3: Instalar Dependências
```bash
sudo apt install -y python3 python3-pip python3-venv git nginx ufw
```

### Passo 4: Clonar Repositório
```bash
cd /home/ubuntu
git clone https://github.com/Pedrohsre/cronometro-atividades.git
cd cronometro-atividades
```

### Passo 5: Configurar Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Passo 6: Testar Aplicação
```bash
python app.py
# Teste em: http://SEU_IP:5000
# Pressione Ctrl+C para parar
```

### Passo 7: Configurar Gunicorn
```bash
# Criar diretório de logs
sudo mkdir -p /var/log/gunicorn
sudo chown ubuntu:ubuntu /var/log/gunicorn

# Testar Gunicorn
gunicorn --config gunicorn_config.py app:app
# Pressione Ctrl+C para parar
```

### Passo 8: Configurar Nginx
```bash
sudo tee /etc/nginx/sites-available/cronometro << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Ativar configuração
sudo ln -sf /etc/nginx/sites-available/cronometro /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Passo 9: Configurar Systemd Service
```bash
sudo tee /etc/systemd/system/cronometro.service << 'EOF'
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
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Configurar e iniciar serviço
sudo systemctl daemon-reload
sudo systemctl enable cronometro
sudo systemctl start cronometro
```

### Passo 10: Configurar Firewall
```bash
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
```

### Passo 11: Verificar Status
```bash
# Status da aplicação
sudo systemctl status cronometro

# Status do Nginx
sudo systemctl status nginx

# Ver logs da aplicação
sudo journalctl -u cronometro -f
```

## ✅ Verificação Final

### 1. Teste Local na VM
```bash
curl http://localhost
```

### 2. Teste Externo
```bash
# No seu computador local
curl http://SEU_IP_PUBLICO
```

### 3. Teste no Navegador
```
http://SEU_IP_PUBLICO
```

## 🔧 Comandos de Gerenciamento

### Logs
```bash
# Logs da aplicação
sudo journalctl -u cronometro -f

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs do Gunicorn
sudo tail -f /var/log/gunicorn/access.log
sudo tail -f /var/log/gunicorn/error.log
```

### Controle de Serviços
```bash
# Reiniciar aplicação
sudo systemctl restart cronometro

# Parar aplicação
sudo systemctl stop cronometro

# Iniciar aplicação
sudo systemctl start cronometro

# Status da aplicação
sudo systemctl status cronometro
```

### Atualizações
```bash
cd /home/ubuntu/cronometro-atividades
git pull origin main
sudo systemctl restart cronometro
```

## 🐛 Solução de Problemas

### Aplicação não inicia
```bash
# Ver logs detalhados
sudo journalctl -u cronometro --no-pager

# Verificar se as dependências estão instaladas
source /home/ubuntu/cronometro-atividades/venv/bin/activate
pip list

# Testar manualmente
cd /home/ubuntu/cronometro-atividades
source venv/bin/activate
python app.py
```

### Nginx com erro
```bash
# Testar configuração
sudo nginx -t

# Ver logs do Nginx
sudo journalctl -u nginx --no-pager

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Porta já em uso
```bash
# Ver o que está usando a porta 5000
sudo lsof -i :5000

# Matar processo se necessário
sudo pkill -f gunicorn
sudo systemctl restart cronometro
```

### Firewall bloqueando
```bash
# Ver status do firewall
sudo ufw status

# Verificar regras
sudo ufw status verbose

# Reconfigurar se necessário
sudo ufw delete allow 80
sudo ufw allow 80
```

## 🔒 Configurações de Segurança

### 1. Firewall
```bash
sudo ufw status
sudo ufw enable
```

### 2. Atualizações Automáticas
```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Backup dos Dados
```bash
# Criar backup dos dados de usuários
tar -czf backup_$(date +%Y%m%d).tar.gz *.json
```

## 📈 Monitoramento

### 1. Status dos Serviços
```bash
# Criar script de monitoramento
tee ~/check_services.sh << 'EOF'
#!/bin/bash
echo "=== Status dos Serviços ==="
echo "Cronometro: $(systemctl is-active cronometro)"
echo "Nginx: $(systemctl is-active nginx)"
echo "UFW: $(ufw status | head -1)"
echo ""
echo "=== Uso de Recursos ==="
echo "CPU: $(top -bn1 | grep "Cpu(s)" | cut -d' ' -f3 | cut -d'%' -f1)%"
echo "RAM: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "Disk: $(df -h / | awk 'NR==2{printf "%s", $5}')"
EOF

chmod +x ~/check_services.sh
```

### 2. Executar Monitoramento
```bash
~/check_services.sh
```

## 🎉 Conclusão

Após seguir este guia, seu cronômetro de atividades estará rodando em:

**🌐 URL:** `http://SEU_IP_PUBLICO`

**📊 Funcionalidades disponíveis:**
- ✅ Cronômetro automático
- ✅ Entrada manual de tempo
- ✅ Sistema de login opcional
- ✅ Dados salvos em cookies (modo anônimo)
- ✅ Dados persistentes (usuários logados)
- ✅ Gráficos visuais
- ✅ Interface responsiva

**🔧 Para gerenciar:**
- Ver logs: `sudo journalctl -u cronometro -f`
- Reiniciar: `sudo systemctl restart cronometro`
- Atualizar: `cd /home/ubuntu/cronometro-atividades && git pull && sudo systemctl restart cronometro`

---

**💡 Dica:** Salve o IP público da sua VM e marque nos favoritos! 🌟
