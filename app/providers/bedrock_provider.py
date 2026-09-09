"""
Optional cloud provider backed by AWS Bedrock.
Only used when LLM_PROVIDER=bedrock.

Setup:
    pip install boto3
    aws configure   # or mount credentials via Sealed Secret in-cluster
    IAM permissions needed: bedrock:InvokeModel (scope to specific model ARNs)

Cost note: no free tier. New accounts get up to $200 in credits that
expire after 6 months. See docs/bedrock-notes.md before running loops
of test calls — track token usage manually while developing.
"""

import json
import os
from typing import List

import boto3

from .base import LLMProvider


class BedrockProvider(LLMProvider):
    def __init__(
        self,
        model_id: str = None,
        embed_model_id: str = None,
        region: str = None,
    ):
        self.model_id = model_id or os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-5-haiku-20241022-v1:0"
        )
        self.embed_model_id = embed_model_id or os.getenv(
            "BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v2:0"
        )
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.client = boto3.client("bedrock-runtime", region_name=self.region)

    @property
    def name(self) -> str:
        return "bedrock"

    def generate(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            body["system"] = system

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
        )
        payload = json.loads(response["body"].read())
        return payload["content"][0]["text"]

    def embed(self, text: str) -> List[float]:
        response = self.client.invoke_model(
            modelId=self.embed_model_id,
            body=json.dumps({"inputText": text}),
        )
        payload = json.loads(response["body"].read())
        return payload["embedding"]
