# Adobe (ADBE) Public Equity 3-Statement Valuation & Investment Case

A fundamental equity-research case study built around Adobe Inc. The project links historical financial statements to a five-year operating forecast, an integrated three-statement model, DCF valuation, scenario analysis, and a concise investment memo.

## Historical base

The seeded historical dataset uses Adobe fiscal 2023-2025 reported financials from the FY2025 Form 10-K / annual report. Model values are in USD millions unless otherwise stated.

## Model

- Revenue and margin forecast
- Working-capital schedule
- CapEx and depreciation schedule
- Debt and interest schedule
- Tax schedule
- Share-count schedule
- Integrated income statement, balance sheet, and cash flow statement
- Free cash flow to firm
- WACC and terminal-value DCF
- EV / EBITDA and P / E reference framework
- Bull, base, and bear scenarios
- ROIC and operating-driver analysis

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest -q
python scripts/run_case.py
```

The model intentionally keeps market price and peer multiples as refreshable inputs. We will perform the final live-market-price and trading-comps refresh during the validation pass.

## Source discipline

Historical statement figures are sourced from Adobe's FY2025 annual report. Forecasts and valuation assumptions are explicitly separated from reported facts.
