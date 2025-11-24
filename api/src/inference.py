import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

logger = logging.getLogger(__name__)

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# Navigate up two levels from src/ to project root, then to models/
ADAPTER_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "models", "adapters", "tinyllama-lora@2025-10-29"
)

INSTRUCT_TEMPLATE = (
    "Task: Explain the internet slang.\n"
    "Term: {term}\n\n"
    "Definition:"
)

# Initialize model and tokenizer at module level
try:
    logger.info(f"Loading base model: {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32,  # CPU-friendly
        device_map={"": "cpu"},
        low_cpu_mem_usage=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base.config.pad_token_id = tokenizer.pad_token_id

    logger.info(f"Loading LoRA adapters from: {ADAPTER_DIR}")
    if not os.path.exists(ADAPTER_DIR):
        logger.error(f"Adapter directory not found: {ADAPTER_DIR}")
        raise FileNotFoundError(f"Adapter directory not found: {ADAPTER_DIR}")

    model = PeftModel.from_pretrained(base, ADAPTER_DIR, device_map={"": "cpu"})
    model.eval()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}", exc_info=True)
    raise


def generate(term: str, max_new_tokens: int = 100) -> str:
    """
    Generate slang explanation using the fine-tuned model.

    Args:
        term: The slang term to explain
        max_new_tokens: Maximum number of tokens to generate

    Returns:
        str: Generated explanation text

    Raises:
        ValueError: If term is empty
        RuntimeError: If generation fails
    """
    if not term or not term.strip():
        raise ValueError("Term cannot be empty")

    try:
        prompt = INSTRUCT_TEMPLATE.format(term=term.strip())
        logger.debug(f"Generating explanation for term: {term}")

        inputs = tokenizer(prompt, return_tensors="pt")  # already on CPU

        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,  # Use greedy decoding for more deterministic output
                num_beams=1,
                repetition_penalty=1.2,  # Reduce repetition
                pad_token_id=tokenizer.eos_token_id,
            )

        result = tokenizer.decode(out[0], skip_special_tokens=True)
        logger.debug(f"Generated text length: {len(result)} characters")
        return result

    except Exception as e:
        logger.error(f"Generation failed for term '{term}': {str(e)}", exc_info=True)
        raise RuntimeError(f"Generation failed: {str(e)}") from e
