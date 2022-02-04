import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def STEPS(date, patient, steps_data):
    return [cstm.AppHeader(top_left='Beweging', top_left_sub=date,  middle=round(sum(steps_data['hist_x'])/len(steps_data['hist_x']), 1), middle_sub='stappen / uur', top_right='header-icon-heartrate.svg', top_right_id='app-header-icon-transparent'),

    html.Div(html.Div([*cstm.DataTable(steps_data)], className='data-body'),
    className='app-body'),
    cstm.AppFooter(buttons=True)]

