import numpy as np


def rank_by_annual_return(momentum_result):
    ranking = sorted(
        momentum_result.items(), key=lambda item: item[1]["annual_return"], reverse=True
    )

    return ranking


def display_rank_by_annual_return(annual_return_ranking_data):
    print("\n" + "=" * 60)
    print(f"{'ANNUAL RETURN RANKING':^60}")
    print("=" * 60)

    for rank, (company, data) in enumerate(annual_return_ranking_data, start=1):
        print(f"{rank:02}. {company:20}{data['annual_return']:.2f}%")


def rank_by_annual_volatility(risk_result):
    ranking = sorted(
        risk_result.items(),
        key=lambda item: item[1]["annualized_volatility"],
        reverse=False,
    )
    return ranking


def display_rank_by_annual_volatility(annual_volatility_ranking_data):
    print("\n" + "=" * 60)
    print(f"{'Annual Volatility(Risk) - LOWEST TO HIGHEST':^60}")
    print("=" * 60)

    for rank, (company, data) in enumerate(annual_volatility_ranking_data, start=1):
        print(f"{rank:02}. {company:20}{data['annualized_volatility']*100:.2f}%")


def rank_by_annual_volume(volume_result):
    ranking = sorted(
        volume_result.items(), key=lambda item: item[1]["average_volume"], reverse=True
    )
    return ranking


def display_rank_by_annual_volume(annual_volume_ranking_data):
    print("\n" + "=" * 60)
    print(f"{'Annual Average Volume Ranking':^60}")
    print("=" * 60)

    for rank, (company, data) in enumerate(annual_volume_ranking_data, start=1):
        print(f"{rank:02}. {company:20}{data['average_volume']:.2f}")


def rank_by_average_price(statistics_result):
    ranking = sorted(
        statistics_result.items(),
        key=lambda item: item[1]["average_price"],
        reverse=True,
    )
    return ranking


def display_rank_by_average_price(average_price_ranking_data):
    print("\n" + "=" * 60)
    print(f"{'Annual Average Price Ranking':^60}")
    print("=" * 60)

    for rank, (company, data) in enumerate(average_price_ranking_data, start=1):
        print(f"{rank:02}. {company:20}{data['average_price']:.2f}")


def create_comparison_data(momentum_result, risk_result, volume_result):
    comparison_data = {}

    for company in momentum_result:

        comparison_data[company] = {
            "annual_return": momentum_result[company]["annual_return"],
            "annualized_volatility": risk_result[company]["annualized_volatility"],
            "average_volume": volume_result[company]["average_volume"],
        }

    return comparison_data


def normalize_higher_is_better(values):
    min_values = np.min(values)
    max_values = np.max(values)

    if max_values == min_values:
        return np.ones(len(values))

    return (values - min_values) / (max_values - min_values)


def normalize_lower_is_better(values):
    min_values = np.min(values)
    max_values = np.max(values)

    if max_values == min_values:
        return np.ones(len(values))

    return (max_values - values) / (max_values - min_values)


def calculate_overall_ranking(comparison_data):
    companies = np.array(list(comparison_data.keys()))
    returns = np.array([data["annual_return"] for data in comparison_data.values()])
    volatility = np.array(
        [data["annualized_volatility"] for data in comparison_data.values()]
    )
    volume = np.array([data["average_volume"] for data in comparison_data.values()])

    return_score = normalize_higher_is_better(returns)
    stability_score = normalize_lower_is_better(volatility)
    volume_score = normalize_higher_is_better(volume)

    overall_score = return_score * 0.50 + stability_score * 0.30 + volume_score * 0.20

    ranking_indices = np.argsort(overall_score)[::-1]

    overall_ranking = []

    for rank, index in enumerate(ranking_indices, start=1):

        overall_ranking.append(
            {
                "rank": rank,
                "company": companies[index],
                "overall_score": overall_score[index],
                "return_score": return_score[index],
                "stability_score": stability_score[index],
                "volume_score": volume_score[index],
            }
        )

    return overall_ranking


def display_overall_company_ranking(overall_ranking):
    print("\n" + "=" * 70)
    print(f"{'OVERALL COMPANY RANKING':^70}")
    print("=" * 70)

    print(
        f"{'Rank':<8}"
        f"{'Company':<20}"
        f"{'Return':<12}"
        f"{'Stability':<12}"
        f"{'Volume':<12}"
        f"{'Score':<10}"
    )

    print("-" * 70)

    for data in overall_ranking:

        print(
            f"{data['rank']:<8}"
            f"{data['company']:<20}"
            f"{data['return_score']:<12.2f}"
            f"{data['stability_score']:<12.2f}"
            f"{data['volume_score']:<12.2f}"
            f"{data['overall_score']:<10.2f}"
        )