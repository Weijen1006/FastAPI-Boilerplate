# FastAPI Template

This repository is a lightweight FastAPI starter organized around clear layers for routing, authentication, middleware, models, and configuration. It already includes several production-friendly building blocks such as centralized exception handling, request logging, JWT helpers, environment-based settings, and role-based authorization.


## Folder Structure

```text
FastAPI Template/
|-- auth/
|   `-- auth_handler.py
|-- configs/
|   |-- constants.py
|   |-- database.py
|   `-- settings.py
|-- controllers/
|   |-- admin/
|   |   |-- auth.py
|   |   |-- items.py
|   |   `-- users.py
|   `-- public/
|       `-- responses.py
|-- middlewares/
|   |-- auth_handler.py
|   |-- exceptions.py
|   `-- request_logger.py
|-- models/
|   |-- auth.py
|   |-- exception.py
|   |-- item.py
|   |-- request_logger.py
|   |-- response.py
|   |-- sample_data.py
|   `-- user.py
|-- services/
|   `-- item_service.py
|-- tests/
|   |-- e2e/
|   |   `-- test_placeholder.py
|   |-- integration/
|   |   `-- test_placeholder.py
|   `-- unit/
|       `-- test_placeholder.py
|-- utils/
|   `-- logger.py
|-- .env
|-- .gitignore
|-- main.py
|-- README.md
`-- requirements.txt
```

## Layer Responsibilities

### `main.py`

- Creates the FastAPI application
- Registers middleware
- Registers custom exception handlers
- Exposes root, health, and info endpoints
- Mounts the versioned routers using `API_PREFIX`

### `configs/`

- `settings.py` loads environment variables using `python-dotenv`
- Stores runtime configuration such as app name, port, JWT settings, API prefix, log limits, and role hierarchy
- `database.py` creates the SQLAlchemy engine, session factory, declarative base, and FastAPI dependency for per-request database sessions
- `constants.py` keeps reusable error message enums

### `controllers/`

- `admin/auth.py` provides the login endpoint and returns a JWT for a mock authenticated user
- `admin/users.py` returns the current authenticated user
- `admin/items.py` provides protected item endpoints and delegates business logic to the item service
- `public/responses.py` demonstrates success, custom error, HTTP error, and unexpected error flows

### `services/`

- `item_service.py` holds the item business logic and receives a SQLAlchemy session from the controller layer

### `auth/`

- Encodes JWT tokens with expiration
- Decodes and verifies JWT tokens
- Extracts the current user from the bearer token
- Contains basic role helper functions

### `middlewares/`

- `request_logger.py` logs inbound requests, request IDs, timing, request bodies, and response payloads
- `exceptions.py` converts application, HTTP, validation, and unexpected exceptions into a consistent JSON response shape
- `auth_handler.py` provides a reusable `with_role()` decorator for role-based access control

### `models/`

- `auth.py` defines the login request schema
- `item.py` defines the item payload schema
- `user.py` defines the authenticated user schema and role enum
- `response.py` defines the standard success and error response contracts
- `exception.py` defines the custom application exception type
- `request_logger.py` defines the structured log model
- `sample_data.py` provides static sample response data used by the public demo endpoints

### `tests/`

- `unit/` is for isolated tests around services, helpers, and business logic
- `integration/` is for tests that cover module and database interactions
- `e2e/` is for full request-flow and API behavior tests

### `utils/`

- `logger.py` centralizes logger creation and console formatting

## Request Flow

1. A request enters the app through FastAPI in `main.py`.
2. The logging middleware in `middlewares/request_logger.py` assigns a request ID, captures request data, and measures execution time.
3. If the route requires authentication, FastAPI resolves `Depends(get_current_user)` from `auth/auth_handler.py`.
4. If the route also uses `@with_role(...)`, the decorator in `middlewares/auth_handler.py` checks the user role hierarchy.
5. The controller delegates business logic to a service when needed and returns `APISuccessResponse` or raises an exception.
6. Custom handlers in `middlewares/exceptions.py` convert failures into a standard error payload.
7. The logging middleware writes a structured request/response log entry before the response leaves the app.

## API Endpoints

### General

- `GET /` returns a hello-world payload
- `GET /health` returns a simple health status
- `GET /info` returns the app name and API prefix

### Auth

- `POST /v1/auth/` accepts `AuthLoginRequest` and returns a JWT token inside `APISuccessResponse`

Current behavior:
- Authentication is mocked
- The returned token always contains an admin role
- No database, password validation, refresh token flow, or identity provider integration is implemented yet

### Users

- `GET /v1/users/me` returns the authenticated user extracted from the JWT

### Items

- `POST /v1/admin/items` requires an authenticated user with `super_admin` role
- `GET /v1/admin/items/{item_id}` requires an authenticated user and returns a simple sample payload

### Public Demo Responses

- `GET /v1/public/responses/api_success`
- `GET /v1/public/responses/api_error`
- `GET /v1/public/responses/http_error`
- `GET /v1/public/responses/other_error`

These routes are useful for testing response envelopes, logging behavior, and exception handling.

## Environment Variables

The application reads configuration from `.env` through `configs/settings.py`.

Supported variables:

- `APP_NAME`: display name returned by `/info`
- `APP_PORT`: port for local startup
- `IS_DEBUG`: enables reload behavior when truthy
- `API_PREFIX`: version prefix for routers, default `/v1`
- `APP_DB_CONNECTION_STRING`: SQLAlchemy connection string used by the shared database engine
- `JWT_SECRET_KEY`: secret used to sign JWT tokens
- `JWT_ALGORITHM`: JWT algorithm, default `HS256`
- `JWT_EXPIRED_IN_SECOND`: token expiration window in seconds

Example:

```env
APP_NAME=FastAPI Template
APP_PORT=8000
IS_DEBUG=1
API_PREFIX=/v1
APP_DB_CONNECTION_STRING=sqlite:///./app.db
JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
JWT_EXPIRED_IN_SECOND=3600
```

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Alternative:

```bash
uvicorn main:app --reload
```

After startup:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Production-Friendly Practices Already Present

- Separation of concerns across configs, controllers, services, middlewares, auth, models, and utilities
- Thin-controller pattern where request handling stays in routers and business logic moves into services
- Versioned API routing through `API_PREFIX`
- Centralized exception handling instead of ad hoc error payloads in controllers
- Standardized success and error response models
- Request correlation using a generated `request_id`
- Execution-time logging for observability
- Environment-variable based runtime configuration
- Centralized SQLAlchemy engine and per-request session dependency
- JWT-based authentication helper functions
- Role hierarchy support for authorization
- Health and info endpoints for operational checks
- Git ignore rules that exclude caches, virtual environments, editor files, logs, and `.env`

## Notes

This repository should be used as a quick-start template, not as a complete production application. To turn it into a fully production-ready FastAPI app, you should still add the following pieces:

- Real authentication is not implemented yet. The login endpoint returns a mock token without credential validation.
- A shared database session layer now exists, but there are still no ORM models, repositories, or migrations wired into application features yet.
- CI, linting, formatting, and type-checking are not configured.
- The service layer has started with `item_service.py`, but repositories and richer domain services still need to be added.
- No deployment assets are included, such as Docker, process manager config, or reverse-proxy guidance.
- Authorization depends entirely on JWT contents. For a real system, permissions should usually be revalidated from a trusted source such as a database or cache.
