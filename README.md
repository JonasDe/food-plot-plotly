### Plotting nutritional data with plot.ly


## CFG file

This is an example cfg file
```
{"resolution": 5,
    "x": "Protein_g",
    "y": "kcal",
    "size_axis": "Fett_g",
    "color_axis": "Vatten_g",
    "color_scale": {
        "R": false,
        "G": true,
        "B": true,
        "max": 255
    },
    "min_size": 5,
    "max_size": 20,
    "username": "Enter Here",
    "api_key": "Enter Api Key"
}
```
resolution:
Amount of intervals for sorting 
(5 = 20%/40%/60%/80%/100%, 
4 = 25%/50%/75%/100%, and so on)
The sort label will show sorting in grams, not percentage.

x:
Which field should be plotted against X-axis

y:
Which field should be plotted against Y-axis

size\_axis:
Which field should determine the size of the data points

color\_axis:
Which field should determine the color of the data points


color\_scale:
Which colors should be used for the color of data points. 
max: What is the largest RGB value for each of the color domains

min\_size:
minimum size of data points

max\_size:
minimum size of data points

username/api\_key:
if you want to push to plot.ly enter key here. N

