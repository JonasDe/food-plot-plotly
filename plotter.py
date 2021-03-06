import plotly
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from itertools import permutations

import plotly.graph_objs as go
import sqlite3
import numpy as np
import json

def labelize(s):
    return s.split('_')[0]




def gen_trace(name, x,y, size, color, visible=False):
    global cfg, max_s_in_dataset, max_c_in_dataset
    max_size  = cfg['max_size']
    min_size  = cfg['min_size']
    max_color = cfg['color_scale']['max']
    norm_b    = max_color/max_c_in_dataset
    norm_size = max_size/max_s_in_dataset
    R = cfg['color_scale']['R']
    G = cfg['color_scale']['G']
    B = cfg['color_scale']['B']
    

    color = ['rgb({},{},{})'.format(norm_b*c*R,norm_b*c*G, norm_b*c*B) for c in color]
    size = [max(min_size, norm_size*s) for s in size]

    return go.Scatter(
            x=x,
            y=y,
            text=name,
            mode='markers',
            visible=visible,
            marker=dict(
                color=color,
                size=size
                )
            )

def menus(labels=[("None", 0)]):
    size = len(labels)
    def button(idx, name, val):
        visible = [b==idx for b  in range(size)]
        label_str = "<={}g {}"
        return dict(label = label_str.format(val, name),
                method = 'update',
                args = [{'visible': visible },
                    {'title': label_str.format(val, labelize(name))}]
                )
    return list([
        dict(type="buttons",
             active=0,
             buttons=list([button(i, labels[i][0], labels[i][1]) for i in range(size)]),)

    ])

def filtered_trace(lists, threshold=0, filter_idx=0, visible=False):
    n,x,y,size,color = lists
    lists = lists[1:]
    filter_list = lists[filter_idx]
    min_v = min(filter_list)
    max_v = max(filter_list)
    indices = [i for i in range(len(filter_list)) if 100*((filter_list[i]-min_v)/(max_v-min_v)) <= threshold]
    x          = [x[i] for i in indices]
    y          = [y[i] for i in indices]
    size       = [size[i] for i in indices]
    color      = [color[i] for i in indices]
    n          = [n[i] for i in indices]
    cutoff_val = (max_v-min_v)*threshold/100
    return (gen_trace(n,x,y,size,color, visible), cutoff_val)

def flatten(l):
    return [item for sublist in l for item in sublist]

def filtered_category(lists, resolution=4, dimension=0):
    filtered_trace_data = [filtered_trace(lists, (100/resolution)*i, dimension, dimension==0 and i == 1) for i in range(1, resolution+1)]
    traces = [filtered_trace_data[i][0] for i in range(len(filtered_trace_data))]
    cutoffs = [filtered_trace_data[i][1] for i in range(len(filtered_trace_data))]
    return traces, cutoffs


def load():
    global cfg
    cfg = json.loads(open('cfg.json', 'r').read())
    conn = sqlite3.connect('nutrients.db')
    c = conn.cursor()
    col_names= ['Livsmedelsnamn', cfg['x'], cfg['y'], cfg['size_axis'], cfg['color_axis']]
    rows = c.execute('SELECT {}, {} ,{}, {}, {} from livsmedel order by Livsmedelsnamn'.format(*col_names))

    cols  = list(map(list, list(zip(*rows))))
    names = list(map(labelize, col_names[1:]))
    N     = len(cols[0])
    return cols, names, N



def gen_plt(cols, names, N):
    resolution = cfg['resolution']
    margin = 1.1
    dimensions = len(names)
    cutoffs = []
    traces = []
    for i in range(dimensions):
        trace, cutoff = filtered_category(cols, resolution=resolution, dimension=i) 
        traces.extend(trace)
        cutoffs.extend(cutoff)

    name_labels = [[i]*resolution for i in names]
    button_labels = list(zip(flatten(name_labels),cutoffs))
    updatemenus = menus(button_labels)
    layout = go.Layout(hovermode='closest', updatemenus=updatemenus,
            xaxis=dict(title=names[0], range=[0,max_x*margin]),
            yaxis=dict(title=names[1], range=[0,max_y*margin]),
            
            )
    data = traces
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename='food')

def main():
    global cfg, max_x, max_y, resolution, max_s_in_dataset, max_c_in_dataset
    cols, names, N = load()
    max_x = max(cols[1])
    max_y = max(cols[2])
    max_s_in_dataset = max(cols[3])
    max_c_in_dataset = max(cols[4])

    gen_plt(cols, names, N)

if __name__ == '__main__':
    main()
