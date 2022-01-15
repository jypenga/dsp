import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def DASHBOARD(date, patient):
    return [cstm.AppHeader(middle_sub=patient[2], top_left='Dashboard', top_left_sub=date, top_right='avatar-m.png', top_right_id='app-header-avatar', dashboard=True),
    html.Div(html.Div([], id='dashboard-body'),
    className='app-body'),
    cstm.AppFooter(buttons=True)]