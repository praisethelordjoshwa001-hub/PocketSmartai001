# PocketSmart AI — Complete Build

FastAPI + Jinja2 + SQLite + Gemini GenAI implementation of the supplied PocketSmart AI specification.

## What is included
- Registration/login/logout and JWT token endpoint
- Home, Party and Jewelry planners
- Optional jewelry outfit image input
- Gemini structured-output integration
- Deterministic local fallback when no Gemini key is configured
- Recommendation history and detail pages
- Platform search links for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO
- Responsive frontend and FastAPI Swagger docs

## Setup
Windows PowerShell:
```powershell
cd PocketSmartAI
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

Put your Gemini API key in `.env` as `GEMINI_API_KEY=...`. The model is configurable with `GEMINI_MODEL`. If no key is supplied, the application stays usable in demo/fallback mode.

## Tests
```powershell
pytest -q
```

## API docs
http://127.0.0.1:8000/docs

## Important product/API note
The supplied specification mentions sourcing from Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO. This build intentionally does not pretend to have access to private vendor APIs or scrape sites. It generates search links and uses local demo catalog data. If you have authorized partner/API access, replace `app/services/catalog.py` with those integrations.
