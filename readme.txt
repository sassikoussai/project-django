# Edge Computing with Django for Low-Latency Applications

A practical project demonstrating distributed edge node management, monitoring, and low-latency application deployment using Django, Celery, GraphQL, REST, and AI-based routing.

---

## 🚀 Features

### Practical Part

- **Edge Node Models:**  
  Define `EdgeNode` and `APIRequestLog` models with geolocation fields to represent distributed compute nodes and their API activity.

- **Location Field Validation:**  
  Enforce valid latitude/longitude values through custom Django model validators.

- **Serialization & GraphQL Integration:**  
  - Create DRF serializers for edge node registration and health checks.
  - Define GraphQL types for edge node data and health checks.

- **REST API Endpoints:**  
  - Register edge nodes via REST (DRF).
  - Route requests to nodes using RESTful endpoints.

- **GraphQL Monitoring:**  
  - GraphQL queries for live node performance and API request logs.

- **Secure Edge Communications:**  
  - API key authentication for edge node access.
  - Mutual TLS (mTLS) recommended—configure at your proxy or Fly.io platform layer.

- **Celery Task Orchestration:**  
  - Schedule Celery tasks to deploy code to edge platforms (like Fly.io) via their API.

- **AI-Based Routing:**  
  - Integrate a trained ML model to predict the optimal edge node for each deployment or request.
  - Use predictions within Celery deployment tasks for smart, latency-aware routing.

---

## 🛠️ Quickstart

### 1. Clone & Install Dependencies

```sh
git clone https://github.com/sassikoussai/project-django.git
cd project-django
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in your project root with the following content:

```dotenv
SECRET_KEY='django-insecure-7obc$(lqz9=kd#)!-8o4a7=0z#0=8o*-qg2wxa14a8)5czge-&'
DATABASE_URL='postgres://postgres:nNYoJRRCNyvyJik@recruitment-db.flycast:5432/postgres'
DEBUG=True
CSRF_TRUSTED_ORIGINS='https://ai-based-resume-screening-recruitment.fly.dev'
FLY_API_TOKEN="FlyV1 fm2_lJPECAAAAAAACJWPxBBI56/YCcuZOMb9T4kF+6pBwrVodHRwczovL2FwaS5mbHkuaW8vdjGWAJLOABALph8Lk7lodHRwczovL2FwaS5mbHkuaW8vYWFhL3YxxDy5q9ZVCYDOs+2BPQAi6biXYPHd8emIWKIwUuW1s4Q/xQAWgrAvch22FCS9LmrGtsZf0pg5SQeaWmszmffETkdXtZE5/O09B+yt1gYqBXRg79MFnvpgw3XSL2Gw8LyRVVkkaYSWmQxpulVVphXCEYVakAR2IgyauNOhDx1kcUF0mTYmQ69VCJVV1oTuvw2SlAORgc4AcEbPHwWRgqdidWlsZGVyH6J3Zx8BxCCgB3whO/EBEYFPCwjIXXolRiK4t6iNSqo6+zXmdyX9dg==,fm2_lJPETkdXtZE5/O09B+yt1gYqBXRg79MFnvpgw3XSL2Gw8LyRVVkkaYSWmQxpulVVphXCEYVakAR2IgyauNOhDx1kcUF0mTYmQ69VCJVV1oTuv8QQ57CG7KOiDOuEt77DU4ONr8O5aHR0cHM6Ly9hcGkuZmx5LmlvL2FhYS92MZgEks5oNj9qzwAAAAEkLl2IF84AEDH7CpHOABAx+wzEEJ/JFDuvQevevFNJ6sSaXVfEIKeullec4oIyTLemCUeylJ4kPOtWj/JUK5Gmi9GpNrL7"
FLY_APP_NAME=ai-based-resume-screening-recruitment-master
ALLOWED_HOSTS=ai-based-resume-screening-recruitment-master.fly.dev,localhost,127.0.0.1
```

### 3. Migrate & Create Superuser

```sh
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Services

- **Django:**  
  `python manage.py runserver`
- **Celery:**  
  `celery -A ai_based_resume_screening_recruitment worker -l info`

---

## 🔌 API Overview

### REST Endpoints

- `POST /api/edge-nodes/` – Register an edge node
- `GET /api/edge-nodes/` – List/monitor edge nodes

### GraphQL

- Visit `/graphql/`
- Example:
  ```graphql
  query {
    edgeNodes {
      id
      name
      latitude
      longitude
      status
    }
    nodePerformance(nodeId: 1) {
      avgLatency
      requestCount
    }
  }
  ```

---

## 🤖 AI Routing & Edge Deployment

- Place your trained model as `model.pkl` in the correct location.
- Celery tasks:
  - `deploy_to_flyio` – Deploys to Fly.io.
  - `deploy_code_with_ai_routing` – Predicts best edge node and deploys.
- Features for predictions might include node geolocation, current workload, etc.

---

## 🔒 Security

- **API Key:**  
  Use API key authentication for edge nodes.
- **Mutual TLS:**  
  Configure mTLS at your proxy or platform layer (e.g., Nginx, Fly.io).//

---

## 🧪 Testing

- Run unit tests:  
  `python manage.py test`
- Test Celery tasks:  
  Import and run them directly or watch logs as you trigger deployments.

---



## 🤝 Contributions

Open to PRs and issues—please describe your enhancement or fix clearly!

---