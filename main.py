# This is a sample Python script.
import matlab as matlab
import scipy as scipy

import agent
import behaviour
import pandas as pd

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tempAgent = agent.TemperatureAgent
    lightAgent = agent.LightingAgent
    pplAgent = agent.PeopleAgent
    supAgent = agent.SupervisorAgent

    tempAgent.__init__(agent.TemperatureAgent, "SPADE", "SPADE", False)
    df = pd.read_excel('temp_sample.xlsx', index_col=0)
    tempAgent.set(agent.TemperatureAgent, "tempAgent", df)

    pplAgent.__init__(agent.PeopleAgent, "SPADE", "SPADE", False)
    df = pd.read_excel('temp_sample.xlsx', index_col=2)
    pplAgent.set(agent.PeopleAgent, "pplAgent", df)

    lightAgent.__init__(agent.LightingAgent, "SPADE", "SPADE", False)
    df = pd.read_excel('temp_sample.xlsx', index_col=1)
    lightAgent.set(agent.LightingAgent, "lightAgent", df)

    tempAgent.add_behaviour(agent.self, behaviour.OneShotBehaviour, None)
    lightAgent.add_behaviour(agent.self, behaviour.OneShotBehaviour, None)
    pplAgent.add_behaviour(agent.self, behaviour.OneShotBehaviour, None)
    supAgent.add_behaviour(agent.self, behaviour.FSMBehaviour, None)

    supAgent.start(agent.SupervisorAgent, True)
    eng = matlab.engine.start_matlab
    matlab.engine.find_matlab
    matlab.engine.connect_matlab
    eng.input(tempAgent.__getattribute__(agent.tempAgent,"values"), lightAgent.__getattribute__(agent.lightAgent,"values"), pplAgent.__getattribute__(agent.pplAgent,"values"))

    supAgent.__init__(agent.SupervisorAgent, "SPADE", "SPADE", False)
    df = scipy.io.loadmat('file.mat')
    supAgent.set(agent.SupervisorAgent, "supAgent", df)

    while supAgent.is_alive(agent.SupervisorAgent):
        df = scipy.io.loadmat('file.mat')
        if not df is None:
          supAgent.set(agent.SupervisorAgent, "supAgent", df)
          if not tempAgent.is_alive(agent.TemperatureAgent):
            tempAgent.start(agent.TemperatureAgent, True)
          if not pplAgent.is_alive(agent.PeopleAgent):
            pplAgent.start(agent.PeopleAgent, True)
           if not lightAgent.is_alive(agent.LightingAgent):
            lightAgent.start(agent.LightingAgent, True)
        else:
          supAgent.stop(supAgent.self)
          tempAgent.stop(tempAgent.self)
          pplAgent.stop(pplAgent.self)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
