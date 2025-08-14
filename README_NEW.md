# ⏱️ Cronômetro de Atividades

Um sistema web para rastrear tempo gasto em diferentes atividades, com cronômetro automático e entrada manual de tempo.

## 🚀 Funcionalidades

- **Cronômetro automático** para rastrear tempo em tempo real
- **Entrada manual de tempo** com atalhos rápidos (50 minutos)
- **Sistema de login opcional** - funciona sem cadastro usando cookies
- **Gráficos visuais** da distribuição de tempo por atividade
- **Interface responsiva** que funciona em desktop e mobile
- **Gerenciamento de atividades** - criar, editar e remover atividades

## 🎯 Modos de Uso

### Modo Anônimo (sem login)
- Use imediatamente sem necessidade de cadastro
- Dados salvos apenas no navegador (cookies)
- Perfeito para uso casual e testes

### Modo Autenticado (com login)
- Dados salvos permanentemente no servidor
- Acesso de qualquer dispositivo
- Histórico preservado entre sessões

## 🛠️ Tecnologias

- **Backend**: Python, Flask, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Matplotlib
- **Armazenamento**: JSON (arquivos) + Cookies
- **Deploy**: Gunicorn, Nginx, Ubuntu

## 📦 Instalação Local

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/Pedrohsre/cronometro-atividades.git
cd cronometro-atividades
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python app.py
```

5. **Acesse no navegador**
```
http://localhost:5000
```

## 🌐 Deploy em Produção (Oracle Cloud Ubuntu)

### Deploy Automatizado

1. **Conecte-se à sua VM Ubuntu**
```bash
ssh ubuntu@SEU_IP_PUBLICO
```

2. **Execute o script de deploy**
```bash
wget https://raw.githubusercontent.com/Pedrohsre/cronometro-atividades/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### Deploy Manual

1. **Instalar dependências do sistema**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git nginx ufw
```

2. **Clonar repositório**
```bash
cd /home/ubuntu
git clone https://github.com/Pedrohsre/cronometro-atividades.git
cd cronometro-atividades
```

3. **Configurar Python**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configurar Nginx**
```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/cronometro
sudo ln -sf /etc/nginx/sites-available/cronometro /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl reload nginx
```

5. **Configurar systemd**
```bash
sudo cp deploy/cronometro.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cronometro
sudo systemctl start cronometro
```

6. **Configurar firewall**
```bash
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
```

## 🔧 Gerenciamento

### Comandos úteis

- **Ver logs**: `sudo journalctl -u cronometro -f`
- **Reiniciar aplicação**: `sudo systemctl restart cronometro`
- **Ver status**: `sudo systemctl status cronometro`
- **Atualizar código**: 
  ```bash
  cd /home/ubuntu/cronometro-atividades
  git pull origin main
  sudo systemctl restart cronometro
  ```

### Estrutura de Arquivos

```
cronometro-atividades/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── gunicorn_config.py    # Configuração do Gunicorn
├── deploy.sh             # Script de deploy automatizado
├── templates/            # Templates HTML
│   ├── index.html        # Página principal
│   ├── login.html        # Página de login
│   └── register.html     # Página de registro
├── users.json           # Database de usuários
└── atividades_data_*.json # Dados dos usuários
```

## 🔒 Segurança

- Senhas são hasheadas com Werkzeug
- Session cookies seguros
- Firewall configurado automaticamente
- Nginx como proxy reverso

## 🐛 Solução de Problemas

### Aplicação não inicia
```bash
sudo journalctl -u cronometro --no-pager
```

### Nginx com erro
```bash
sudo nginx -t
sudo systemctl status nginx
```

### Porta 5000 já em uso
```bash
sudo lsof -i :5000
sudo systemctl restart cronometro
```

## 📈 Atualizações

Para manter o sistema atualizado:

```bash
cd /home/ubuntu/cronometro-atividades
git pull origin main
sudo systemctl restart cronometro
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✨ Autor

Desenvolvido por [Pedrohsre](https://github.com/Pedrohsre)

---

🌟 **Se este projeto foi útil para você, deixe uma estrela!** 🌟
