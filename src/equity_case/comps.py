import pandas as pd

def implied_values(peer_table:pd.DataFrame,target_ebitda,target_net_income,target_net_debt,target_shares):
    rows=[]
    for metric,col in [("EV/EBITDA","ev_ebitda"),("P/E","pe")]:
        vals=peer_table[col].dropna()
        med=float(vals.median())
        if metric=="EV/EBITDA":
            enterprise=med*target_ebitda; equity=enterprise-target_net_debt
        else:
            equity=med*target_net_income
        rows.append({"method":metric,"median_multiple":med,"implied_equity_value":equity,
                     "implied_value_per_share":equity/target_shares})
    return pd.DataFrame(rows)
