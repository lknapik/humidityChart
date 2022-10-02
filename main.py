from psychrochart import PsychroChart
import matplotlib.pyplot as plt
amb = __import__('ambient-weather-api.ambientweather_api')


def gen_grad(progress):
    rgb = [0,0,0,1]
    if(progress <= 0.5):
        progress *= 2
        rgb[0] = ((1-progress)+.5)
        rgb[1] = (progress + .5)
    else:
        progress = (progress*2)-1 
        rgb[1] = (1-progress)+.5
        rgb[2] = progress + .5

    if rgb[0]*1.1 >= 1:
        rgb[0] = 1
    if rgb[1]*1.1 >= 1:
        rgb[1] = 1
    if rgb[2]*1.1 >= 1:
        rgb[2] = 1   

    return rgb

#plot setup
custom_style = {
    "figure": {
        "figsize": [12, 8],
        "dpi": 1200,
        "base_fontsize": 12,
        "title": "My chart",
        "x_label": None,
        "y_label": None,
        "partial_axis": False
    },
    "limits": {
        "range_temp_c": [0, 40],
        "range_humidity_g_kg": [0, 20],
        "altitude_m": 900,
        "step_temp": .5
    },
    "saturation": {"color": [0, .3, 1.], "linewidth": 2},
    "constant_rh": {"color": [0.0, 0.498, 1.0, .7], "linewidth": 2.5,
                    "linestyle": ":"},
    "chart_params": {
        "with_constant_rh": True,
        "constant_rh_curves": [25, 50, 75],
        "constant_rh_labels": [25, 50, 75],
        
        "range_vol_m3_kg": [0.9, 1.],
        "constant_v_labels": [0.9, 0.94, 0.98],
        
        "with_constant_h": False,
        "with_constant_wet_temp": False,
        "with_zones": False
    }
}


# Get a preconfigured chart
chart = PsychroChart(custom_style)


# Plot the chart
ax = chart.plot(ax=plt.gca())

#Get data and convert
with open("data.csv", 'r') as f:
    rawData = f.readlines()

trimData = []
for line in rawData:
    dataList = line.split("\t")
    tempC = (float(dataList[1][:-3])-32.0)*(5.0/9.0)
    relHum = (float(dataList[3][:-2]))

    reqData = (dataList[0], tempC, relHum)
    trimData.append(reqData)

points = {}

dataLen = len(trimData)

for count, item in enumerate(trimData):

    points[item[0]] = {
                        'style': {'color': gen_grad( float(count/dataLen) ),
                                    'marker': '.', 'markersize': 5},
                        'xy': (item[1], item[2])}

chart.plot_points_dbt_rh(points)

# Add a legend
#chart.plot_legend(markerscale=.7, frameon=False, fontsize=10, labelspacing=1.2)
ax.get_figure()
plt.savefig("plt.pdf")