import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def LOGS(date, patient, logs):
    return [cstm.AppHeader(middle_sub=patient[2], top_left='Logboek', top_left_sub=date, top_right='avatar-m.png', top_right_id='app-header-avatar'),
    html.Div(html.Div([cstm.LogsTable(patient, logs)], id='log-body'),
    className='app-body'),
    html.Button('+', id={'type':'add-button', 'index':'log'}, className='add-button'),
    cstm.AppFooter(buttons=True)]