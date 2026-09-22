"""
Busca vagas de emprego no Rio de Janeiro usando a API da Adzuna
e salva em docs/jobs.json para o site estático ler.

Documentação da API: https://developer.adzuna.com/
Uso gratuito: até 2.500 consultas por mês.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

APP_ID = os.environ["ADZUNA_APP_ID"]
APP_KEY = os.environ["ADZUNA_APP_KEY"]

COUNTRY = "br"
BASE_URL = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search"

LOCATIONS = [
    "Rio de Janeiro",
    "Niterói",
    "Duque de Caxias",
    "Nova Iguaçu",
    "São Gonçalo",
    "Guapimirim",
    "Magé",
    "Petrópolis",
    "Volta Redonda",
    "Campos dos Goytacazes",
]

RESULTS_PER_LOCATION = 20
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "jobs.json"


def fetch_jobs_for_location(location: str, page: int = 1):
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTS_PER_LOCATION,
        "where": location,
        "content-type": "application/json",
    }
    url = f"{BASE_URL}/{page}?{urlencode(params)}"
    try:
        with urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("results", [])
    except HTTPError as e:
        print(f"Erro ao buscar '{location}': {e}")
        return []


def normalize_job(raw: dict, fallback_location: str) -> dict:
    return {
        "title": raw.get("title", "").strip(),
        "company": (raw.get("company") or {}).get("display_name", "Empresa não informada"),
        "location": (raw.get("location") or {}).get("display_name", fallback_location),
        "description": (raw.get("description", "")[:400]).strip(),
        "apply_url": raw.get("redirect_url", ""),
        "created": raw.get("created", ""),
        "salary_min": raw.get("salary_min"),
        "salary_max": raw.get("salary_max"),
        "category": (raw.get("category") or {}).get("label", ""),
    }


def main():
    all_jobs = {}

    for location in LOCATIONS:
        print(f"Buscando vagas em: {location}")
        raw_jobs = fetch_jobs_for_location(location)
        for raw in raw_jobs:
            job = normalize_job(raw, location)
            if job["apply_url"]:
                all_jobs[job["apply_url"]] = job
        time.sleep(1)

    jobs_list = sorted(
        all_jobs.values(), key=lambda j: j.get("created", ""), reverse=True
    )

    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(jobs_list),
        "jobs": jobs_list,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Salvo {len(jobs_list)} vagas em {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
