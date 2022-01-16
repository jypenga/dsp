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
        dcc.Link('Wachtwoord vergeten?', href='/patienten', id='free-link-1'),
        dcc.Link('Nog geen account?', href='/registreren', id='free-link-2')],
className='app-body'),
cstm.RegisterFooter()
]