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


Available axis-fields:
Livsmedelsnamn
Livsmedelsnummer
kcal
kj
Kolhydrater_g
Fett_g
Protein_g
Fibrer_g
Vatten_g
Alkohol_g
Aska_g
Monosackarider_g
Disackarider_g
Sackaros_g
Fullkorn_totalt__g
Sockerarter_g
Summa_mättade_fettsyror_g
Fettsyra_g
Laurinsyra_g
Myristinsyra_g
Palmitinsyra_g
Stearinsyra_g
Arakidinsyra_g
Summa_enkelomättade_fettsyror_g
Palmitoljesyra_g
Oljesyra_g
Summa_fleromättade_fettsyror_g
Linolsyra_g
Linolensyra_g
Arakidonsyra_g
EPA_g
DPA_g
DHA_g
Kolesterol_mg
Retinol_ug
Vitamin_A_ug
beta_Karoten_ug
Vitamin_D_ug
Vitamin_E_mg
Vitamin_K_ug
Tiamin_mg
Riboflavin_mg
Vitamin_C_mg
Niacin_mg
Niacinekvivalenter_mg
Vitamin_B6_mg
Vitamin_B12_ug
Folat_ug
Fosfor_mg
Jod_ug
Järn_mg
Kalcium_mg
Kalium_mg
Koppar_mg
Magnesium_mg
Natrium_mg
Salt_g
Selen_ug
Zink_mg
Avfall
Stärkelse_g

### Using this setup with your own database

The python script connects to `nutrients.db`, and uses the `cfg.json` to extract relevant fields.

Just make sure your database contains whatever rows of numbers you wish to visualize, and add them to the config file.
Rename that database to nutrients.py and run `python3 plotter.py`. The html should then be auto generated.

Beware about using '_' in the field names though, since this is used as a separator for the labels in the plot.

