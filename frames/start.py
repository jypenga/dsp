import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

START = [
cstm.RegisterHeader(),
html.Div([
    html.P('Ben jij mantelzorger en heb je hulp nodig bij het verzorgen van jouw patient(en)?'),
    html.P('Met MoniZorg kun je gemakkelijk jouw patienten monitoren en de juiste zorg bieden die jouw patient op dat moment nodig heeft.'),
    dcc.Link('REGISTREREN', href='/registreren', id='app-free-btn')],
className='app-body'),
cstm.RegisterFooter()
]
