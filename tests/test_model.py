import numpy as np
from equity_case.model import load_inputs,scenario_from_table,build_forecast,dcf_value,valuation_sensitivity,roic_proxy
from equity_case.statements import forecast_three_statements

def test_scenarios_build_and_dcf_ordering():
    h,b,a=load_inputs()
    vals={}
    for name in ["bear","base","bull"]:
        s=scenario_from_table(a,name); f=build_forecast(h,b,s); d=dcf_value(f,b,s,current_diluted_shares=float(h.loc[2025,"diluted_shares"]))
        assert len(f)==5 and (f.revenue>0).all() and (f.fcff>0).all()
        assert np.isfinite(d["value_per_share"])
        vals[name]=d["value_per_share"]
    assert vals["bull"]>vals["base"]>vals["bear"]

def test_three_statements_and_sensitivity():
    h,b,a=load_inputs(); s=scenario_from_table(a,"base"); f=build_forecast(h,b,s)
    inc,bs,cf=forecast_three_statements(f,b)
    assert inc.index.equals(bs.index) and bs.index.equals(cf.index)
    assert np.allclose(cf.free_cash_flow,cf.cfo-cf.capex)
    sens=valuation_sensitivity(f,b,[.08,.09],[.025,.03],current_diluted_shares=float(h.loc[2025,"diluted_shares"]))
    assert len(sens)==4

def test_roic_is_finite():
    h,b,_=load_inputs()
    assert np.isfinite(roic_proxy(h,b))


def test_historical_balance_sheet_balances():
    _,b,_=load_inputs()
    assets=sum(float(b[k]) for k in ["cash","short_term_investments","accounts_receivable","prepaids","ppe","lease_assets","goodwill","intangibles","deferred_tax_assets","other_assets"])
    liabilities=sum(float(b[k]) for k in ["accounts_payable","accrued_liabilities","deferred_revenue","taxes_payable","lease_liabilities","other_liabilities","debt"])
    assert abs(assets-(liabilities+float(b["equity"])))<1e-6

def test_dcf_uses_current_not_forecast_share_count():
    h,b,a=load_inputs(); s=scenario_from_table(a,"base"); f=build_forecast(h,b,s)
    current=float(h.loc[2025,"diluted_shares"])
    d=dcf_value(f,b,s,current_diluted_shares=current)
    assert d["shares_for_valuation"]==current
    assert not np.isclose(current,float(f.shares.iloc[-1]))
