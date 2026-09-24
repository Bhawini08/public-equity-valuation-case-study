import pandas as pd

def historical_summary(hist:pd.DataFrame):
    x=hist.copy()
    x["gross_margin"]=x.gross_profit/x.revenue
    x["operating_margin"]=x.operating_income/x.revenue
    x["net_margin"]=x.net_income/x.revenue
    x["fcf_proxy"]=x.cfo-x.capex
    return x

def forecast_three_statements(forecast:pd.DataFrame,bs_start:pd.Series):
    income=forecast[["revenue","operating_income","interest_expense","pretax_income","tax_expense","net_income","eps"]].copy()
    cashflow=forecast[["net_income","d_and_a","delta_nwc","cfo","capex"]].copy()
    cashflow["investing_cash_flow"]=-cashflow["capex"]
    cashflow["free_cash_flow"]=cashflow["cfo"]-cashflow["capex"]
    balance=forecast[["cash","ppe","debt","shares"]].copy()
    balance["net_working_capital"]=forecast["nwc"]
    balance["goodwill"]=float(bs_start["goodwill"])
    balance["intangibles"]=float(bs_start["intangibles"])
    return income,balance,cashflow
