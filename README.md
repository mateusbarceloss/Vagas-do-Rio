# Vagas do Rio

Site estático de vagas de emprego no Rio de Janeiro, 100% grátis e automatizado.

O site vai ficar publicado em algo como:
`https://SEU-USUARIO.github.io/Vagas-do-Rio/`

- As vagas vêm da API da Adzuna (`scripts/fetch_jobs.py`).
- Um workflow do GitHub Actions (`.github/workflows/update-jobs.yml`) roda esse
  script todo dia e atualiza `docs/jobs.json` automaticamente.
- `docs/index.html` é o site em si (publicado via GitHub Pages), com busca por
  cargo e cidade.

## Configuração necessária

Em Settings → Secrets and variables → Actions, adicione:
- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`

(Conseguidos gratuitamente em https://developer.adzuna.com/)
