# 🖥️ Personal Portfolio Backend (Django + DRF)

This repository contains the backend of my **personal portfolio**, built with **Django REST Framework (DRF)** and designed as a reference implementation of **modern backend best practices**.  

It serves as both:
1. The backend powering my personal portfolio website.
2. An **open-source example project** for recruiters, engineers, and contributors interested in clean DRF design patterns.

---

## 🚀 Features

- **Content Management via Django Admin**:
  - Blog posts
  - Work experiences
  - Education
  - Skills
  - Projects
  - GitHub repositories (fetched automatically)
  - Courses
  - Resume page
  - Gallery
  - About section
  - Contact me (with email integration and Telegram messaging)

- **Backend Stack**:
  - **Django 5 + DRF** — core backend & API
  - **PostgreSQL** — relational database
  - **Redis** — cache & Celery broker
  - **Celery + Celery Beat + Celery Results** — async tasks & scheduling
  - **django-cors-headers** — secure CORS management
  - **Gunicorn** — production WSGI server
  - **Nginx** — reverse proxy & static/media server
  - **Docker Compose** — containerized services

- **Developer Experience**:
  - **Taskfile** — automate common dev tasks (migrations, tests, lint, etc.)
  - **GitHub Actions** — CI/CD pipeline
  - **Best Practices** — modular apps, clean serializers, typed code, environment configs

---

## 📐 Architecture (corrected)
```
Client (Browser)  -->  Nginx (edge: TLS, routing, static)  
    ├─ /  & /_next/*  --> Next.js (Node SSR/SSG container)
    ├─ /api/*         --> Django + Gunicorn (backend container)
    ├─ /admin/*       --> Django Admin (protected)
    └─ /flower/*      --> Celery Flower (protected, optional)

Backend (Django)  --> Postgres (DB) & Redis (cache + Celery broker)  
Celery workers & beat access Redis and Postgres internally (not exposed).
Static/media can be served by Nginx or hosted on S3/CDN.
```

## 🛠️ Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Taskfile (optional but recommended)
- Python 3.12+ (for local development)

### Quickstart (Docker Compose)
```bash
# Clone repository
git clone git@github.com:osmanmakhtoom/portfolio_backend.git
cd portfolio_backend

# Copy environment template and adjust values
cp .env.example .env

# Run services
docker compose up --build
```

The backend will be available at:  
`http://localhost:8000/api/v1/`

---

## ⚡ Development Workflow

### Using Taskfile
```bash
# Run migrations
task migrate

# Create superuser
task createsuperuser

# Run tests
task test

# Lint & format
task lint

# Run
task run
```

### Without Taskfile
```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

---

## 🧩 API Endpoints (Planned)

- `/api/v1/blog/`
- `/api/v1/experiences/`
- `/api/v1/education/`
- `/api/v1/skills/`
- `/api/v1/projects/`
- `/api/v1/github-repos/`
- `/api/v1/courses/`
- `/api/v1/gallery/`
- `/api/v1/about/`
- `/api/v1/resume/`
- `/api/v1/contact/`

All endpoints are designed with:
- Pagination
- Filtering & ordering
- Serializer layers for clean separation
- Caching for high-traffic data (projects, repos)

---

## 🔄 Background Tasks

Celery workers handle:
- Contact form email delivery
- Fetching GitHub repositories periodically
- Scheduled maintenance tasks
- Async heavy operations (e.g., generating resume PDFs)

---

## 🛡️ Security & Best Practices

- Environment-based settings (`.env`)
- CORS controlled via **django-cors-headers**
- Strict separation of dev/stage/prod configs
- Dockerized deployment with Gunicorn + Nginx
- GitHub Actions CI/CD (linting, testing, deployment)

---

## 📦 Deployment

Production stack is managed with **Docker Compose**:
- **Nginx** — reverse proxy & static files
- **Gunicorn** — Django app server
- **PostgreSQL + Redis** — data persistence
- **Celery workers + beat** — background jobs

Example production run:
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

---

## 🧑‍💻 Contribution

This project is **open source** to showcase **DRF best practices**.  
Feel free to fork, explore, and contribute improvements.

1. Fork repo
2. Create feature branch (`git checkout -b feature/awesome`)
3. Commit changes
4. Push branch & open PR

---

## 🧰 Tools & Packages Used

### Core Backend
- [Django 5](https://www.djangoproject.com/) — web framework
- [Django REST Framework](https://www.django-rest-framework.org/) — API framework
- [django-environ](https://github.com/joke2k/django-environ) — environment variable management
- [psycopg3](https://www.psycopg.org/) — PostgreSQL driver
- [Redis](https://redis.io/) — caching & Celery broker

### Asynchronous Tasks & Scheduling
- [Celery](https://docs.celeryq.dev/) — async task queue
- [django-celery-beat](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#beat) — periodic task scheduling
- [django-celery-results](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#results-backend) — task result backend

### Authentication & Security
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/) — JWT authentication
- [django-allauth](https://django-allauth.readthedocs.io/) — social login / OAuth
- [django-cors-headers](https://github.com/adamchainz/django-cors-headers) — manage CORS

### Admin & Content Management
- [django-prose-editor](https://django-prose-editor.readthedocs.io/) — rich text editing
- [drf-yasg](https://drf-yasg.readthedocs.io/) — Swagger / OpenAPI documentation
- [django-filter](https://django-filter.readthedocs.io/) — filtering support for APIs

### Media, Files & Analytics
- [Pillow](https://python-pillow.org/) — image handling
- [XlsxWriter](https://xlsxwriter.readthedocs.io/) — Excel file generation
- [MinIO](https://min.io/) — S3-compatible object storage
- [DuckDB](https://duckdb.org/) + [Fireducks](https://github.com/fireducks) — analytics & reporting

### Utilities & Dev Tools
- [Markdown](https://python-markdown.github.io/) — Markdown support
- [simple-ulid](https://github.com/simple-ulid/simple-ulid) — ULID identifiers
- [django-phonenumber-field](https://github.com/stefanfoulis/django-phonenumber-field) — phone number validation
- [pytimeparse](https://pypi.org/project/pytimeparse/) — parse durations
- [Ruff](https://github.com/charliermarsh/ruff) — linter
- [mypy](http://mypy-lang.org/) — static type checking
- [IPython](https://ipython.org/) — interactive development shell
- [pytest-django](https://pytest-django.readthedocs.io/) + [pytest-cov](https://pytest-cov.readthedocs.io/) + [coverage](https://coverage.readthedocs.io/) — testing & coverage

### Deployment & Infrastructure
- [Docker Compose](https://docs.docker.com/compose/) — container orchestration
- [Taskfile](https://taskfile.dev/) — automate routine dev tasks
- [GitHub Actions](https://docs.github.com/en/actions) — CI/CD pipelines
- [Gunicorn](https://gunicorn.org/) — WSGI server
- [Nginx](https://www.nginx.com/) — reverse proxy, TLS, static/media serving
- [Sentry SDK](https://docs.sentry.io/platforms/python/django/) — error monitoring

---

## 📄 License
MIT License — you can use this project freely as a reference or starting point.

---

## 📌 Notes for Recruiters

This project is more than just a portfolio backend:  
- It demonstrates **real-world Django/DRF architecture**.  
- It includes **CI/CD, Docker, async tasks, caching, and modular design**.  
- It shows my approach to **clean, scalable, production-ready code**.  

If you’d like to see the **frontend (Next.js)** that consumes this API, check here:  
👉 [Frontend Repository (coming soon)](https://github.com/osmanmakhtoom/portfolio_frontend)

---
