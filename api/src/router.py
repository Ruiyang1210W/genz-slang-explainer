import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .inference import generate
from .postprocess import parse_definition_example
from .retrieval import lookup

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Gen Z Slang Explainer API",
    description="Fine-tuned LLM API for explaining Gen Z slang with definitions and examples",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info("Starting Gen Z Slang Explainer API")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Shutting down Gen Z Slang Explainer API")


@app.get("/")
def index():
    """Root endpoint returning service information."""
    return {"service": "slang-explainer", "status": "ok", "version": "0.1.0"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"ok": True}


class ExplainInput(BaseModel):
    """Request model for explain endpoint."""

    term: str = Field(..., min_length=1, max_length=100, description="The slang term to explain")


class ExplainResponse(BaseModel):
    """Response model for explain endpoint."""

    term: str
    definition: str | None
    example: str | None
    source: str


@app.post("/v1/explain", response_model=ExplainResponse)
def explain(payload: ExplainInput):
    """
    Explain a Gen Z slang term with definition and example.

    Args:
        payload: Input containing the slang term to explain

    Returns:
        ExplainResponse with definition, example, and metadata

    Raises:
        HTTPException: If an error occurs during processing
    """
    term = payload.term.strip().lower()

    if not term:
        raise HTTPException(status_code=400, detail="Term cannot be empty")

    logger.info(f"Explaining term: {term}")

    try:
        # 1) Try LoRA model generation
        raw = generate(term)
        parsed = parse_definition_example(raw)

        # 2) Fallback to baseline if needed
        source = "lora"
        if not parsed["format_ok"]:
            logger.warning(f"LoRA output format invalid for term: {term}, trying fallback")
            base = lookup(term)
            if base:
                parsed["definition"] = parsed["definition"] or base["definition"]
                parsed["example"] = parsed["example"] or base["example"]
                source = "lora+baseline"
                logger.info(f"Used baseline fallback for term: {term}")
            else:
                source = "lora_raw"
                logger.warning(f"No baseline match found for term: {term}")

        logger.info(f"Successfully explained term: {term} (source: {source})")

        return {
            "term": term,
            "definition": parsed["definition"],
            "example": parsed["example"],
            "source": source,
        }
    except Exception as e:
        logger.error(f"Error explaining term '{term}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing term: {str(e)}")
