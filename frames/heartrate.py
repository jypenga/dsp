import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def HEARTRATE(name, patients):

    # hier niks aan veranderen
    return [cstm.AppHeader(top_left='Patienten', top_left_sub=name, middle=len(patients), middle_sub='Patienten', top_right='header-icon-patients.svg'),

    # hier relatief weining shit aan toevoegen
    html.Div([],
    className='app-body'),

    # hier niks aan veranderen
    cstm.AppFooter(buttons=False)]