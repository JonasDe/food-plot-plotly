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

col_names= ['Livsmedelsnamn', 'Protein_g', 'kcal', 'Fett_g', 'Kolhydrater_g', 'Vatten_g']
rows = c.execute('SELECT {}, {} ,{}, {}, {}, {} from livsmedel order by Livsmedelsnamn'.format(*col_names))

name, prot, kcal, fat, carb, water = list(map(list, list(zip(*rows))))


N         = len(prot)
x         = prot
y         = fat
size      = kcal
color_val = water
max_size  = 20
min_size  = 5
max_color = 255
# norm_x    = max_color/max(water)
# norm_y    = max_color/max(y)
norm_b    = max_color/max(water)
norm_size = max_size/max(size)



color = ['rgb(0,0,{})'.format(norm_b*w) for w in water]
size = [max(min_size, s*norm_size) for s in size]
trace0=go.Scatter(
        x=x,
        y=y,
        text=name,
        mode='markers',
        marker=dict(
            color=color,
            size=size
            )
        )
layout = go.Layout(hovermode='closest')

data = [trace0]
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='food-protx-kcaly')
