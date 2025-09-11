# 🖥️ Personal Portfolio Backend (Django + DRF)

This repository contains the backend of my **personal portfolio**, built with **Django REST Framework (DRF)** and designed as a reference implementation of **modern backend best practices**.

It serves as both:

1. The backend powering my personal portfolio website.  
2. An **open-source example project** for recruiters, engineers, and contributors interested in clean DRF design patterns.

---

## 🚀 Features

* **Content Management via Django Admin**:
  * User accounts
  * Blog posts
  * Work experiences
  * Education
  * Skills
  * Projects
  * GitHub repositories (fetched automatically)
  * Courses
  * Resume page
  * Gallery
  * About section
  * Contact me (with email integration and Telegram messaging)

* **Backend Stack**:
  * **Django 5 + DRF** — core backend & API
  * **PostgreSQL** — relational database
  * **Redis** — cache & Celery broker
  * **Celery + Celery Beat + Celery Results** — async tasks & scheduling
  * **django-cors-headers** — secure CORS management
  * **Gunicorn** — production WSGI server
  * **Nginx** — reverse proxy & static/media server
  * **Docker Compose** — containerized services

* **Developer Experience**:
  * **Taskfile** — automate common dev tasks (migrations, tests, lint, etc.)
  * **GitHub Actions** — CI/CD pipeline
  * **Best Practices** — modular apps, clean serializers, typed code, environment configs
  * **Sentry** — error monitoring and performance tracking

---

## 📐 Architecture

```
Client (Browser)  -->  Nginx (edge: TLS, routing, static)  
├─ /  & /_next/* --> Next.js (Node SSR/SSG container)
├─ /api/*        --> Django + Gunicorn (backend container)
├─ /admin/*      --> Django Admin (protected)
└─ /flower/*     --> Celery Flower (protected, optional)

Backend (Django)  --> Postgres (DB) & Redis (cache + Celery broker)  
Celery workers & beat access Redis and Postgres internally (not exposed).
Static/media can be served by Nginx or hosted on S3/CDN.
```

---

## 🛠️ Installation & Setup

### Prerequisites

* Docker & Docker Compose  
* Taskfile (optional but recommended)  
* Python 3.12+ (for local development)  

---

### Quickstart (Docker Compose)

<details>
<summary>📥 Setup & Run</summary>

```bash
# Clone repository
git clone git@github.com:osmanmakhtoom/portfolio_backend.git
cd portfolio_backend

# Copy environment template and adjust values
cp .env.example .env

# Run services
docker compose up --build
```

</details>

Backend available at: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)

---

## ⚡ Development Workflow

### Using Taskfile

<details>
<summary>🛠 Taskfile Commands</summary>

```bash
# Start Docker services
task up

# Run migrations
task migrate

# Create database migrations
task make_migrations

# Create a superuser
task createsuperuser

# Run tests (with 80% coverage check)
task test

# Lint & format code
task clean

# Run development server
task run

# Stop and remove Docker services
task down
```
</details>

---

### Without Taskfile

<details>
<summary>⚙️ Django Management Commands</summary>

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py createsuperuser
```
</details>

---

## 🧩 API Endpoints (Planned)

* `/api/v1/account/` (Implemented & Tested)  
* `/api/v1/blog/`  
* `/api/v1/experiences/`  
* `/api/v1/education/`  
* `/api/v1/skills/`  
* `/api/v1/projects/`  
* `/api/v1/github-repos/`  
* `/api/v1/courses/`  
* `/api/v1/gallery/`  
* `/api/v1/about/`  
* `/api/v1/resume/`  
* `/api/v1/contact/`

All endpoints are designed with:

* Pagination  
* Filtering & ordering  
* Serializer layers for clean separation  
* Caching for high-traffic data (projects, repos)  

---

## 🔄 Background Tasks

Celery workers handle:

* Contact form email delivery  
* Fetching GitHub repositories periodically  
* Scheduled maintenance tasks  
* Async heavy operations (e.g., generating resume PDFs)  

---

## 🛡️ Security & Best Practices

* Environment-based settings (`.env`)  
* CORS controlled via **django-cors-headers**  
* Strict separation of dev/stage/prod configs  
* Dockerized deployment with Gunicorn + Nginx  
* GitHub Actions CI/CD (linting, testing, deployment)  
* Sentry for error tracking and performance monitoring  

---

## 📦 Deployment

Production stack is managed with **Docker Compose**:

* **Nginx** — reverse proxy & static files  
* **Gunicorn** — Django app server  
* **PostgreSQL + Redis** — data persistence  
* **Celery workers + beat** — background jobs  
* **S3 / MinIO** — media storage (via `django-storages` and `boto3`)  

<details>
<summary>🚀 Production Run</summary>

```bash
docker compose -f docker-compose.yml up -d --build
```

Or simply run:
```bash
task up
```
</details>

---

## 🧑‍💻 Contribution

This project is **open source** to showcase **DRF best practices**.  
Feel free to fork, explore, and contribute improvements.

1. Fork repo  
2. Create feature branch:  
   ```bash
   git checkout -b feat/awesome
   ```
3. Commit changes  
4. Push branch & open PR  

---

## 🧰 Tools & Packages Used

### Core Backend
* [Django](https://pypi.org/project/Django/)  
* [Django REST Framework](https://pypi.org/project/djangorestframework/)  
* [django-environ](https://pypi.org/project/django-environ/)  
* [psycopg](https://pypi.org/project/psycopg/)  
* [redis](https://pypi.org/project/redis/)  

### Asynchronous Tasks & Scheduling
* [Celery](https://pypi.org/project/celery/)  
* [django-celery-beat](https://pypi.org/project/django-celery-beat/)  
* [django-celery-results](https://pypi.org/project/django-celery-results/)  

### Authentication & Security
* [djangorestframework-simplejwt](https://pypi.org/project/djangorestframework-simplejwt/)  
* [django-allauth](https://pypi.org/project/django-allauth/)  
* [django-cors-headers](https://pypi.org/project/django-cors-headers/)  
* [sentry-sdk](https://pypi.org/project/sentry-sdk/)  

### Admin & Content Management
* [django-prose-editor](https://pypi.org/project/django-prose-editor/)  
* [drf-yasg](https://pypi.org/project/drf-yasg/)  
* [django-filter](https://pypi.org/project/django-filter/)  

### Media & Files
* [Pillow](https://pypi.org/project/Pillow/)  
* [XlsxWriter](https://pypi.org/project/XlsxWriter/)  
* [django-storages](https://pypi.org/project/django-storages/)  
* [boto3](https://pypi.org/project/boto3/)  
* [minio](https://pypi.org/project/minio/)  

### Utilities & Dev Tools
* [Markdown](https://pypi.org/project/Markdown/)  
* [simple-ulid](https://pypi.org/project/simple-ulid/)  
* [django-phonenumber-field](https://pypi.org/project/django-phonenumber-field/)  
* [pytimeparse](https://pypi.org/project/pytimeparse/)  
* [duckdb](https://pypi.org/project/duckdb/)  
* [ruff](https://pypi.org/project/ruff/)  
* [mypy](https://pypi.org/project/mypy/)  
* [ipython](https://pypi.org/project/ipython/)  
* [pytest-django](https://pypi.org/project/pytest-django/)  
* [pytest-cov](https://pypi.org/project/pytest-cov/)  
* [coverage](https://pypi.org/project/coverage/)  

### Deployment & Infrastructure
* Docker Compose  
* Taskfile  
* GitHub Actions  
* [Gunicorn](https://pypi.org/project/gunicorn/)  
* Nginx  

---

## 📄 License

MIT License — you can use this project freely as a reference or starting point.

---

## 📌 Notes for Recruiters

This project is more than just a portfolio backend:

* It demonstrates **real-world Django/DRF architecture**.  
* It includes **CI/CD, Docker, async tasks, caching, and modular design**.  
* It shows my approach to **clean, scalable, production-ready code**.  

👉 Frontend repo (Next.js, coming soon): [portfolio_frontend](https://github.com/osmanmakhtoom/portfolio_frontend)
