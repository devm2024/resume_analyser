import numpy as np
import pandas as pd

def tiervalue(df,fldname,uni_data):
    uni_rank = pd.read_excel('./University_rankings.xlsx')
    tier = uni_rank.loc[:,['Name of the institution','Tier']].to_records(index=False)
    d = {k:v for (k,v) in tier}
    df['tier'+'_'+fldname] = df[fldname].map(d)
    return df

