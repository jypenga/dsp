import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def HEARTRATE(patient, heart_rate):

    # hier niks aan veranderen
    return [cstm.AppHeader(top_left='Hartslag', top_right='header-icon-heartrate.svg', top_right_id='app-header-icon-transparent'),

    # hier relatief weining shit aan toevoegen
    html.Div([html.H1('Pindakaas'), cstm.HrTable(patient, round(heart_rate.mean()))],
    className='app-body'),

    # hier niks aan veranderen
    cstm.AppFooter(buttons=True)]

