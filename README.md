# To-Do List API

Uma API REST profissional para gerenciamento de tarefas (To-Do List) construída com FastAPI.

## Características

- **Versão 1**: Armazenamento em memória (lista Python)
- API REST completa com FastAPI
- Validação de dados com Pydantic
- Testes automatizados com Pytest
- Documentação interativa automática (Swagger/OpenAPI)

## Modelo de Dados

### Task
- `id` (int): Identificador único
- `title` (str): Título da tarefa
- `description` (str, opcional): Descrição detalhada
- `done` (bool): Status de conclusão (padrão: false)
- `created_at` (datetime): Data e hora de criação

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/tasks` | Criar nova tarefa |
| GET | `/tasks` | Listar todas as tarefas |
| GET | `/tasks/{id}` | Obter tarefa específica |
| PUT | `/tasks/{id}` | Atualizar tarefa |
| DELETE | `/tasks/{id}` | Remover tarefa |

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar dependências de desenvolvimento (para testes)
pip install -r requirements-dev.txt
```

## Executando a API

```bash
# Iniciar o servidor
uvicorn main:app --reload

# O servidor estará disponível em http://localhost:8000
```

## Documentação Interativa

Após iniciar o servidor, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Exemplos de Uso

### Criar uma tarefa
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar leite", "description": "Ir ao supermercado"}'
```

### Listar todas as tarefas
```bash
curl http://localhost:8000/tasks
```

### Obter uma tarefa específica
```bash
curl http://localhost:8000/tasks/1
```

### Atualizar uma tarefa
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

### Deletar uma tarefa
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Testes

```bash
# Executar todos os testes
pytest test_main.py -v

# Executar com cobertura
pytest test_main.py --cov=main
```

## Estrutura do Projeto

```
to-do-list0/
├── main.py                 # Aplicação FastAPI principal
├── test_main.py           # Testes automatizados
├── requirements.txt       # Dependências de produção
├── requirements-dev.txt   # Dependências de desenvolvimento
└── README.md             # Documentação
```

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI
- **Pytest**: Framework de testes