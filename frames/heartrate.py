import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def HEARTRATE(patient):

    # hier niks aan veranderen
    return [cstm.AppHeader(top_left='Hartslag', top_right='header-icon-heartrate.svg', top_right_id='app-header-icon-transparent'),

    # hier relatief weining shit aan toevoegen
    html.Div([html.H1('Volgens mij zitten de verschillende buttons allemaal op dezelfde plek. Morgen even oplossen met Jorit'), cstm.HrTable(patient)],
    className='app-body'),

    # hier niks aan veranderen
    cstm.AppFooter(buttons=True)]

