import mesa
import yaml
import numpy as np

from model import EconomyModel
from hist_module import HistogramModule

with open("params.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

config_model = config['model']


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if agent.wealth > 100:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.wealth > 0:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.4
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.2
    return portrayal


model_params = {
    "N": mesa.visualization.Slider(
        "Number of agents",
        1000,
        10,
        10000,
        10,
        description="Choose how many agents to include in the model",
    ),
    "r_base": mesa.visualization.Slider(
        "Baseline interest rate",
        config['model']['r_base'],
        0,
        1,
        0.01,
        description="Choose baseline rate",
    ),
    "intensity": mesa.visualization.Slider(
        "Intensity of Central Bank policy",
        config['model']['intensity'],
        0,
        1,
        0.1,
        description="Choose policy intensity",
    ),
    "inf_target": mesa.visualization.Slider(
        "Central Bank target rate",
        config['model']['inf_target'],
        0,
        1,
        0.05,
        description="Choose target rate",
    ),
    "trust": mesa.visualization.Slider(
        "Trust of agents to central bank",
        config['model']['trust'],
        0,
        1,
        0.1
    ),
}

width = int(np.sqrt(model_params["N"].value))
height = model_params["N"].value // width + 1

model_params["width"] = width
model_params["height"] = height


grid = mesa.visualization.CanvasGrid(
    agent_portrayal,
    model_params["width"],
    model_params["height"],
    500, 500
)
gini = mesa.visualization.ChartModule(
    [{"Label": "Gini", "Color": "Black"}],
    data_collector_name="datacollector"
)
inf = mesa.visualization.ChartModule(
    [{"Label": "Actual Inflation", "Color": "Black"},
     {"Label": "Inflation EMA", "Color": "Green"},
     {"Label": "Inflation Expectations", "Color": "Red"}],
    data_collector_name="datacollector"
)
gap = mesa.visualization.ChartModule(
    [{"Label": "Output", "Color": "Blue"},
     {"Label": "Demand", "Color": "Red"}]
)
price = mesa.visualization.ChartModule(
    [{"Label": "Price", "Color": "Blue"}]
)
hist = HistogramModule(
    bins=list(range(-100, 100, 10)),
    canvas_height=200,
    canvas_width=500
)

server = mesa.visualization.ModularServer(
    EconomyModel,
    [grid, gini, inf, gap, price, hist],
    "Economy Model",
    model_params
)

server.port = 8521
server.launch()
