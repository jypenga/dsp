import dash

from dash import dcc
from dash import html

import base64
import svgwrite
import numpy as np


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


    def AppHeader(self, color=None, middle=None, middle_sub=None, top_left=None, top_left_sub=None, top_right=None, top_right_id='app-header-icon', dashboard=False, profile=False, checklist=False):
        if dashboard:
            subheader = html.Div([html.Button(html.H3('GEMONITORD'), id='dashboard-button-monitored', style={'borderBottom': '3px solid #3B72FF'}), html.Button(html.H3('HANDMATIG'), id='dashboard-button-manual')], className='dashboard-subheader')
            shadow = {'box-shadow': 'rgba(0, 0, 0, 0.15) 0px 0px 50px 0px'}
        elif profile:
            subheader = html.Div([html.Button(html.H3('INFO'), id='profile-button-info', style={'borderBottom': '3px solid #3B72FF'}), html.Button(html.H3('MEDISCH'), id='profile-button-medical'), html.Button(html.H3('VOEDING'), id='profile-button-food')], className='dashboard-subheader')
            shadow = {'box-shadow': 'rgba(0, 0, 0, 0.15) 0px 0px 50px 0px'}
        elif checklist:
            subheader = html.Div([html.Button(html.H3('MEDICATIE'), id='checklist-button-medical', style={'borderBottom': '3px solid #3B72FF'}), html.Button(html.H3('VOEDING'), id='checklist-button-food'), html.Button(html.H3('ONTWIKKELING'), id='checklist-button-development')], className='dashboard-subheader')
            shadow = {'box-shadow': 'rgba(0, 0, 0, 0.15) 0px 0px 50px 0px'}
        else:
            subheader = None
            shadow = {}

        content = html.Div([
                    html.Div([], className='app-header-oval'), 
                    html.Img(src=self.app.get_asset_url(top_right), id=top_right_id),
                    html.Button(html.Img(src=self.app.get_asset_url('header-icon-menu.svg')), id='app-header-button-menu'),
                    html.Div(html.Ul([html.Li(dcc.Link('Wissel patient', href='/patienten')), html.Li('Instellingen'), html.Li(html.Button('Log uit', id='app-header-button-logout'))]), id='app-header-menu-container', style={'display':'none'}),
                    html.Div([
                        html.H1(top_left),
                        html.P(top_left_sub)], 
                        className='app-header-text-left'),
                    html.Div([
                        html.H1(middle),
                        html.P(middle_sub)], 
                        className='app-header-text-middle'),
                    subheader,
                ], className='app-header', style=shadow)
        return content


    def AppFooter(self, color=None, buttons=True):
        if not buttons:
            return self.RegisterFooter()

        content = html.Div(html.Table(html.Tbody(html.Tr([html.Td(dcc.Link(html.Img(src=self.app.get_asset_url('footer-icon-calendar.svg')), href='/agenda')), 
                                                          html.Td(dcc.Link(html.Img(src=self.app.get_asset_url('footer-icon-checklist.svg')), href='/checklist')), 
                                                          html.Td(dcc.Link(html.Div(html.Img(src=self.app.get_asset_url('footer-icon-dashboard.svg')), id='app-footer-dashboard-container-background'), href='/dashboard'), id='app-footer-dashboard-container'), 
                                                          html.Td(dcc.Link(html.Img(src=self.app.get_asset_url('footer-icon-log.svg')), href='/logboek')), 
                                                          html.Td(dcc.Link(html.Img(src=self.app.get_asset_url('footer-icon-profile.svg')), href='/profiel'))]))), 
                    className='app-footer')
        return content

    
    def Notification(self, contents, result, index=0):
        src = self.app.get_asset_url('notification-icon-success.svg') if result else self.app.get_asset_url('notification-icon-failure.svg')
        contents = contents if result else 'Actie mislukt!'
        content = html.Div([html.Table(html.Tbody(html.Tr([html.Td(html.Img(src=src)), html.Td(html.P(contents))]))), 
        html.Button('x', id={'type':'close-notification-button', 'index':str(index)})], id={'type':'notification', 'index':str(index)}, className='notification') 
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

        content = [html.H2('Jouw patienten'), content]
        return content


    def DashboardListMonitored(self):
        tables = ['hartslag', 'saturatie', 'temperatuur', 'slaapscore', 'beweging']
        icons = ['heartbeat', 'saturation', 'temperature', 'sleep', 'activity']
        colors = ['#fff0f4', '#e6eaff', '#ecfaff', '#fffaed', '#e6f5da']
        content = html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url(f'dashboard-icon-{icons[i]}.svg'), className='dashboard-icon'), className='dashboard-card-icon'), 
                                                  html.Td([html.H2(tables[i].title()), html.P('placeholder')], className='dashboard-card-text'), 
                                                  html.Td(html.Img(src=self.app.get_asset_url('smiley-positive.svg'), className='dashboard-card-smiley-score')), 
                                                  html.Td(dcc.Link(html.Img(src=self.app.get_asset_url('icon-chevron.svg'), className='dashboard-card-expand'), href=f'/{tables[i]}'))], style={'background': f'radial-gradient(circle 10vh at 4% 50%, {colors[i]} 70%, transparent 70%)'}, className='dashboard-clickable-card') for i in range(len(tables))]),
                                                  className='dashboard-table')
        return content


    def DashboardListManual(self):
        tables = ['bloeddruk', 'glucose', 'medicatie', 'voeding']
        icons = ['blood-pressure', 'glucose', 'medication', 'food']
        colors = ['#ffecec', 'white', '#ecf9f1', '#f6fef9']
        content = html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url(f'dashboard-icon-{icons[i]}.svg'), className='dashboard-icon'), className='dashboard-card-icon'), 
                                                  html.Td([html.H2(tables[i].title()), html.P('placeholder')], className='dashboard-card-text'), 
                                                  html.Td(html.Img(src=self.app.get_asset_url('smiley-positive.svg'), className='dashboard-card-smiley-score')), 
                                                  html.Td(dcc.Link(html.Img(src=self.app.get_asset_url('icon-chevron.svg'), className='dashboard-card-expand'), href=f'/{tables[i]}'))], style={'background': f'radial-gradient(circle 10vh at 4% 50%, {colors[i]} 70%, transparent 70%)'}, className='dashboard-clickable-card') for i in range(len(tables))]),
                                                  className='dashboard-table')
        return content


    def ProfileTableInfo(self, patient):
        content = [html.H3('ALGEMENE INFORMATIE'),
                html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-user.svg'))), html.Td('Naam'), html.Td(dcc.Input(id='input-user', type='text', value=patient[2]))]),
                html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-age.svg'))), html.Td('Leeftijd'), html.Td(dcc.Input(id='input-age', type='number', value=patient[3]))]),
                html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-sex.svg'))), html.Td('Geslacht'), html.Td(dcc.Dropdown(id='input-sex', options=[{'label':'man', 'value':'m'}, {'label':'vrouw', 'value':'v'}, {'label':'anders', 'value':'a'}], placeholder='', clearable=False, value=patient[4]))]),
                html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-height.svg'))), html.Td('Lengte'), html.Td(dcc.Input(id='input-email', type='text', value=f'{patient[5]} m'))]),
                html.Tr([html.Td(html.Img(src=self.app.get_asset_url('icon-weight.svg'))), html.Td('Gewicht'), html.Td(dcc.Input(id='input-phone', type='text', value=f'{patient[6]} kg'))]),
                ]), id='app-register-table')]
        return content


    def ProfileTableMedical(self, patient, medication):
        content = [html.H3('ALGEMENE MEDISCHE INFORMATIE'),
                html.Table(html.Tbody([html.Tr([html.Td('Huisarts'), html.Td(dcc.Input(id='input-user', type='text', value=patient[9]))]),
                html.Tr([html.Td('Tel. huisarts'), html.Td(dcc.Input(id='input-age', type='text', value=patient[10]))]),
                html.Tr([html.Td('Zorgverzekering'), html.Td(dcc.Input(id='input-sex', type='text', value=patient[11]))]),
                html.Tr([html.Td('Achtergrond'), html.Td(dcc.Textarea(id='input-email', value=patient[12]))]),
                ]), id='app-medical-table'),
                html.H3('MEDICATIE'),
                *[html.Table(html.Tbody([html.Tr([html.Td('Naam medicatie'), html.Td(dcc.Input(id='input-user', type='text', value=medicine[2]), colSpan=4)]),
                html.Tr([html.Td('Vorm medicatie'), html.Td(dcc.Input(id='input-age', type='text', value=medicine[3]), colSpan=4)]),
                html.Tr([html.Td('Tijd inname'), html.Td(dcc.Checklist(options=[{'label':'', 'value':'1'}], value=[str(medicine[4])])), html.Td(dcc.Input(id='input-age', type='text', value=medicine[5])), html.Td('↔'), html.Td(dcc.Input(id='input-age', type='text', value=medicine[6]))]),
                html.Tr([html.Td('Maaltijd'), html.Td(dcc.Dropdown(options=[{'label':'Geen', 'value':'0'}, 
                                                                            {'label':'Ontbijt', 'value':'1'}, 
                                                                            {'label':'Lunch', 'value':'2'},
                                                                            {'label':'Diner', 'value':'3'}], value=str(medicine[7])), colSpan=4)]),
                html.Tr([html.Td(dcc.Checklist(options=[{'label':'Voor', 'value':'1'}, 
                                                        {'label':'Tijdens', 'value':'2'}, 
                                                        {'label':'Na', 'value':'3'}], labelStyle={'display': 'inline-block'
                                                        }, value=[str(medicine[8])]), colSpan=5)]),
                html.Tr([html.Td('Reden'), html.Td(dcc.Textarea(id='input-email', value=medicine[9]), colSpan=4)]),
                html.Tr([html.Td(html.Hr(), colSpan=5)]),
                ]), className='app-medication-table') for medicine in medication]]
        return content


    def ProfileTableFood(self, patient, diet):
        content = [html.H3('MAALTIJDEN'),
                   html.Table(html.Tbody([html.Tr([html.Td('Ontbijt'), html.Td(dcc.Checklist(options=[{'label':'', 'value':'1'}], value=[str(diet[2])])), html.Td(dcc.Input(id='input-age', type='text', value=diet[3])), html.Td('↔'), html.Td(dcc.Input(id='input-age', type='text', value=diet[4]))]),
                   html.Tr([html.Td('Lunch'), html.Td(dcc.Checklist(options=[{'label':'', 'value':'1'}], value=[str(diet[5])])), html.Td(dcc.Input(id='input-age', type='text', value=diet[6])), html.Td('↔'), html.Td(dcc.Input(id='input-age', type='text', value=diet[7]))]),
                   html.Tr([html.Td('Diner'), html.Td(dcc.Checklist(options=[{'label':'', 'value':'1'}], value=[str(diet[8])])), html.Td(dcc.Input(id='input-age', type='text', value=diet[9])), html.Td('↔'), html.Td(dcc.Input(id='input-age', type='text', value=diet[10]))]),
                   html.Tr([html.Td('Vegetarisch'), html.Td(dcc.Checklist(options=[{'label':'', 'value':'1'}], value=[str(diet[11])])), html.Td('Vegan'), html.Td(dcc.Checklist(options=[{'label':'', 'value':'1'}], value=[str(diet[12])]))]),
                   html.Tr([html.Td('Allergieen'), html.Td(dcc.Textarea(id='input-email', value=diet[13]), colSpan=4)]),
                   html.Tr([html.Td(['Bijzonder-', html.Br(), 'heden']), html.Td(dcc.Textarea(id='input-email', value=diet[14]), colSpan=4)]),
                   ]), id='app-food-table')]
        return content


    def LogsTable(self, patient, logs):
        color = '#ecfaff'
        content = html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url(f'smiley-positive.svg'), className='dashboard-icon'), className='dashboard-card-icon'), 
                                                  html.Td([html.H2(log[2]), html.P(log[-1])], className='dashboard-card-text'), 
                                                  html.Td(f'{log[3]}-{log[4]}')], style={'background': f'radial-gradient(circle 10vh at 4% 50%, {color} 70%, transparent 70%)'}) for log in logs]),
                                                  className='dashboard-table')
        return content


    def ChecklistTable(self):
        content = []
        return content


    def NewPatient(self):
        content = html.Div([html.H3('NIEUWE PATIENT'), html.P("Verdere patientgegevens kunnen worden ingevuld in het profiel."),
        html.Table(html.Tbody([html.Tr([html.Td('Naam'), html.Td(dcc.Input(id={'type':'entry-input', 'index':'name'}, type='text'))]),
                html.Tr([html.Td('Leeftijd'), html.Td(dcc.Input(id={'type':'entry-input', 'index':'age'}, type='number'))]),
                html.Tr([html.Td('Geslacht'), html.Td(dcc.Dropdown(id={'type':'entry-input', 'index':'sex'}, options=[{'label':'man', 'value':'m'}, {'label':'vrouw', 'value':'v'}, {'label':'anders', 'value':'a'}], placeholder='', clearable=False))]),
                html.Tr([html.Td('Lengte'), html.Td(dcc.Input(id={'type':'entry-input', 'index':'height'}, type='number'))]),
                html.Tr([html.Td('Gewicht'), html.Td(dcc.Input(id={'type':'entry-input', 'index':'weight'}, type='number'))]),
                ]), id='app-register-table'), 
                html.Button('x', id={'type':'close-entry-button', 'index':'patients'}, className='close-entry-button'),
                html.Button('Opslaan', id={'type':'save-entry-button', 'index':'patients'}, className='save-entry-button')], className='new-entry')
        return content


    def NewLogEntry(self, date):
        content = html.Div([html.H3('NIEUWE LOG'), html.P("yes yes"),
        html.Table(html.Tbody([html.Tr([html.Td('Titel'), html.Td(dcc.Input(type='text', id={'type':'entry-input', 'index':'title'}), colSpan=3)]),
                               html.Tr([html.Td('Datum'), html.Td(dcc.DatePickerSingle(max_date_allowed=date, display_format='D-M-Y', date=date, id={'type':'entry-input', 'index':'date'}), colSpan=3)]), 
                               html.Tr([html.Td('Gezondheid'), html.Td(html.Img(src=self.app.get_asset_url('smiley-negative.svg'))), html.Td(html.Img(src=self.app.get_asset_url('smiley-neutral.svg'))), html.Td(html.Img(src=self.app.get_asset_url('smiley-positive.svg')))]),
                               html.Tr([html.Td('Stemming'), html.Td(html.Img(src=self.app.get_asset_url('smiley-negative.svg'))), html.Td(html.Img(src=self.app.get_asset_url('smiley-neutral.svg'))), html.Td(html.Img(src=self.app.get_asset_url('smiley-positive.svg')))]),
                               html.Tr([html.Td('Bijzonderheden')]),
                               html.Tr([html.Td(dcc.Textarea(id={'type':'entry-input', 'index':'extra'}), colSpan=4)]),
                               ]), className='log-entry-table'), 
                               html.Button('x', id={'type':'close-entry-button', 'index':'log'}, className='close-entry-button'),
                               html.Button('Opslaan', id={'type':'save-entry-button', 'index':'log'}, className='save-entry-button')], className='new-entry')
        return content


    def NewMedicineEntry(self):
        content = html.Div([html.H3('NIEUWE MEDICATIE'), html.P(""),
        html.Table(html.Tbody([html.Tr([html.Td('Naam medicatie'), html.Td(dcc.Input(id={'type':'entry-input', 'index':'name'}, type='text'), colSpan=4)]),
                html.Tr([html.Td('Vorm medicatie'), html.Td(dcc.Input(id={'type':'entry-input', 'index':'type'}, type='text'), colSpan=4)]),
                html.Tr([html.Td('Tijd inname'), html.Td(dcc.Checklist(options=[{'label':'', 'value':'1'}], id={'type':'entry-input', 'index':'time_range'})), html.Td(dcc.Input(id={'type':'entry-input', 'index':'time_start'}, type='text')), html.Td('↔'), html.Td(dcc.Input(id={'type':'entry-input', 'index':'time_end'}, type='text'))]),
                html.Tr([html.Td('Maaltijd'), html.Td(dcc.Dropdown(options=[{'label':'Geen', 'value':'0'}, 
                                                                            {'label':'Ontbijt', 'value':'1'}, 
                                                                            {'label':'Lunch', 'value':'2'},
                                                                            {'label':'Diner', 'value':'3'}], value='0', id={'type':'entry-input', 'index':'meal'}), colSpan=4)]),
                html.Tr([html.Td(dcc.Checklist(options=[{'label':'Voor', 'value':'1'}, 
                                                        {'label':'Tijdens', 'value':'2'}, 
                                                        {'label':'Na', 'value':'3'}], labelStyle={'display': 'inline-block'
                                                        }, id={'type':'entry-input', 'index':'specific'}), colSpan=5)]),
                html.Tr([html.Td('Reden'), html.Td(dcc.Textarea(id={'type':'entry-input', 'index':'reason'}), colSpan=4)])]), className='app-medication-table'),
                html.Button('x', id={'type':'close-entry-button', 'index':'medical'}, className='close-entry-button'),
                html.Button('Opslaan', id={'type':'save-entry-button', 'index':'medical'}, className='save-entry-button')], className='new-entry')
        return content


    def HrTable(self, patient, mean):

        subjects = ['Gem bpm rust', 'Gem bpm actief', 'Fitness level', 'Endurance']

        # create block
        def block(subject, mean=False):
            return html.Td(html.Div([subject, html.P(mean)], className='app-data-card'))
        
        # create table from blocks
        content = html.Table(
           html.Tbody(
               [html.Tr(html.Td(html.Div(['grafiek', html.P('420')], className='app-main-data-card'), colSpan=2)),
                html.Tr([block(subjects[0], mean), block(subjects[1])]),
                html.Tr([block(subjects[2]), block(subjects[3])])]
           ), className='app-data-table' 
        )

        return content


    def Calendar(self):
        return html.Img(src=self.app.get_asset_url('calendar.svg'))


    def DataTable(self, hist, graph):

        subjects = ['Gem bpm rust', 'Gem bpm actief', 'Fitness level', 'Endurance']

        def block(subject, mean=False):
            return html.Td(html.Div([html.Div([html.P(mean),html.P(mean)]), html.P(mean), html.P('ya')], className='app-data-card'))
            
            # #html.Table(html.Tbody([html.Tr([html.Td('Gemiddeld'), html.Td('Hoog')]),
            #                              html.Tr([html.Td('yas', colSpan=2)]),
            #                              html.Tr([html.Td('yas', colSpan=2)])]), className='app-data-card')
        
        content = [html.H3('STATISTIEKEN'),
        html.Table(
           html.Tbody(
               [html.Tr(html.Td(html.Div([html.H4('Januari'), *hist, *graph], className='app-main-data-card'), colSpan=2)),
                html.Tr([block(subjects[0], 0), block(subjects[1])]),
                html.Tr([block(subjects[2]), block(subjects[3])])]
           ), className='app-data-table' 
        )]

        return content


    def BloodPressureHist(self):
        HEIGHT = 350
        WIDTH = 980
        
        uppers = np.random.randint(100, 200, size=30)
        lowers = np.random.randint(60, 120, size=30)

        drawing = svgwrite.Drawing(size=(WIDTH, HEIGHT), filename='assets/test.svg')

        n = 7
        spacing = 5
        bar_width = 30

        graph_height = HEIGHT - 40
        graph_width = WIDTH - 40

        upper_subset = uppers[:-n]
        lower_subset = lowers[:-n]

        scaling_factor = graph_height / np.max(np.hstack((upper_subset, lower_subset)))

        for i, (x, upper, lower) in enumerate(zip(np.linspace(20, graph_width - (bar_width * 2 + 5), num=n), upper_subset, lower_subset)):

            if i < n - 1:
                a = .5
            else:
                a = 1
            
            upper_bar_height = int(np.floor(graph_height - upper * scaling_factor))
            lower_bar_height = int(np.floor(graph_height - lower * scaling_factor))
            
            drawing.add(drawing.polygon([(x, upper_bar_height), (x + bar_width, upper_bar_height), (x+bar_width, graph_height), (x, graph_height)], fill='#FFCD4B', opacity=a))
            drawing.add(drawing.polygon([(x + bar_width + spacing, lower_bar_height), (x + bar_width*2 + spacing, lower_bar_height), (x+bar_width*2 +spacing, graph_height), (x + bar_width + spacing, graph_height)], fill='#FFCD4B', opacity=a))

            if i in [0, 3]:  
                drawing.add(drawing.text(f'{29 - n +  i}/01', (x - 5, HEIGHT), font_size='25pt', font_family='sans-serif', opacity=.5))
            if i in [6]:
                drawing.add(drawing.text(f'{29 - n +  i}/01', (x - 5, HEIGHT), font_size='25pt', font_family='sans-serif', font_weight='bold', opacity=.5))

        drawing.save()

        encoded = base64.b64encode(open('assets/test.svg','rb').read()) 
        svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode()) 
        
        return [html.Img(src=svg, className='blood-pressure-fig')]


    def BloodPressureGraph(self):
        HEIGHT = 350
        WIDTH = 980
        
        uppers = np.random.randint(100, 200, size=30)
        lowers = np.random.randint(60, 120, size=30)

        max_height = np.max(np.hstack((uppers, lowers)))

        drawing = svgwrite.Drawing(size=(WIDTH, HEIGHT), filename='assets/test.svg')
        drawing.add(drawing.rect((0, 0), (WIDTH, HEIGHT), rx=40, ry=40, stroke='#FFCD4B', fill='#FFCD4B', opacity=.17))

        gradient = svgwrite.gradients.LinearGradient(start=('0%', '100%'), end=('0%', '0%'), id='Gradient')
        gradient.add_stop_color(offset=0, color='#FFCD4B', opacity=0.17)
        gradient.add_stop_color(offset=1, color='#FFCD4B', opacity=0.83)
        drawing.add(gradient)

        xs = np.linspace(0, WIDTH, num=len(uppers))

        drawing.add(drawing.polygon([(0, HEIGHT)] + [(int(x), HEIGHT - int(upper)) for x, upper in zip(xs, uppers)] + [(WIDTH, HEIGHT)], fill=gradient.get_paint_server()))
        drawing.add(drawing.polyline([(int(x), HEIGHT - int(upper)) for x, upper in zip(xs, uppers)], stroke='white', stroke_width=7, fill='none'))

        drawing.save()

        encoded = base64.b64encode(open('assets/test.svg','rb').read()) 
        svg_upper = 'data:image/svg+xml;base64,{}'.format(encoded.decode())

        drawing = svgwrite.Drawing(size=(WIDTH, HEIGHT), filename='assets/test.svg')
        drawing.add(drawing.rect((0, 0), (WIDTH, HEIGHT), rx=40, ry=40, stroke='#FFCD4B', fill='#FFCD4B', opacity=.17))

        gradient = svgwrite.gradients.LinearGradient(start=('0%', '100%'), end=('0%', '0%'), id='Gradient')
        gradient.add_stop_color(offset=0, color='#FFCD4B', opacity=0.17)
        gradient.add_stop_color(offset=1, color='#FFCD4B', opacity=0.83)
        drawing.add(gradient)

        xs = np.linspace(0, WIDTH, num=len(uppers))

        drawing.add(drawing.polygon([(0, HEIGHT)] + [(int(x), HEIGHT - int(lower)) for x, lower in zip(xs, lowers)] + [(WIDTH, HEIGHT)], fill=gradient.get_paint_server()))
        drawing.add(drawing.polyline([(int(x), HEIGHT - int(lower)) for x, lower in zip(xs, lowers)], stroke='white', stroke_width=7, fill='none'))

        drawing.save()

        encoded = base64.b64encode(open('assets/test.svg','rb').read()) 
        svg_lower = 'data:image/svg+xml;base64,{}'.format(encoded.decode())
        
        return [html.Table(html.Tbody(html.Tr([html.Td('Per maand'), html.Td(html.Img(src=self.app.get_asset_url(f'icon-edit.svg')))])), className='data-fig-header'), 
        html.Img(src=svg_upper, className='blood-pressure-fig'), 
        html.Table(html.Tbody(html.Tr([html.Td('Per maand'), html.Td(html.Img(src=self.app.get_asset_url(f'icon-edit.svg')))])), className='data-fig-header'), 
        html.Img(src=svg_lower, className='blood-pressure-fig'),
        html.Table(html.Tbody(html.Tr([html.Td('< Vorige')])), className='data-fig-previous'), 
        html.Table(html.Tbody(html.Tr([html.Td('Volgende >')])), className='data-fig-next'), 
        ]

    def ChecklistTableMedication(self, medication):
        def Icon(type):
            if 'inject' in type.lower():
                return 'checklist-icon-injection'
            else:
                return 'checklist-icon-pills'

        medication = sorted(medication, key=lambda x: int(x[5].split(':')[0]))
        color = '#ecfaff'
        names = [med[2] for med in medication]
        totals = {name:names.count(name) for name in set(names)}
    
        medtable = html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url(f'{Icon(med[3])}.svg'), className='dashboard-icon'), className='checklist-card-icon'), 
                                                  html.Td([html.H2(med[2]), html.P(f'{0}/{totals[med[2]]}')], className='checklist-card-text'), 
                                                  html.Td([html.P(f'{med[5]}-{med[6]}'), dcc.Checklist(options=[{'label':'', 'value':'1'}], id={'type':'checklist-input', 'index':f'{med[2]}-{med[5]}-{med[6]}'})], className='checklist-checkbox')], style={'background': f'radial-gradient(circle 10vh at 4% 50%, {color} 70%, transparent 70%)'}) for med in medication]),
                                                  className='dashboard-table')

        return [html.H3('DAGELIJKSE MEDICATIE'), medtable]


    def ChecklistTableFood(self, diet):
        color = '#ecfaff'
        bools = [diet[2], diet[5], diet[8]]
        icons = [f'checklist-icon-{name}' for name in ['breakfast', 'lunch', 'dinner']]
        times = [[diet[3], diet[4]], [diet[6], diet[7]], [diet[9], diet[10]]]
        names = ['Ontbijt', 'Lunch', 'Diner']

        diettable = html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url(f'{icons[i]}.svg'), className='dashboard-icon'), className='checklist-card-icon'), 
                                                  html.Td([html.H2(names[i])], className='checklist-card-text'), 
                                                  html.Td([html.P(f'{times[i][0]}-{times[i][1]}'), dcc.Checklist(options=[{'label':'', 'value':'1'}], id={'type':'checklist-input', 'index':f'{names[i]}'})], className='checklist-checkbox')], style={'background': f'radial-gradient(circle 10vh at 4% 50%, {color} 70%, transparent 70%)'}) for i in range(3) if bools[i]]),
                                                  className='dashboard-table')
        return [html.H3('DAGELIJKSE VOEDING'), diettable]


    def ChecklistTableDevelopment(self):
        colors = ['#ecfaff', '#ecfaff']
        h3s = ['DAGELIJKSE BEWEGING', 'DAGELIJKS CONTACT']
        names = [['walking', 'stretching'], ['walking', 'stretching']]
        titles =  [['Rondje lopen', 'Rek oefeningen'], ['Telefoongesprek', 'Gesprek']]
        subtexts = [['5 minuten', '10 minuten'], ['min. 2 minuten', 'min. 2 minuten']]

        devtable = [(html.H3(h3s[i]), html.Table(html.Tbody([html.Tr([html.Td(html.Img(src=self.app.get_asset_url(f'checklist-icon-{names[i][j]}.svg'), className='dashboard-icon'), className='checklist-card-icon'), 
                                                  html.Td([html.H2(titles[i][j]), html.P(subtexts[i][j])], className='checklist-card-text'), 
                                                  html.Td([dcc.Checklist(options=[{'label':'', 'value':'1'}])], className='checklist-checkbox')], style={'background': f'radial-gradient(circle 10vh at 4% 50%, {colors[i]} 70%, transparent 70%)'})
                                                  for j in range(len(names[i]))]),
                                                  className='dashboard-table')) for i in range(len(h3s))]

        content = []

        for h3, cards in devtable:
            content += [h3]
            content += [cards]
        return content
