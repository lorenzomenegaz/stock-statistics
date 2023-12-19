import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime

ticker = str(input('Ticker: ')).upper() + '.SA'

df = pd.DataFrame(yf.download([ticker, '^BVSP'], '2015-01-01', datetime.now())).dropna()

df['ano'] = df.index.year

df_close = df['Close'].pct_change().dropna()
df_close['ano'] = df_close.index.year

retorno_anual_contra_ibov = df_close.groupby('ano').sum()

print(f'Retorno anual contra IBOVESPA: \n{retorno_anual_contra_ibov}\n')

def estatisticas(agrupamento):
    
    return {'min': agrupamento.min() * 100, 'max': agrupamento.max() * 100, 
            'media': agrupamento.mean() * 100, 'vol': agrupamento.std() * np.sqrt(252)}

estatisticas_por_ano = df.groupby('ano')['Close'].apply(estatisticas)

print(f'Estatísticas descritivas: \n{estatisticas_por_ano.describe()}\n')

acao = yf.download(ticker, '2015-01-01', datetime.now())

acao = pd.DataFrame(acao)

acao['ano'], acao['mes'] = acao.index.year, acao.index.month

acao['volume_financeiro'] = acao['Volume'] * acao['Close']

volume_medio_anual = acao.groupby(['ano'])['volume_financeiro'].mean()

volume_medio_anual = volume_medio_anual.astype(int)

print(f'Volume financeiro médio anual negociado pela empresa: \n{volume_medio_anual}\n')

maxdd = pd.DataFrame(acao)

maxdd['ano'] = maxdd.index.year

maxdd['maxima_do_ano'] = maxdd.groupby('ano')['Adj Close'].cummax()

maxdd['quedas'] = maxdd['Adj Close']/maxdd['maxima_do_ano'] - 1

retorno_maxdd = maxdd.groupby('ano')['quedas'].min()

print(f'Máximo drawndown por ano: \n{retorno_maxdd}\n')

cotacoes_ajustadas = df['Adj Close']

retornos = cotacoes_ajustadas.pct_change().dropna()

retornos['ano'] = retornos.index.year

retornos[f'{ticker}'].rolling(252).corr(retornos['^BVSP']).dropna().plot()

print(f'Gráfico de correlação x IBOVESPA em 252 dias: \n{retornos}\n')
