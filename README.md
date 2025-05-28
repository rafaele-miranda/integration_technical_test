# Sistema de Integração TracOS ↔ Cliente

![Badge Django](https://img.shields.io/badge/Django-4.2-brightgreen)
![Badge SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)

Sistema de sincronização bidirecional de ordens de serviço entre o TracOS (sistema CMMS) e sistemas clientes, utilizando arquivos JSON para simulação de APIs.

## 📋 Funcionalidades

- **Fluxo Inbound (Cliente → TracOS)**
  - Processa arquivos JSON da pasta `data/inbound`
  - Valida e converte para formato TracOS
  - Armazena no banco de dados

- **Fluxo Outbound (TracOS → Cliente)**
  - Identifica ordens não sincronizadas
  - Gera arquivos JSON na pasta `data/outbound`
  - Atualiza status de sincronização

- **Tradução de Dados**
  - Conversão de formatos e status
  - Normalização de datas para UTC ISO 8601

## 🚀 Instalação

### Pré-requisitos
- Python 3.*

### Passo a Passo
1. Clone o repositório:
   ```
   git clone https://github.com/rafaele-miranda/integration_technical_test.git
   cd integration
   ```
2. Configure o ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```
4. Configure o banco de dados:
    ```
    python manage.py migrate
    ```
5. Crie um superusuário (opcional):
    ```
    python manage.py createsuperuser
    ```
6. Comando para processar arquivos de entrada:
    ```
    python manage.py process_inbound
    ```
    Exemplo de entrada (inbound):
    ``` 
    {
    "orderNo": 1,
    "isPending": true,
    "isOnHold": false,
    "isDone": false,
    "isCanceled": false,
    "summary": "Manutenção preventiva",
    "creationDate": "2025-05-26T08:00:00Z",
    "lastUpdateDate": "2025-05-26T08:30:00Z"
    }
    ```

8. Comando para iniciar servidor de desenvolvimento:
    ```
    python manage.py runserver
    ```
9. Acessar admin (após criar superusuário):
    ```
    http://localhost:8000/admin
    ```


   
