import plotly.offline as pyo
import plotly.graph_objects as go
import pandas as pd
#import numpy as np

from plotly.subplots import make_subplots

#wczytaj dane
kghm_data = pd.read_csv('kgh_d.csv', parse_dates=True)
cuprum_data = pd.read_csv('ca_c_f_d.csv', parse_dates=True)
#połącz dane
merged_data = pd.merge(kghm_data[['Data', 'Zamkniecie']], cuprum_data[['Data', 'Zamkniecie']], 
                       on='Data', how='outer', suffixes=('_kghm', '_cuprum'))
merged_data.sort_values(by='Data', ascending=False, inplace=True)


#utwórz figurę jako make_subplots
fig = make_subplots(rows=3,cols=1,subplot_titles=['KGHM','Miedź'],shared_xaxes=True,
                    specs=[[{"type": "scatter"}], [{"type": "scatter"}], [{"type": "table"}]])

#dodaj wykresy
fig.add_trace(go.Scatter(x=kghm_data['Data'],
                         y=kghm_data['Zamkniecie'],
                         name='KGHM'
                         ),1,1)

fig.add_trace(go.Scatter(x=cuprum_data['Data'],
                         y=cuprum_data['Zamkniecie'],
                         name='Miedź'
                         ),2,1)

#dodaj tabelę jako trzeci wykres
fig.add_trace(go.Table(header=dict(values=['Data','KGHM','Miedź'],
                                   font=dict(weight='bold')),
                       cells=dict(values=[merged_data['Data'], 
                                          merged_data['Zamkniecie_kghm'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-"), 
                                          merged_data['Zamkniecie_cuprum'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")
                                          ],
                                  align=['left', 'left', 'left'])
                       ),3,1)

#sformatuj wykresy
fig.update_layout(title='Ceny zamknięcia akcji KGHM oraz miedzi',
                  showlegend=False,
                  yaxis=dict(title="Cena w PLN"),
                  yaxis2=dict(title="Cena w PLN"))
#fig.update_xaxes(showticklabels=True, row=1, col=1)


#eksportuj
pyo.plot(fig,filename='result.html')