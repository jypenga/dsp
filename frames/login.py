import sys

from dash import dcc
from dash import html

sys.path.insert(0, '../')
from templates.main import Custom

cstm = Custom()

LOGIN = [
cstm.RegisterHeader(),
html.Div([html.H2('Inloggen'),
        *cstm.LoginTable(),
        html.Button('INLOGGEN', id='login-button'),
        dcc.Link('Wachtwoord vergeten?', href='/patienten')],
className='app-body'),
cstm.RegisterFooter()
]