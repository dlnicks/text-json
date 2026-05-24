# Text-to-JSON — Learning Notes

## Setup
- Secrets (API keys) go in `.env`, never in code. `.env` is gitignored → key stays local. (Hardcoded keys get scraped off GitHub in minutes.)
- Key path: `.env` → `load_dotenv()` loads it into environment variables → `OpenAI()` auto-reads `OPENAI_API_KEY`.
- Variable must be named exactly `OPENAI_API_KEY`. Debugging a key: check it's in `.env`, `load_dotenv()` runs before `OpenAI()`, name is exact.
- `pip freeze > requirements.txt` — saves exact versions of installed libraries so others can `pip install -r requirements.txt`.
- Libraries pull in their own dependencies automatically (pydantic came bundled with openai). If you import something directly, install it explicitly so it can't vanish when the parent changes.

## Concepts

### Messages & roles
- `messages` = list of `{role, content}`. Model has NO memory — you send the whole conversation every call.
- Roles: `system` (behaviour/instructions), `user` (human input), `assistant` (model's past replies). They tell the stateless model who said what.

### Structured output
- System message forces JSON instead of prose: messy text in → structured data out. You instruct intent; the model structures it (core of applied AI).
- `response_format={"type":"json_object"}` guarantees valid JSON text (prompt must contain the word "JSON").
- But `.content` is still a string — fragile until parsed + validated.

### Pydantic validation
- Define the expected shape as a class (fields + types). `model_validate_json()` parses AND validates in one step.
- Wrong type / missing field → `ValidationError` naming the field + reason. Catches bad LLM output at the door, not downstream.
- `Optional[type] = None` → field allowed to be missing (validates to None, no crash).
- Trade-off: required = fail-fast (reject bad data); optional = extract what you can (suits messy text).
- Interview line for "handling unreliable LLM output": validate against a schema, fail fast with clear errors.

### try/except
- `try` runs risky code (validation) → success returns the result. `except` catches failure → print message, return None.
- Function returns a valid object OR None. `if person:` checks which — valid prints, None skips. = graceful failure instead of crashing.

### Functions & docstrings
- Docstring (`"""..."""` first line in a function) describes its purpose. Unlike `#` comments, Python keeps it — readable via `help()` / editor hover.
- Brackets `()` = call/run a function now. No brackets = pass the function itself as a value (first-class).
- Variables are referenced (just name them); functions are called (need brackets).

## Stuck points
(what broke + how I fixed it)

## Decisions

### When to use an LLM vs not
- Fixed/predictable input → regex/parsing. Free, fast, deterministic.
- Messy/varied natural language → LLM. Handles infinite phrasings rules can't enumerate.
- The skill is choosing: LLM-for-everything is overkill; don't pay for what regex does.