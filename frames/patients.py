import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def PATIENTS(name, patients, scores):
    return [cstm.AppHeader(top_left='Patienten', top_left_sub=name, middle=len(patients), middle_sub='Patienten', top_right='header-icon-patients.svg'),
    html.Div(html.Div(cstm.PatientTable(patients, scores), id={'type':'refresh-body', 'index':'patients'}),
    className='app-body'),
    html.Button('+', id={'type':'add-button', 'index':'patients'}, className='add-button'),
    cstm.AppFooter(buttons=False)]