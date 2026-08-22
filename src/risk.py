import numpy as np


def get_max_streak(condition_mask):
    if not np.any(condition_mask):
        return 0

    padded = np.pad(condition_mask, (1, 1), mode="constant", constant_values=False)
    edges = np.diff(padded.astype(int))

    starts = np.where(edges == 1)[0]
    ends = np.where(edges == -1)[0]

    streaks = ends - starts

    return int(np.max(streaks))


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

    winning_days = np.sum(returns > 0)
    losing_days = np.sum(returns < 0)

    longest_winning_streak = get_max_streak(returns > 0)
    longest_losing_streak = get_max_streak(returns < 0)

    maximum_recovery_days = get_max_streak(drawdown < 0)

    vol_penalty = np.clip(annulalized_volatility / 0.50, 0, 1) * 33.33

    dd_penalty = np.clip(abs(maximum_drawdown))

    rec_penalty = np.clip(maximum_recovery_days / 252, 0, 1) * 33.33

    risk_score = vol_penalty + dd_penalty + rec_penalty

    if risk_score < 33:
        risk_level = "Low"
    elif risk_score < 66:
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
        "winning_days": int(winning_days),
        "losing_days": int(losing_days),
        "longest_winning_streak": longest_winning_streak,
        "longest_losing_streak": longest_losing_streak,
        "maximum_recovery_days": maximum_recovery_days,
        "risk_score": float(risk_score),
        "risk_level": risk_level,
    }


def display_risk(risk_data):
    print("\n" + "━" * 60)
    print(" 🛡️ RISK & DRAWDOWN ENGINE")
    print("━" * 60)

    print(f"{'Daily Volatility':30}- {(risk_data['daily_volatility'])*100:.2f}%")
    print(
        f"{'Annualized Volatility':30}- {(risk_data['annualized_volatility'])*100:.2f}%"
    )
    print(f"{'Maximum Daily Gain':30}- {(risk_data['maximum_daily_gain'])*100:.2f}%")
    print(f"{'Maximum Daily Loss':30}- {(risk_data['maximum_daily_loss'])*100:.2f}%")
    print(f"{'Downside Volatility':30}- {(risk_data['downside_volatility'])*100:.2f}%")
    print(f"{'Maximum Downside':30}- {(risk_data['maximum_drawdown'])*100:.2f}%")
    print(f"{'Average Downside':30}- {(risk_data['average_drawdown'])*100:.2f}%")
    print("-" * 60)
    print(f"{'Winning Days':30}- {risk_data['winning_days']}")
    print(f"{'Losing Days':30}- {risk_data['losing_days']}")
    print(f"{'Longest Winning Streak':30}- {risk_data['longest_winning_streak']} days")
    print(f"{'Longest Losing Streak':30}- {risk_data['longest_losing_streak']} days")
    print(f"{'Max Recovery Time':30}- {risk_data['maximum_recovery_days']} days")
    print("-" * 60)
    print(f"{'Composite Risk Score':30}- {risk_data['risk_score']:.2f} / 100")
    print(f"{'Risk Level':30}- {risk_data['risk_level']}")