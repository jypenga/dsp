import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

REGISTER = [
cstm.RegisterHeader(),
html.Div([html.H2('Registreren als Mantelzorger'),
    cstm.RegisterTable(),
    html.Button('REGISTREREN', id='register-button'),
    dcc.Link('Al geregistreerd?', href='/login')
    ], 
className='app-body'),
cstm.RegisterFooter()
]