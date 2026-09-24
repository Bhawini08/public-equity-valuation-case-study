# Adobe (ADBE) Public Equity Valuation & Investment Case

A fundamental equity-research case study built around Adobe Inc. The project links reported historical financials to a five-year operating forecast, DCF valuation, scenario analysis, statement views, and a concise investment memo.

## Historical base

The seeded historical dataset uses Adobe fiscal 2023-2025 reported financials from the FY2025 Form 10-K / annual report. Model values are in USD millions unless otherwise stated.

## Model

- Revenue and operating-margin forecast
- Working-capital schedule
- CapEx and depreciation schedule
- Debt and interest schedule
- Tax schedule
- Share-count schedule
- Forecast income statement, balance-sheet view, and cash-flow statement
- Free cash flow to firm
- WACC and terminal-value DCF
- EV / EBITDA and P / E reference framework
- Bull, base, and bear scenarios
- ROIC and operating-driver analysis
- DCF sensitivity analysis

## Validated valuation output

Using the current scenario assumptions and FY2025 diluted share count of **427 million**:

| Scenario | Enterprise value | Equity value | Value / share |
| --- | ---: | ---: | ---: |
| Bear | $117.4B | $117.8B | **$275.90** |
| Base | $190.8B | $191.2B | **$447.77** |
| Bull | $286.0B | $286.4B | **$670.76** |

The model uses current diluted shares for present-value per-share valuation. Forecast share-count reductions are modeled for EPS and operating scenarios but are not used to inflate today's DCF value without also modeling the cash cost of those future repurchases.

## Validation controls

- Bull > base > bear valuation ordering
- Positive FCFF across forecast scenarios
- DCF sensitivity grid
- Historical balance-sheet identity check
- Explicit current-share-count test for DCF per-share value
- Reported facts separated from forecast assumptions

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest -q
python scripts/run_case.py
```

## Scope discipline

The forecast statement views are designed to support valuation and operating-driver analysis. They should not be interpreted as a fully transaction-level accounting model with every balance-sheet line dynamically forecast and balanced.

Trading-comparable multiples remain a refreshable framework rather than frozen market data.

## Source discipline

Historical statement figures are sourced from Adobe's FY2025 annual report. Forecasts and valuation assumptions are stored separately from reported facts.
