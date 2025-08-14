# ⏱️ Cronômetro de Atividades

Uma aplicação web desenvolvida em Flask para controlar o tempo gasto em diferentes atividades usando um cronômetro interativo, com **sistema de login individual** para cada usuário.

## 🎯 Funcionalidades

- **🔐 Sistema de Login**: Cada usuário tem sua própria conta e dados
- **⏱️ Cronômetro Completo**: Iniciar, pausar, parar e resetar
- **⏰ Tempo Manual**: Adicionar horas, minutos e segundos manualmente
- **⚡ Atalhos Rápidos**: Botões para adicionar +50min, +30min, +15min, +5min
- **📝 Gerenciamento de Atividades**: Criar, remover e adicionar tempo às atividades
- **📊 Visualização**: Gráfico de pizza da distribuição de tempo
- **💾 Persistência Individual**: Cada usuário tem seu próprio arquivo JSON de dados
- **📱 Interface Responsiva**: Funciona em desktop e mobile

## 🔐 Sistema de Usuários

### Funcionalidades de Login:
- **Registro**: Criação de conta com usuário e senha
- **Login Seguro**: Senhas criptografadas com Werkzeug
- **Dados Isolados**: Cada usuário tem suas próprias atividades
- **Sessão Persistente**: Mantém login até fazer logout

### Arquivos por Usuário:
- `atividades_data_USUARIO.json` - Dados individuais de cada usuário
- `users.json` - Banco de dados de usuários (senhas criptografadas)

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Matplotlib
- **Persistência**: JSON
