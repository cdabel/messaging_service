# Messaging Service (API Project)

This project implements a simplified messaging service that mimics key functionality from an agentic AI platform.

It supports:

- Sending outbound messages to a mock provider
- Persisting messages to a PostgreSQL database
- Handling provider-side errors and retries, including HTTP 429 rate limits
- FastAPI-based routing and schema validation

---

## Tech Stack

- FastAPI for the API layer
- Pydantic for data validation
- SQLAlchemy for database modeling and persistence
- PostgreSQL as the relational store
- httpx for async provider communication
- Tenacity for retry logic

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/messaging-service.git
cd messaging-service
```

### 2. Create a `.env` File

```env
DATABASE_URL=postgresql://<redacted>:<redacted>@localhost:5432/messaging
```

Refer to `.env.example` if needed.

### 3. Set Up PostgreSQL

**Option A: Native**

```bash
sudo service postgresql start
sudo -u postgres psql
# Then in psql:
CREATE USER <redacted> WITH PASSWORD '<redacted>';
CREATE DATABASE messaging;
GRANT ALL PRIVILEGES ON DATABASE messaging TO <redacted>;
```

**Option B: Docker**

```bash
docker run --name messaging-proj-postgres \
  -e POSTGRES_USER=hatch \
  -e POSTGRES_PASSWORD=<redacted> \
  -e POSTGRES_DB=messaging \
  -p 5432:5432 \
  -d postgres:15
```

### 4. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

### 6. Test the Flow

```bash
curl -X POST http://localhost:8000/messages/send \
  -H "Content-Type: application/json" \
  -d '{
    "from_": "+11234567890",
    "to": "+10987654321",
    "type": "sms",
    "body": "Test message",
    "attachments": [],
    "timestamp": "2025-05-21T18:00:00Z"
  }'
```

---

## Assumptions and Design Decisions

- Provider URL is assumed to be a mock endpoint. Retries are implemented using Tenacity, and error responses are handled gracefully.
- Conversations were mentioned in the prompt but no grouping logic was defined. This was intentionally deferred and noted in the code for follow-up.
- The database schema is created on startup using `create_tables()` for simplicity in development. We'd use Alembic to productionize a schema migration.git 
- Environment configuration is loaded via `python-dotenv` using a `.env` file.
- The application is written with production extensibility in mind, but focused on delivery of core functionality under time constraints.

---

## Potential Improvements

If extended or taken to production:

- Implement conversation grouping logic based on contact history and timestamps
- Add read endpoints for retrieving messages and conversations
- Switch to Alembic for schema migrations
- Use FastAPI’s `Depends` system for scoped DB sessions
- Add Pytest-based unit and integration tests
- Include Docker Compose to streamline local dev setup
