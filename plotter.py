import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from itertools import permutations
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
relevant = [prot, fat, kcal, water]

N         = len(prot)


def gen_trace(x,y, size, color):
    max_size  = 20
    min_size  = 5
    max_color = 255

    norm_b    = max_color/max(color)
    norm_size = max_size/max(size)
    color = ['rgb(0,0,{})'.format(norm_b*c) for c in color]
    size = [max(min_size, norm_size*s) for s in size]

    return go.Scatter(
            x=x,
            y=y,
            text=name,
            mode='markers',
            marker=dict(
                color=color,
                size=size
                )
            )

def menus(buttons=4, name="unknown"):
    def button(idx):
        return dict(label = "{}% {}".format(idx*25, name),
                method = 'update',
                args = [{'visible': [b==idx for b  in range(buttons)]},
                    {'title': 'Food'}]
                )
    return list([
        dict(type="buttons",
             active=-1,
             buttons=list([button(i) for i in range(buttons)]),
        )

    ])

def filtered_trace(lists, threshold=0, filter_idx=0):
    x,y,size,color = lists

    filter_list = lists[filter_idx]
    # prot
    # max prot = 86
    min_v = min(filter_list)
    max_v = max(filter_list)

    indices = [i for i in range(len(filter_list)) if 100*((filter_list[i]-min_v)/(max_v-min_v)) >= threshold]
    x = [x[i] for i in indices]
    y = [y[i] for i in indices]
    print(y)
    print(x)

    return gen_trace(x,y,size,color), min_v, max_v

lists = [prot, fat, kcal, water]

filtered_trace_data = [filtered_trace(lists, 25*i) for i in [1,2,3,4]]
traces = [t[0] for t in filtered_trace_data]
labels = [mi-maxfor t,mi,ma, in filtered_trace_data]


updatemenus = menus(name="protein")

layout = go.Layout(hovermode='closest', updatemenus=updatemenus)

data = traces
fig = go.Figure(data=data, layout=layout)
plot(fig, filename='food-protx-kcaly')
