# ⏱️ Cronômetro de Atividades

Uma aplicação web desenvolvida em Flask para controlar o tempo gasto em diferentes atividades usando um cronômetro interativo.

## 🎯 Funcionalidades

- **⏱️ Cronômetro Completo**: Iniciar, pausar, parar e resetar
- **⏰ Tempo Manual**: Adicionar horas, minutos e segundos manualmente
- **⚡ Atalhos Rápidos**: Botões para adicionar +50min, +30min, +15min, +5min
- **📝 Gerenciamento de Atividades**: Criar, remover e adicionar tempo às atividades
- **📊 Visualização**: Gráfico de pizza da distribuição de tempo
- **💾 Persistência**: Dados salvos automaticamente em arquivo JSON
- **📱 Interface Responsiva**: Funciona em desktop e mobile

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- pip

### Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/SEU_USUARIO/cronometro-atividades.git
   cd cronometro-atividades
   ```

2. **Crie um ambiente virtual** (opcional, mas recomendado):
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**:
   ```bash
   python app.py
   ```

5. **Acesse no navegador**:
   ```
   http://localhost:5000
   ```

## 🎮 Como Usar

### Cronômetro
1. Use os botões **▶️ Iniciar**, **⏸️ Pausar**, **⏹️ Parar** e **🔄 Resetar**
2. O tempo é exibido no formato HH:MM:SS

### Tempo Manual
1. Digite valores nos campos de horas, minutos e segundos
2. Clique em **➕ Adicionar** para somar ao cronômetro
3. Use os atalhos rápidos para adicionar tempo instantaneamente

### Atividades
1. **Criar**: Digite o nome e clique em **🆕 Criar Atividade**
2. **Adicionar Tempo**: Selecione a atividade e clique em **➕ Adicionar Tempo**
3. **Remover**: Selecione a atividade e clique em **🗑️ Remover Atividade**

### Visualização
- Os cards mostram o total de horas por atividade
- O gráfico de pizza exibe a distribuição percentual do tempo

## 📁 Estrutura do Projeto

```
cronometro-atividades/
├── app.py                 # Aplicação Flask principal
├── templates/
│   └── index.html        # Interface web completa
├── atividades_data.json  # Dados persistidos (criado automaticamente)
├── requirements.txt      # Dependências Python
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Documentação
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Gráficos**: Matplotlib
- **Persistência**: JSON
- **Estilo**: CSS Grid, Flexbox, Design Responsivo

## 📊 Funcionalidades Técnicas

- **API RESTful**: Endpoints para gerenciar atividades
- **Auto-reload**: Flask em modo debug
- **Validação**: Inputs com limites e verificações
- **Feedback**: Mensagens de sucesso e erro
- **Responsivo**: Layout adaptável para diferentes telas

## 🎨 Interface

- **Design Moderno**: Gradientes e sombras
- **Cores Intuitivas**: Verde para iniciar, vermelho para parar
- **Ícones**: Emojis para melhor UX
- **Animações**: Transições suaves

## 🔧 Desenvolvimento

### Executar em modo desenvolvimento:
```bash
python app.py
```

A aplicação roda em `http://localhost:5000` com auto-reload ativo.

### Estrutura da API:
- `GET /` - Página principal
- `GET /api/atividades` - Lista todas as atividades
- `POST /api/nova_atividade` - Cria nova atividade
- `POST /api/adicionar_tempo` - Adiciona tempo a uma atividade
- `POST /api/remover_atividade` - Remove uma atividade
- `GET /api/grafico` - Obtém gráfico atualizado

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato

Pedro - [@seu_usuario](https://github.com/seu_usuario)

Link do Projeto: [https://github.com/seu_usuario/cronometro-atividades](https://github.com/seu_usuario/cronometro-atividades)
