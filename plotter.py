import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3
import numpy as np
import json

credentials = json.loads(open('credentials.json', 'r').read())
plotly.tools.set_credentials_file(username=credentials['username'], api_key=credentials['api_key'])
conn = sqlite3.connect('nutrients.db')

c = conn.cursor()

col_names= ['Livsmedelsnamn', 'Protein_g', 'kcal', 'Fett_g', 'Kolhydrater_g']
rows = c.execute('SELECT {}, {} ,{}, {}, {} from livsmedel order by Livsmedelsnamn'.format(*col_names))

name, prot, kcal, fat, carb = list(map(list, list(zip(*rows))))


N = len(prot)

x = prot
y = fat

norm_x = 255/max(x)
norm_y = 255/max(y)

color = ['rgb({},{},0)'.format(r*norm_x,g*norm_y) for r,g in zip(x,y)]

trace0=go.Scatter(
        x=x,
        y=y,
        text=name,
        mode='markers',
        marker=dict(
            color=color
            )
        )
layout = go.Layout(hovermode='closest')

data = [trace0]
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='food-protx-kcaly')
