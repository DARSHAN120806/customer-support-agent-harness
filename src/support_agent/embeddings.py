"""Embedding models: they turn text into numbers for the knowledge base search."""

from __future__ import annotations

import json

from .retry import ServiceError

DEFAULT_TITAN_MODEL = "amazon.titan-embed-text-v2:0"
TITAN_DIMENSIONS = 512

# AWS error codes that mean "try again in a moment".
RETRYABLE_AWS_CODES = {
    "ThrottlingException",
    "TooManyRequestsException",
    "ServiceUnavailableException",
    "ModelNotReadyException",
    "ModelTimeoutException",
    "InternalServerException",
    "RequestTimeout",
}


def to_service_error(error: Exception) -> ServiceError:
    """Turn an error from the AWS library into a ServiceError that says whether
    it is worth trying again."""
    from botocore.exceptions import BotoCoreError, ClientError

    if isinstance(error, ClientError):
        code = error.response.get("Error", {}).get("Code", "Unknown")
        status = error.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0)
        return ServiceError(
            f"The embedding service returned an error ({code}).",
            service="embeddings",
            kind=code,
            retryable=code in RETRYABLE_AWS_CODES or status >= 500,
        )
    if isinstance(error, BotoCoreError):
        # Connection problems and timeouts. Missing credentials also arrive
        # here, and those will not fix themselves.
        name = type(error).__name__
        return ServiceError(
            f"Could not reach the embedding service ({name}).",
            service="embeddings",
            kind=name,
            retryable="Credential" not in name and "Region" not in name,
        )
    return ServiceError(
        f"The embedding service gave an answer that could not be read ({type(error).__name__}).",
        service="embeddings",
        kind="bad_response",
        retryable=False,
    )


class TitanEmbedder:
    """Amazon Titan Text Embeddings, reached through Amazon Bedrock.

    AWS credentials are read from the environment by the AWS library itself.
    """

    def __init__(
        self, aws_region: str, model_id: str = DEFAULT_TITAN_MODEL, timeout_seconds: float = 60
    ) -> None:
        # Imported here so the AWS library is only loaded when it is needed.
        import boto3
        from botocore.config import Config

        self._client = boto3.client(
            "bedrock-runtime",
            region_name=aws_region,
            # The AWS library's own retries are switched off; ours are used
            # instead, so every retry can be logged.
            config=Config(
                retries={"total_max_attempts": 1},
                connect_timeout=10,
                read_timeout=timeout_seconds,
            ),
        )
        self._model_id = model_id
        self.name = f"{model_id}/{TITAN_DIMENSIONS}"

    def embed(self, text: str) -> list[float]:
        try:
            response = self._client.invoke_model(
                modelId=self._model_id,
                body=json.dumps(
                    {"inputText": text, "dimensions": TITAN_DIMENSIONS, "normalize": True}
                ),
            )
            embedding = json.loads(response["body"].read())["embedding"]
            if not isinstance(embedding, list) or not embedding:
                raise ValueError("empty embedding")
            return embedding
        except ServiceError:
            raise
        except Exception as error:
            raise to_service_error(error) from error


class OpenAICompatibleEmbedder:
    """Embeddings from any service that speaks the OpenAI format: OpenAI itself,
    or a local model through Ollama (for example "nomic-embed-text") or LM Studio.

    Our search scores sections by multiplying vectors, which assumes each vector
    has length 1. Titan guarantees that; other models may not, so every vector
    is scaled to length 1 here.
    """

    def __init__(self, client, model: str) -> None:
        self._client = client
        self._model = model
        # Identifies the model, so cached embeddings from another model are not reused.
        self.name = f"openai-compatible/{model}"

    def embed(self, text: str) -> list[float]:
        import openai

        try:
            response = self._client.embeddings.create(model=self._model, input=text)
            vector = [float(x) for x in response.data[0].embedding]
        except openai.APIError as error:
            from .providers.openai_compatible import to_service_error as model_error

            problem = model_error(error)
            raise ServiceError(
                str(problem).replace("model service", "embedding service"),
                service="embeddings",
                kind=problem.kind,
                retryable=problem.retryable,
            ) from error
        except (AttributeError, IndexError, TypeError, ValueError) as error:
            raise ServiceError(
                "The embedding service gave an answer that could not be read.",
                service="embeddings",
                kind="bad_response",
                retryable=False,
            ) from error
        length = sum(x * x for x in vector) ** 0.5
        if not vector or length == 0:
            raise ServiceError("The embedding service sent an empty vector.", service="embeddings", kind="bad_response", retryable=False)
        return [x / length for x in vector]
