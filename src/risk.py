import numpy as np


def calculate_risk(stock, returns):
    close = stock["close"]
    if len(returns) == 0 or len(close) == 0:
        return None

    daily_volatility = np.std(returns, ddof=1)
    annulalized_volatility = daily_volatility * np.sqrt(252)
    maximum_daily_gain = np.max(returns)
    maximum_daily_loss = np.min(returns)

    negative_returns = returns[returns < 0]
    if len(negative_returns) > 0:
        downside_volatility = np.std(negative_returns, ddof=1)
    else:
        downside_volatility = 0

    running_max = np.maximum.accumulate(close)

    drawdown = (close - running_max) / running_max
    maximum_drawdown = np.min(drawdown)
    average_drawdown = np.mean(drawdown)

    if annulalized_volatility < 0.20:
        risk_level = "Low"
    elif annulalized_volatility < 0.40:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "daily_volatility": daily_volatility,
        "annualized_volatility": annulalized_volatility,
        "maximum_daily_gain": maximum_daily_gain,
        "maximum_daily_loss": maximum_daily_loss,
        "downside_volatility": downside_volatility,
        "maximum_drawdown": maximum_drawdown,
        "average_drawdown": average_drawdown,
        "risk_level": risk_level,
    }


def display_risk(company_name, risk_data):
    print("=" * 60)
    print(f"{company_name:^60}")
    print("=" * 60)

    print(f"{'Daily Volatility':30}- {(risk_data['daily_volatility'])*100:.2f}%")
    print(
        f"{'Annualized Volatility':30}- {(risk_data['annualized_volatility'])*100:.2f}%"
    )
    print(f"{'Maximum Daily Gain':30}- {(risk_data['maximum_daily_gain'])*100:.2f}%")
    print(f"{'Maximum Daily Loss':30}- {(risk_data['maximum_daily_loss'])*100:.2f}%")
    print(f"{'Downside Volatility':30}- {(risk_data['downside_volatility'])*100:.2f}%")
    print(f"{'Maximum Downside':30}- {(risk_data['maximum_drawdown'])*100:.2f}%")
    print(f"{'Average Downside':30}- {(risk_data['average_drawdown'])*100:.2f}%")
    print(f"{'Risk Level':30}- {risk_data['risk_level']}")
