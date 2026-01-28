# AutomationExercise - Playwright (Python) POM

## Quickstart

```bash
pip install -r requirements.txt
playwright install
pytest
```

### Headed mode

```bash
HEADLESS=0 pytest -q
```

## Output

- HTML report: `reports/report.html`

## CI

GitHub Actions workflow in `.github/workflows/ci.yml` runs tests headless and uploads the HTML report as an artifact.
