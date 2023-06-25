from model import EconomyModel
import numpy as np

'''
An example of how to run the model to get agent reporters as a pd dataframe.
'''

seed = np.random.seed(0)

if __name__ == '__main__':
    model = EconomyModel()
    for i in range(50):
        model.step()

    agent_rep = model.datacollector.get_agent_vars_dataframe()
    agent_rep.to_csv('agent_reporters.csv')
