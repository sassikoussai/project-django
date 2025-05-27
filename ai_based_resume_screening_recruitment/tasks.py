import os
import requests
import pickle
import numpy as np
from celery import shared_task

FLY_API_URL = "https://api.fly.io/graphql"
FLY_API_TOKEN = os.getenv("FlyV1 fm2_lJPECAAAAAAACJWPxBBI56/YCcuZOMb9T4kF+6pBwrVodHRwczovL2FwaS5mbHkuaW8vdjGWAJLOABALph8Lk7lodHRwczovL2FwaS5mbHkuaW8vYWFhL3YxxDy5q9ZVCYDOs+2BPQAi6biXYPHd8emIWKIwUuW1s4Q/xQAWgrAvch22FCS9LmrGtsZf0pg5SQeaWmszmffETkdXtZE5/O09B+yt1gYqBXRg79MFnvpgw3XSL2Gw8LyRVVkkaYSWmQxpulVVphXCEYVakAR2IgyauNOhDx1kcUF0mTYmQ69VCJVV1oTuvw2SlAORgc4AcEbPHwWRgqdidWlsZGVyH6J3Zx8BxCCgB3whO/EBEYFPCwjIXXolRiK4t6iNSqo6+zXmdyX9dg==,fm2_lJPETkdXtZE5/O09B+yt1gYqBXRg79MFnvpgw3XSL2Gw8LyRVVkkaYSWmQxpulVVphXCEYVakAR2IgyauNOhDx1kcUF0mTYmQ69VCJVV1oTuv8QQ57CG7KOiDOuEt77DU4ONr8O5aHR0cHM6Ly9hcGkuZmx5LmlvL2FhYS92MZgEks5oNj9qzwAAAAEkLl2IF84AEDH7CpHOABAx+wzEEJ/JFDuvQevevFNJ6sSaXVfEIKeullec4oIyTLemCUeylJ4kPOtWj/JUK5Gmi9GpNrL7")  # Store API token securely in environment variables

# Load pre-trained AI model (example: scikit-learn model)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(MODEL_PATH, "rb") as file:
    ai_model = pickle.load(file)

def predict_optimal_node(features):
    """
    Predict the optimal edge node based on input features using the AI model.

    Args:
        features (list): A list of input features for prediction.

    Returns:
        str: Predicted optimal edge node.
    """
    prediction = ai_model.predict([features])
    return prediction[0]

@shared_task
def deploy_code_with_ai_routing(app_name, deployment_payload, features):
    """
    Deploy code to Fly.io edge platforms with AI-based routing decisions.

    Args:
        app_name (str): Name of the Fly.io application.
        deployment_payload (dict): Payload containing deployment details.
        features (list): Features for AI model to predict optimal edge node.

    Returns:
        dict: Response from Fly.io API.
    """
    # Predict the optimal edge node
    optimal_node = predict_optimal_node(features)

    # Add the optimal node to deployment payload
    deployment_payload["config"]["optimal_node"] = optimal_node

    headers = {
        "Authorization": f"Bearer {FLY_API_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        FLY_API_URL,
        json={
            "query": """
            mutation ($input: DeployInput!) {
                deploy(input: $input) {
                    id
                    status
                }
            }
            """,
            "variables": {
                "input": deployment_payload,
            },
        },
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}