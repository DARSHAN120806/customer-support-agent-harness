"""Embedding models: they turn text into numbers for the knowledge base search."""

from __future__ import annotations

import json

DEFAULT_TITAN_MODEL = "amazon.titan-embed-text-v2:0"
TITAN_DIMENSIONS = 512


class TitanEmbedder:
    """Amazon Titan Text Embeddings, reached through Amazon Bedrock.

    AWS credentials are read from the environment by the AWS library itself.
    """

    def __init__(self, aws_region: str, model_id: str = DEFAULT_TITAN_MODEL) -> None:
        # Imported here so the AWS library is only loaded when it is needed.
        import boto3

        self._client = boto3.client("bedrock-runtime", region_name=aws_region)
        self._model_id = model_id
        self.name = f"{model_id}/{TITAN_DIMENSIONS}"

    def embed(self, text: str) -> list[float]:
        response = self._client.invoke_model(
            modelId=self._model_id,
            body=json.dumps(
                {"inputText": text, "dimensions": TITAN_DIMENSIONS, "normalize": True}
            ),
        )
        return json.loads(response["body"].read())["embedding"]
