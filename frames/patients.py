import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def PATIENTS(name):
    return [cstm.AppHeader(top_left_sub=name),
    html.Div([html.H2('Jouw patienten'),],
    className='app-body'),]
# cstm.AppFooter()