NB / my .env is here 
# AI-Based Resume Screening Recruitment Platform

This project implements an AI-powered resume screening recruitment platform leveraging Django, Django REST Framework, GraphQL, Celery, and edge computing capabilities via Fly.io. The architecture supports low-latency applications by intelligently routing requests to the optimal edge node, with advanced security and scalable deployment features.

## Deployed Application

- **Production URL:** [https://ai-based-resume-screening-recruitment.fly.dev](https://ai-based-resume-screening-recruitment.fly.dev)
- **Base URL:** `https://ai-based-resume-screening-recruitment.fly.dev/api/`

---

## Features

1. **Edge Computing with Django for Low-Latency Applications**
    - **Models:**
        - `EdgeNode`: Represents an edge server with location (latitude, longitude).
        - `APIRequestLog`: Logs API requests with location data.
    - **Validation:** Enforces valid latitude/longitude using Django model validators.
    - **Serializers & GraphQL Types:** For edge node registration and health checks.
    - **REST API Endpoints:**
        - Register edge nodes (`/api/edge/register/`)
        - Route requests to optimal edge node (`/api/edge/route/`)
    - **GraphQL Queries:** Monitor node performance metrics.
    - **Security:** Mutual TLS and API key-based authentication for edge communications.
    - **Celery Tasks:** 
        - Automated code deployment to edge platforms (Fly.io) via API.
        - AI-based routing decisions to predict the optimal edge node for each request.
    - **Monitoring & Health Checks:** Exposed via both REST and GraphQL.

---

## Usage

### Environment Variables

Add the following to your `.env` file (do **not** commit this file to public repos):

```env
SECRET_KEY='django-insecure-7obc$(lqz9=kd#)!-8o4a7=0z#0=8o*-qg2wxa14a8)5czge-&'
DATABASE_URL='postgres://postgres:nNYoJRRCNyvyJik@recruitment-db.flycast:5432/postgres'
DEBUG=True
CSRF_TRUSTED_ORIGINS=https://ai-based-resume-screening-recruitment.fly.dev,localhost,127.0.0.1
FLY_API_TOKEN="FlyV1 fm2_lJPECAAAAAAACJWPxBCo1n7MrSOOFeUAawGc/Lm/wrVodHRwczovL2FwaS5mbHkuaW8vdjGWAJLOABALph8Lk7lodHRwczovL2FwaS5mbHkuaW8vYWFhL3YxxDym3WPD2iu0SPKNr8l2FvhErafzV3MIeYFu020OQ3XKCpRU2HqCqJl1evRZUlAbC7oPfNEjv4NCZLIOZBrETv+KbPVrnFAnCfEDGUKOutUA2gd2gdaqhaC12sjN1n6zs3v9s0KjzLAUJD0OIOy4v8QXKf5ttZpGYSKSJb+FrFhg1yVnlcCFOuA3OPkT9A2SlAORgc4AcEbPHwWRgqdidWlsZGVyH6J3Zx8BxCDbHQiRsL+Jz5bnaS0A2C6PAeA1cdJ1i5lL6yOoubaXpg==,fm2_lJPETv+KbPVrnFAnCfEDGUKOutUA2gd2gdaqhaC12sjN1n6zs3v9s0KjzLAUJD0OIOy4v8QXKf5ttZpGYSKSJb+FrFhg1yVnlcCFOuA3OPkT9MQQSmg/om2mPemCEP2E22AR3cO5aHR0cHM6Ly9hcGkuZmx5LmlvL2FhYS92MZgEks5oPkS7zwAAAAEkNmLZF84AD2zWCpHOAA9s1gzEEMvMOXoRGNOri7vrhFXM7Z3EICDAyQqQw7j4H11s0l5vbHdbMNZDrjsWCb96a96KAbAI"
FLY_APP_NAME=ai-based-resume-screening-recruitment-master
ALLOWED_HOSTS=ai-based-resume-screening-recruitment-master.fly.dev,localhost,127.0.0.1
X-CSRFToken=29dpNrWIbKFF1G1g1VSqK4kajVPLvzWG
```

---

### API Overview

#### REST Endpoints

- **Edge Node Registration:**  
  `POST /api/edge/register/`  
  Registers a new edge node. Payload includes location and authentication info.

- **Edge Node Routing:**  
  `POST /api/edge/route/`  
  Finds and returns the optimal edge node for a given request.

- **Health Check:**  
  `GET /api/edge/health/`  
  Returns the health status of edge nodes.

#### GraphQL

- **Monitor Node Performance:**  
  `POST /graphql/`  
  Query example:
  ```graphql
  {
    edgeNodes {
      id
      location
      status
      lastHealthCheck
      requestsHandled
    }
  }
  ```

---

### Celery Tasks

- **Automated Deployment:**  
  Deploys latest code to available edge platforms (Fly.io) using the Fly API.

- **AI-Based Routing:**  
  Predicts and routes requests to the optimal edge node based on real-time metrics.

---

### Security

- **Mutual TLS:** All edge communications use TLS with client certificates.
- **API Key Authentication:** Register and use API keys for secure access to endpoints.
- **CSRF Protection:**  
  Add your domain to `CSRF_TRUSTED_ORIGINS` in `.env`.

---

## Project Structure

- **models.py**: Contains `EdgeNode`, `APIRequestLog`, and other core models.
- **serializers.py**: DRF serializers for model validation and data transfer.
- **schema.py**: GraphQL types and queries.
- **views.py**: All view logic for REST endpoints.
- **tasks.py**: Celery tasks for deployment and AI-based routing.
- **settings.py**: Django settings, including `.env` integration.
- **Dockerfile**: For containerized deployment.

---

## How to Run Locally

1. **Clone the repository**
    ```bash
    git clone https://github.com/sassikoussai/project-django.git
    cd project-django
    ```

2. **Create and activate a virtualenv**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your `.env` file** (see above)

5. **Run migrations**
    ```bash
    python manage.py migrate
    ```

6. **Run the server**
    ```bash
    python manage.py runserver
    ```

---

## Usage of All Views

- All views (REST and GraphQL) are documented via [DRF's browsable API](https://ai-based-resume-screening-recruitment.fly.dev/api/) and the `/graphql/` endpoint.
- For custom endpoints or specific usage, see docstrings in `views.py`.

---

## Deployment

- **Platform:** [Fly.io](https://fly.io)
- **App Name:** `ai-based-resume-screening-recruitment-master`
- **Deployments triggered via Celery tasks and Fly API integration.**

---

## License

This project is licensed under the MIT License.

---

## Maintainer

- [sassikoussai](https://github.com/sassikoussai)
