# Gerador de Ideias de Conteúdo

Aplicativo web para gerar ideias de conteúdo para redes sociais a partir de um tema.

## Funcionalidades

- **Cadastro e Login** com nome, e-mail e senha (banco SQLite local)
- **Geração de ideias** organizadas em:
  - Sugestões de Títulos
  - Ganchos (Hooks) para os primeiros 3 segundos
  - Ideias de Call to Action
  - Ideias de Descrição
- **Botão Copiar** em cada ideia
- **Histórico** de temas pesquisados com possibilidade de visualizar e excluir

## Como rodar

```bash
cd gerador-ideias
python3 app.py
```

Acesse: http://localhost:5000

## Requisitos

- Python 3.8+
- Flask, Flask-SQLAlchemy, Werkzeug

Instale com:
```bash
pip install flask flask-sqlalchemy werkzeug
```

## Estrutura

```
gerador-ideias/
├── app.py              # Backend Flask
├── templates/          # HTML
├── static/css/         # Estilos
├── static/js/          # Scripts
└── gerador.db          # Banco SQLite (criado automaticamente)
```
