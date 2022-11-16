from ejemplo2_add_space.money_model import MoneyModel
import matplotlib.pyplot as plt


def basic_example_space():
    # empty_model = MoneyModel(10)
    # empty_model.step()

    model = MoneyModel(50, 10, 10)
    for i in range(20):
        model.step()

    agent_wealth = [a.wealth for a in model.schedule.agents]
    print(agent_wealth)

    plt.hist(agent_wealth)
    plt.show()