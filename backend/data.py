import pandas as pd
import datetime as dt

from .select import *
from datetime import datetime
from scipy.stats import linregress

COLUMNS = ['index', 'patient', 'date', 'month', 'day', 'year', 'hour', 'minute', 'steps', 'heartrate', 'sleep', 'bp_upper', 'bp_lower', 'score']

def get_steps_data(pid):
    pkg = {}

    raw = get_all_patient_vitals(pid)

    df = pd.DataFrame(raw, columns=COLUMNS)
    df.date = df.date.apply(lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S'))

    tmp = df.loc[(df.month == 4) & (df.day == 12) & (df.year == 2016)]
    hist = tmp.groupby('hour').steps.sum()

    pkg['hist_x'] = hist.index
    pkg['hist_y'] = hist.rolling(1).mean()

    graph = df.groupby(df.date.dt.date).steps.sum()
    old_x = graph.index
    graph.index = graph.index.map(dt.date.toordinal)

    pkg['graph_x'] = old_x
    pkg['graph_y'] = graph

    pkg['mean'] = graph.mean()

    slope, _, _, _, _ = linregress(graph.index, graph.values)
    pkg['trend'] = slope

    return pkg