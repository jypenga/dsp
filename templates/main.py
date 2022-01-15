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


    def AppHeader(self, color=None, middle=None, middle_sub=None, top_left=None, top_left_sub=None, top_right=None, top_right_id='app-header-icon', dashboard=False):
        content = html.Div([
                    html.Div([], 
                    className='app-header-oval'), 
                    html.Img(src=self.app.get_asset_url(top_right), 
                    id=top_right_id),
                    html.Img(src=self.app.get_asset_url('header-icon-menu.svg'), 
                    id='app-header-menu'),
                    html.Div([
                        html.H1(top_left),
                        html.P(top_left_sub)], 
                        className='app-header-text-left'),
                    html.Div([
                        html.H1(middle),
                        html.P(middle_sub)], 
                        className='app-header-text-middle'),
                    html.Div([html.Button(html.H3('GEMONITORD'), id='dashboard-button-monitored', style={'border-bottom': '3px solid #3B72FF'}), html.Button(html.H3('HANDMATIG'), id='dashboard-button-manual')], className='dashboard-subheader') if dashboard else None,
                ], className='app-header', style={'box-shadow': 'rgba(0, 0, 0, 0.15) 0px 0px 50px 0px'} if dashboard else {})
        return content


    def AppFooter(self, color=None, buttons=True):
        if not buttons:
            return self.RegisterFooter()

        content = html.Div(html.Table(html.Tbody(html.Tr([html.Td(html.Img(src=self.app.get_asset_url('footer-icon-calendar.svg'))), 
                                                          html.Td(html.Img(src=self.app.get_asset_url('footer-icon-checklist.svg'))), 
                                                          html.Td(html.Div(html.Img(src=self.app.get_asset_url('footer-icon-dashboard.svg')), id='app-footer-dashboard-container-background'), id='app-footer-dashboard-container'), 
                                                          html.Td(html.Img(src=self.app.get_asset_url('footer-icon-notifications.svg'))), 
                                                          html.Td(html.Img(src=self.app.get_asset_url('footer-icon-profile.svg')))]))), 
                    className='app-footer')
        return content

    
    def PatientTable(self, patients):
        # group by 2
        tmp = None
        if len(patients) % 2 == 0:
            patients = list(zip(patients, patients[1:]))[::2]
        else:
            tmp = patients[-1]
            patients = patients[:-1] if len(patients) > 1 else []
            patients = list(zip(patients, patients[1:]))[::2]

        # create card
        def PatientCard(patient):
            avatar = 'avatar-m.png' if patient[4] == 'm' else 'avatar-f.png'
            return html.Td(html.Button(html.Div([html.Img(src=self.app.get_asset_url('smiley-positive.svg'), className='patient-card-smiley-score'),
                                    html.Img(src=self.app.get_asset_url(avatar)), 
                                    patient[2]], className='app-patient-card'), id={'type':'app-patient-card', 'index':patient[0]}))

        # create table from cards
        content = html.Table(html.Tbody([*[html.Tr([PatientCard(duo[0]), PatientCard(duo[1])]) for duo in patients], 
                                           html.Tr(PatientCard(tmp) if tmp else [])]), 
                                            id='app-patient-table')
        return content


    def DashboardListMonitored(self):
        tables = ['hartslag', 'saturatie', 'temperatuur', 'slaapscore']
        icons = ['heartbeat', 'saturation', 'temperature', 'sleep']
        colors = ['#fff0f4', '#e6eaff', '#ecfaff', '#fffaed']
        content = html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url(f'dashboard-icon-{icons[i]}.svg'), className='dashboard-icon'), className='dashboard-card-icon'), 
                                                  html.Td([html.H2(tables[i].title()), html.P('placeholder')], className='dashboard-card-text'), 
                                                  html.Td(html.Img(src=self.app.get_asset_url('smiley-positive.svg'), className='dashboard-card-smiley-score')), 
                                                  html.Td(html.Img(src=self.app.get_asset_url('icon-chevron.svg'), className='dashboard-card-expand'))], style={'background': f'radial-gradient(circle 10vh at 4% 50%, {colors[i]} 70%, transparent 70%)'}) for i in range(len(tables))]),
                                                  className='dashboard-table')
        return content


    def DashboardListManual(self):
        tables = ['bloeddruk', 'glucose', 'medicatie', 'voeding']
        icons = ['blood-pressure', 'glucose', 'medication', 'food']
        colors = ['#ffecec', 'white', '#ecf9f1', '#f6fef9']
        content = html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url(f'dashboard-icon-{icons[i]}.svg'), className='dashboard-icon'), className='dashboard-card-icon'), 
                                                  html.Td([html.H2(tables[i].title()), html.P('placeholder')], className='dashboard-card-text'), 
                                                  html.Td(html.Img(src=self.app.get_asset_url('smiley-positive.svg'), className='dashboard-card-smiley-score')), 
                                                  html.Td(html.Img(src=self.app.get_asset_url('icon-chevron.svg'), className='dashboard-card-expand'))], style={'background': f'radial-gradient(circle 10vh at 4% 50%, {colors[i]} 70%, transparent 70%)'}) for i in range(len(tables))]),
                                                  className='dashboard-table')
        return content