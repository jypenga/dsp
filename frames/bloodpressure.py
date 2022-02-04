import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def BLOODPRESSURE(patient, blood_pressure):
    return [cstm.AppHeader(top_left='Bloeddruk', middle=144, middle_sub='/ 80 mmHg', top_right='header-icon-heartrate.svg', top_right_id='app-header-icon-transparent'),

    html.Div(html.Div([*cstm.DataTable(cstm.BloodPressureHist(), cstm.BloodPressureGraph(), 'xd')], className='data-body'),
    className='app-body'),
    html.Button('+', id={'type':'add-button', 'index':'bloodpressure'}, className='add-button'),
    cstm.AppFooter(buttons=True)]

