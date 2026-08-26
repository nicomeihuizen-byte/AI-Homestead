"""Local model via Ollama. Structured JSON output, schema-validated.

Schema per recommendation:
    {action, crop, plot, window, rationale, confidence, inputs_used}

`inputs_used` is what makes a recommendation auditable three months later.

Prompts live in scheduler/prompts/ and every output row records the prompt hash; when the
advice changes you need to know whether the world changed or the prompt did.

TODO Phase 8.
"""
