def process_with_cloud(text: str) -> tuple[str, float]:
    return ("Processed with ChatGPT!", 0.95)

def process_with_local_llama(text: str) -> tuple[str, float]:
    return ("Processed with local GPU LLaMA!", 0.90)

def process_with_quantized_llama(text: str) -> tuple[str, float]:
    return ("Processed with quantized CPU LLaMA!", 0.85)

def needs_cloud_processing(text: str) -> bool:
    return len(text) > 500

def gpu_available() -> bool:
    return True  # You can later add real hardware detection here
