import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def PROFILE(patient):
    return [cstm.AppHeader(middle_sub=patient[2], top_left='Patient Profiel', top_right='avatar-m.png', top_right_id='app-header-avatar', profile=True),
    html.Div(html.Div([], id='profile-body'),
    className='app-body'),
    html.Button('+', id={'type':'add-button', 'index':'medical'}, className='add-button'),
    cstm.AppFooter(buttons=True)]