import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

def CALENDAR(date, patient):
    return [cstm.AppHeader(middle='4', middle_sub='To Do', top_left='Agenda', top_left_sub=date, top_right='avatar-m.png', top_right_id='app-header-avatar'),
    html.Div(html.Div([cstm.Calendar()], id='calendar-body'),
    className='app-body'),
    html.Button('+', id={'type':'add-button', 'index':'calendar'}, className='add-button'),
    cstm.AppFooter(buttons=True)]