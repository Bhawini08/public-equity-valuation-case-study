import json
from pathlib import Path
import pandas as pd
from equity_case.model import load_inputs,scenario_from_table,build_forecast,dcf_value,valuation_sensitivity,roic_proxy
from equity_case.statements import historical_summary,forecast_three_statements
out=Path("results"); out.mkdir(exist_ok=True)
h,b,a=load_inputs(); historical_summary(h).to_csv(out/"historical_summary.csv")
rows=[]
for name in ["bear","base","bull"]:
    s=scenario_from_table(a,name); f=build_forecast(h,b,s); f.to_csv(out/(name+"_forecast.csv"))
    inc,bs,cf=forecast_three_statements(f,b); inc.to_csv(out/(name+"_income_statement.csv")); bs.to_csv(out/(name+"_balance_sheet.csv")); cf.to_csv(out/(name+"_cash_flow.csv"))
    d=dcf_value(f,b,s); rows.append({"scenario":name,**d})
    if name=="base": valuation_sensitivity(f,b).to_csv(out/"dcf_sensitivity.csv",index=False)
summary=pd.DataFrame(rows); summary.to_csv(out/"valuation_summary.csv",index=False)
metrics={"roic_proxy_2025":roic_proxy(h,b),"base_value_per_share":float(summary.loc[summary.scenario=="base","value_per_share"].iloc[0])}
(out/"metrics.json").write_text(json.dumps(metrics,indent=2))
print(summary.to_json(orient="records",indent=2))
