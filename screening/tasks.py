import os
import requests
import pickle
from celery import shared_task
import subprocess
import logging

# If you use django-environ, import and initialize it here:
# import environ
# env = environ.Env()
# environ.Env.read_env()

FLY_APP_NAME = os.environ.get("FLY_APP_NAME")  # or use env("FLY_APP_NAME")
FLY_API_TOKEN = os.environ.get("FLY_API_TOKEN")  # or use env("FLY_API_TOKEN")
FLY_API_URL = "https://api.fly.io/graphql"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

# Load the AI model at import time (once)
try:
    with open(MODEL_PATH, "rb") as file:
        ai_model = pickle.load(file)
except Exception as e:
    ai_model = None
    logging.error(f"Failed to load AI model: {e}")



 # AI model used

def predict_optimal_node(features):
    """
    Predict the optimal edge node based on input features using the AI model.
    Args:
        features (list): A list of input features for prediction.
    Returns:
        str: Predicted optimal edge node.
    """
    if ai_model is None:
        raise RuntimeError("AI model not loaded")
    prediction = ai_model.predict([features])
    return prediction[0]

@shared_task
def deploy_to_flyio():
    """
    Run 'flyctl deploy --remote-only' from Celery.
    """
    try:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result = subprocess.run(
            ["flyctl", "deploy", "--remote-only"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True
        )
        logging.info("Fly.io deploy succeeded: %s", result.stdout)
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        logging.error("Fly.io deploy failed: %s", e.stderr)
        return {"status": "failed", "error": e.stderr}


# AI model used

@shared_task
def deploy_code_with_ai_routing(deployment_payload: dict, features: list):
    """
    Deploy code to Fly.io edge platforms with AI-based routing decisions.

    Args:
        deployment_payload (dict): Payload containing deployment details.
        features (list): Features for AI model to predict optimal edge node.

    Returns:
        dict: Response from Fly.io API.
    """
    if FLY_API_TOKEN is None or FLY_APP_NAME is None:
        return {"error": "Missing FLY_API_TOKEN or FLY_APP_NAME environment variable."}
    if ai_model is None:
        return {"error": "AI model not loaded."}

    # Predict the optimal edge node
    optimal_node = predict_optimal_node(features)

    # Add the optimal node to deployment payload (adjust this to match Fly API schema)
    deployment_payload.setdefault("config", {})["optimal_node"] = optimal_node

    headers = {
        "Authorization": f"Bearer {FLY_API_TOKEN}",
        "Content-Type": "application/json",
    }

    # Example mutation and input; adjust as needed for your Fly.io workflow
    query = """
    mutation DeployCode($input: DeployImageInput!) {
        deployImage(input: $input) {
            release {
                id
                version
            }
            app {
                name
                status
            }
        }
    }
    """

    variables = {
        "input": {
            "appId": FLY_APP_NAME,
            # You may need to flatten/decompose your deployment_payload as needed by Fly.io API
            **deployment_payload
        }
    }

    response = requests.post(
        FLY_API_URL,
        json={
            "query": query,
            "variables": variables,
        },
        headers=headers,
    )
    try:
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"error": response.text}