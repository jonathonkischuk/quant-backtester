import pandas as pd


def clean_price_data(data, is_df=False):
    if not is_df:
        df = pd.read_csv(data, index_col='Date', parse_dates=True)
    else:
        df = data.copy()
        if df.index.name != 'Date':
            df.index.name = 'Date'
    
    df.columns = [col.split("_")[0].capitalize().strip() for col in df.columns]
    
    df.dropna(inplace=True)
    df.sort_index(inplace=True)
    return df
