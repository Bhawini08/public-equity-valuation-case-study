from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass(frozen=True)
class Scenario:
    name:str
    wacc:float
    terminal_growth:float
    tax_rate:float
    revenue_growth:list[float]
    operating_margin:list[float]
    d_and_a_pct_revenue:float
    capex_pct_revenue:float
    nwc_pct_revenue:float
    net_debt_change_per_year:float
    share_count_decline:float

def load_inputs(hist_path="data/adobe_historicals.csv",bs_path="data/adobe_balance_sheet_2025.csv",assumptions_path="data/valuation_inputs.csv"):
    hist=pd.read_csv(hist_path).set_index("year")
    bs=pd.read_csv(bs_path).set_index("line_item")["2025"]
    a=pd.read_csv(assumptions_path).set_index("input")
    return hist,bs,a

def scenario_from_table(a:pd.DataFrame,name:str):
    years=range(2026,2031)
    return Scenario(name,float(a.loc["wacc",name]),float(a.loc["terminal_growth",name]),float(a.loc["tax_rate",name]),
        [float(a.loc[f"revenue_growth_{y}",name]) for y in years],
        [float(a.loc[f"operating_margin_{y}",name]) for y in years],
        float(a.loc["d_and_a_pct_revenue",name]),float(a.loc["capex_pct_revenue",name]),
        float(a.loc["nwc_pct_revenue",name]),float(a.loc["net_debt_change_per_year",name]),
        float(a.loc["share_count_decline",name]))

def build_forecast(hist:pd.DataFrame,bs:pd.Series,s:Scenario):
    years=list(range(2026,2031)); rows=[]
    prev_rev=float(hist.loc[2025,"revenue"])
    prev_nwc=s.nwc_pct_revenue*prev_rev
    debt=float(bs["debt"]); shares=float(bs["shares_outstanding"])
    ppe=float(bs["ppe"]); cash=float(bs["cash"])
    for i,y in enumerate(years):
        revenue=prev_rev*(1+s.revenue_growth[i])
        op_income=revenue*s.operating_margin[i]
        d_and_a=revenue*s.d_and_a_pct_revenue
        capex=revenue*s.capex_pct_revenue
        nwc=revenue*s.nwc_pct_revenue
        delta_nwc=nwc-prev_nwc
        interest=max(debt,0)*0.04
        pretax=op_income-interest
        taxes=max(pretax,0)*s.tax_rate
        net_income=pretax-taxes
        fcff=op_income*(1-s.tax_rate)+d_and_a-capex-delta_nwc
        cfo=net_income+d_and_a-delta_nwc
        debt_change=debt*s.net_debt_change_per_year/100
        debt=max(0,debt+debt_change)
        shares=shares*(1-s.share_count_decline)
        ppe=ppe+capex-d_and_a
        # simplified cash build before discretionary repurchases
        cash=max(0,cash+cfo-capex+debt_change)
        rows.append({"year":y,"revenue":revenue,"revenue_growth":s.revenue_growth[i],"operating_margin":s.operating_margin[i],
                     "operating_income":op_income,"interest_expense":interest,"pretax_income":pretax,"tax_expense":taxes,
                     "net_income":net_income,"d_and_a":d_and_a,"capex":capex,"nwc":nwc,"delta_nwc":delta_nwc,
                     "cfo":cfo,"fcff":fcff,"debt":debt,"cash":cash,"ppe":ppe,"shares":shares,
                     "eps":net_income/shares if shares else np.nan})
        prev_rev=revenue; prev_nwc=nwc
    return pd.DataFrame(rows).set_index("year")

def dcf_value(forecast:pd.DataFrame,bs:pd.Series,s:Scenario):
    fcff=forecast.fcff.to_numpy(float); years=np.arange(1,len(fcff)+1)
    pv_explicit=float(np.sum(fcff/(1+s.wacc)**years))
    terminal=fcff[-1]*(1+s.terminal_growth)/(s.wacc-s.terminal_growth)
    pv_terminal=float(terminal/(1+s.wacc)**len(fcff))
    enterprise=pv_explicit+pv_terminal
    net_debt=float(bs["debt"]-bs["cash"]-bs["short_term_investments"])
    equity=enterprise-net_debt
    shares=float(forecast.shares.iloc[-1])
    return {"enterprise_value":enterprise,"net_debt":net_debt,"equity_value":equity,
            "value_per_share":equity/shares,"pv_explicit":pv_explicit,"pv_terminal":pv_terminal}

def valuation_sensitivity(forecast,bs,wacc_grid=None,g_grid=None):
    wacc_grid=np.arange(.07,.105,.005) if wacc_grid is None else np.asarray(wacc_grid)
    g_grid=np.arange(.02,.045,.005) if g_grid is None else np.asarray(g_grid)
    fcff=forecast.fcff.to_numpy(float); years=np.arange(1,len(fcff)+1); shares=float(forecast.shares.iloc[-1])
    net_debt=float(bs["debt"]-bs["cash"]-bs["short_term_investments"])
    rows=[]
    for w in wacc_grid:
        for g in g_grid:
            if w<=g: continue
            pv=np.sum(fcff/(1+w)**years); tv=fcff[-1]*(1+g)/(w-g)/(1+w)**len(fcff)
            rows.append({"wacc":w,"terminal_growth":g,"value_per_share":(pv+tv-net_debt)/shares})
    return pd.DataFrame(rows)

def roic_proxy(hist:pd.DataFrame,bs:pd.Series):
    nopat=hist.loc[2025,"operating_income"]*(1-hist.loc[2025,"tax_expense"]/hist.loc[2025,"pretax_income"])
    invested=bs["equity"]+bs["debt"]-bs["cash"]-bs["short_term_investments"]
    return float(nopat/invested)
