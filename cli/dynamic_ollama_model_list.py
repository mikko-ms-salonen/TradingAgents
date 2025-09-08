import requests

def format_size(size_bytes) -> str:
    """
    Converts a size in bytes to a human-readable string.
    """
    if size_bytes is None:
        return "unknown"
    try:
        size_bytes = int(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"
    except (ValueError, TypeError):
        return "unknown"

def dynamic_ollama_model_list(ollama_base_url: str) -> list[tuple]:
    """
    Fetches the list of models from the Ollama API and returns them as tuples:
    ("model name (model size)", "model")

    Args:
        ollama_base_url (str): Base URL of the Ollama API (e.g., "http://localhost:11434")

    Returns:
        List[Tuple[str, str]]: List of formatted model tuples
    """
    if "/v1" in ollama_base_url:
        ollama_base_url = ollama_base_url.split("/v1")[0]
    try:
        response = requests.get(f"{ollama_base_url}/api/tags")
        response.raise_for_status()
        data = response.json()

        models = data.get("models", [])
        formatted_models = []

        for model in models:
            name = model.get("name", "unknown")
            size_bytes = model.get("size", None)
            size_hr = format_size(size_bytes)
            label = f"{name} ({size_hr})"
            formatted_models.append((label, name))

        return formatted_models

    except requests.RequestException as e:
        print(f"Error fetching models: {e}")
        return []