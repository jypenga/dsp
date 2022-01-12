import dash

from dash import dcc
from dash import html


class Custom():
    def __init__(self):
        self.app = dash.Dash(__name__)


    def RegisterHeader(self):
        content = html.Div([
                    html.Div([], 
                    className='register-header-oval'), 
                    html.Img(src=self.app.get_asset_url('logo-home.svg'), 
                    id='register-header-icon'),
                    html.Div([
                        html.H1('MoniZorg'),
                        html.P('ZORGEN MOET JE DOEN, NIET MAKEN')], 
                        className='register-header-text')], 
                className='register-header')
        return content


    def RegisterFooter(self):
        content = html.Div([], 
                    className='register-footer')
        return content


    def RegisterTable(self):
        content = html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-user.svg'))), html.Td('Naam'), html.Td(dcc.Input(id='input-user', type='text'))]),
                html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-age.svg'))), html.Td('Leeftijd'), html.Td(dcc.Input(id='input-age', type='number'))]),
                html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-sex.svg'))), html.Td('Geslacht'), html.Td(dcc.Dropdown(id='input-sex', options=[{'label':'man', 'value':'m'}, {'label':'vrouw', 'value':'v'}, {'label':'anders', 'value':'a'}], placeholder='', clearable=False))]),
                html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-email.svg'))), html.Td('Email'), html.Td(dcc.Input(id='input-email', type='email'))]),
                html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-phone.svg'))), html.Td('Tel.'), html.Td(dcc.Input(id='input-phone', type='tel'))]),
                html.Tr(html.Td(dcc.Checklist(id='input-privacy', options=[{'label':' Ik ben het eens met de blablabla', 'value':'checked'}]), colSpan=3))
                ]), id='app-register-table')
        return content


    def LoginTable(self):
        content = [html.Table(html.Tbody([html.Tr(html.Td('Emailadres')), html.Tr(html.Td(dcc.Input(id='login-input-email', type='email')))]), className='login-table'),
                html.Table(html.Tbody([html.Tr(html.Td('Wachtwoord')), html.Tr(html.Td(dcc.Input(id='login-input-password', type='password')))]), className='login-table')]
        return content


    def AppHeader(self, color=None, middle=None, top_left=None, top_right=None):
        content = html.Div([
                    html.Div([], 
                    className='app-header-oval'), 
                    html.Img(src=self.app.get_asset_url('header-icon-patients.svg'), 
                    id='app-header-icon'),
                    html.Img(src=self.app.get_asset_url('header-icon-menu.svg'), 
                    id='app-header-menu'),
                    html.Div([
                        html.H1('Patienten'),
                        html.P('Bas van den Placeholder')], 
                        className='app-header-text-left'),
                    html.Div([
                        html.H1('4'),
                        html.P('Patienten')], 
                        className='app-header-text-middle')
                ], className='app-header')
        return content


    def AppFooter(self, color=None, buttons=True):
        content = None
        return content