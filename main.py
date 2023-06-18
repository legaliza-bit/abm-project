from model import EconomyModel
import numpy as np


seed = np.random.seed(0)

if __name__ == '__main__':
    model = EconomyModel()
    for i in range(50):
        model.step()
    gini = model.datacollector.get_model_vars_dataframe()
    gini.plot()

    agent_rep = model.datacollector.get_agent_vars_dataframe()
    agent_rep.to_csv('agent_reporters.csv')
