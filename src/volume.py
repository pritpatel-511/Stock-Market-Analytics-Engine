import numpy as np


def calculate_volume(stock):
    volume = stock["volume"]

    if len(volume) == 0:
        return None

    average_volume = np.mean(volume)
    highest_volume = np.max(volume)
    lowest_volume = np.min(volume)

    today = volume[1:]
    yesterday = volume[:-1]

    growth_mask = today > yesterday
    growth_days = np.sum(growth_mask)

    decline_mask = today < yesterday
    decline_days = np.sum(decline_mask)

    spike_threshold = average_volume * 1.5
    spike_mask = volume > spike_threshold
    volume_spike_days = np.sum(spike_mask)

    low_volume_threshold = average_volume * 0.5
    low_volume_mask = volume < low_volume_threshold
    low_volume_days = np.sum(low_volume_mask)

    return {
        "average_volume": average_volume,
        "highest_volume": highest_volume,
        "lowest_volume": lowest_volume,
        "volume_growth_days": growth_days,
        "volume_decline_days": decline_days,
        "volume_spike_days": volume_spike_days,
        "low_volume_days": low_volume_days,
    }


def display_volume_analysis(company_name, volume_data):
    print("=" * 60)
    print(f"{company_name:^60}")
    print("=" * 60)

    print(f"{'Average Volume':30}- {volume_data['average_volume']:.2f}")
    print(f"{'Highest Volume':30}- {volume_data['highest_volume']}")
    print(f"{'Lowest Volume':30}- {volume_data['lowest_volume']}")
    print(f"{'Volume Growth Days':30}- {volume_data['volume_growth_days']}")
    print(f"{'Volume Decline Days':30}- {volume_data['volume_decline_days']}")
    print(f"{'Volume Spike Days':30}- {volume_data['volume_spike_days']}")
    print(f"{'Low Volume Days':30}- {volume_data['low_volume_days']}")
