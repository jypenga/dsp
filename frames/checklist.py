import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def CHECKLIST(date, patient):
    return [cstm.AppHeader(middle='5', middle_sub='To Do', top_left='Checklist', top_left_sub=date, top_right='header-icon-checklist.svg', top_right_id='app-header-icon'),
    html.Div(html.Div([], id='checklist-body'),
    className='app-body'),
    cstm.AppFooter(buttons=True)]