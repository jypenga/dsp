import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def PATIENTS(name, patients):
    return [cstm.AppHeader(top_left='Patienten', top_left_sub=name, middle=len(patients), middle_sub='Patienten', top_right='header-icon-patients.svg'),
    html.Div([html.H2('Jouw patienten'), cstm.PatientTable(patients)],
    className='app-body'),
    cstm.AppFooter(buttons=False)]