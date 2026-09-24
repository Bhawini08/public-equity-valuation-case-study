import numpy as np
from equity_case.model import load_inputs,scenario_from_table,build_forecast,dcf_value,valuation_sensitivity,roic_proxy
from equity_case.statements import forecast_three_statements

def test_scenarios_build_and_dcf_ordering():
    h,b,a=load_inputs()
    vals={}
    for name in ["bear","base","bull"]:
        s=scenario_from_table(a,name); f=build_forecast(h,b,s); d=dcf_value(f,b,s)
        assert len(f)==5 and (f.revenue>0).all() and (f.fcff>0).all()
        assert np.isfinite(d["value_per_share"])
        vals[name]=d["value_per_share"]
    assert vals["bull"]>vals["base"]>vals["bear"]

def test_three_statements_and_sensitivity():
    h,b,a=load_inputs(); s=scenario_from_table(a,"base"); f=build_forecast(h,b,s)
    inc,bs,cf=forecast_three_statements(f,b)
    assert inc.index.equals(bs.index) and bs.index.equals(cf.index)
    assert np.allclose(cf.free_cash_flow,cf.cfo-cf.capex)
    sens=valuation_sensitivity(f,b,[.08,.09],[.025,.03])
    assert len(sens)==4

def test_roic_is_finite():
    h,b,_=load_inputs()
    assert np.isfinite(roic_proxy(h,b))
