#!/usr/bin/env python3

import re
import pandas as pd
from datetime import datetime


def read_input():
    with open('./input.txt', 'r') as input:
        for line in input:
            yield line


def parse_log(input):
    pattern = r'^\[([0-9 -:]+)\] ((Guard #)([0-9]+) )?(.*)$'
    _log_parts = re.search(pattern, input).groups()
    return [
        datetime.strptime(
            _log_parts[0],
            '%Y-%m-%d %H:%M'),
        _log_parts[3],
        _log_parts[4]
    ]


def get_time_asleep(df):
    df['snooze_duration'] = df['date'] - df['snooze_time']
    df = df[df['action'] == 'wakes up'].groupby(['guard']).sum()
    df = df['snooze_duration']
    df = pd.DataFrame(df, df.index)

    return df


def get_minute_most_asleep(df):
    df['snooze_duration'] = df['date'] - df['snooze_time']
    return None


def main():
    log = []
    for line in read_input():
        log.append(parse_log(line))

    log = pd.DataFrame(log)
    log.columns = ['date', 'guard', 'action']
    log = log.sort_values(
        by=['date']
    )
    log['guard'] = log['guard'].fillna(method='ffill')
    log['snooze_time'] = log['date'].shift(1)

    nap_log = get_time_asleep(log).sort_values(
        by=['snooze_duration'],
        ascending=False
    )

    minute = get_minute_most_asleep(
        log[
            (log['action'] == 'wakes up') &
            (log['guard'] == nap_log['guard'].iloc[0])
        ]
    )

    print(nap_log.head())


if __name__ == '__main__':
    main()
