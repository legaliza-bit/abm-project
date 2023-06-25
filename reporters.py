def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.households]
    x = sorted(agent_wealths)
    N = len(model.households)
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B


def show_inf_actual(model):
    return model.inf_actual


def show_inf_ema(model):
    return model.inf_ema


def show_inf_expec(model):
    return model.inf_expec


def show_output(model):
    return model.firm.output


def show_demand(model):
    return model.agg_demand


def show_price(model):
    return model.firm.price


def show_rate(model):
    return model.cb.rate


def show_unemployment(model):
    return model.unemploymentss
