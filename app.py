import dash
import yaml
import flask
import bcrypt
import pickle
import sqlite3

from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL

from datetime import date

# import templates
from templates.main import Custom

# import static frames
from frames.start import START
from frames.register import REGISTER
from frames.login import LOGIN

# import dynamic frames
from frames.patients import PATIENTS
from frames.dashboard import DASHBOARD
from frames.profile import PROFILE
from frames.calendar import CALENDAR
from frames.checklist import CHECKLIST

# import backend funcs
from backend.register import register
from backend.login import login
from backend.get import *

cstm = Custom()

GC_UID = None
GC_PID = None

# init app
app = dash.Dash(__name__, 
                external_stylesheets=['https://fonts.googleapis.com/css?family=Lato'])

# suppress callback exceptions
app.config.suppress_callback_exceptions = True

# layout
app.layout = html.Div([dcc.Location(id='url-1', refresh=False),
                       dcc.Location(id='url-2', refresh=False),
                       html.Div([], id='app-placeholder-1', className='app-placeholder'),
                       html.Div([], id='app-placeholder-2', className='app-placeholder'),
                       html.Div([], id='app-placeholder-3', className='app-placeholder'),
                       html.Div([], id='app-box')])


# content switch
@app.callback(Output('app-box', 'children'),
              Input('url-1', 'pathname'),
              Input('url-2', 'pathname'))
def display_page(path_1, path_2):
    uid = flask.request.cookies.get('uid')
    pid = flask.request.cookies.get('pid')
    today = date.today().strftime('%d %b %Y')

    def check_path(pathname):
        return path_1 == pathname or path_2 == pathname

    if check_path('/'):
        return START
    elif check_path('/registreren'):
        return REGISTER
    elif check_path('/login'):
        return LOGIN
    elif check_path('/patienten') and uid:
        name = get_name(uid)
        patients = get_patients(uid)
        return PATIENTS(name, patients)
    elif check_path('/dashboard') and uid and pid:
        patient = get_patient(pid)
        return DASHBOARD(today, patient)
    elif check_path('/agenda') and uid and pid:
        patient = get_patient(pid)
        return CALENDAR(today, patient)
    elif check_path('/checklist') and uid and pid:
        patient = get_patient(pid)
        return CHECKLIST(today, patient)
    elif check_path('/notificaties') and uid and pid:
        return []
    elif check_path('/profiel') and uid and pid:
        patient = get_patient(pid)
        return PROFILE(patient)
    # if first time login, but no patient selected, redirect to patients
    elif not pid:
        name = get_name(uid)
        patients = get_patients(uid)
        return PATIENTS(name, patients)
    # if not logged in, redirect to login
    else:
        return LOGIN


# initial register
@app.callback(Output('app-placeholder-1', 'children'),
              inputs=[Input('register-button', 'n_clicks')],
              state=[State('input-user', 'value'),
                     State('input-age', 'value'),
                     State('input-sex', 'value'),
                     State('input-email', 'value'),
                     State('input-phone', 'value')])
def cb_register(n_clicks, username, age, sex, email, tel):
    # TODO: filter register input before writing to db
    hashable_pw = bytes('abc', encoding='utf-8')
    hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())

    if n_clicks:
        register(username, age, sex, email, tel, hashed_pw)
        # TODO: registration succesful notification
        return []
    else:
        return []


# login callback
@app.callback(Output('app-placeholder-2', 'children'),
              inputs=[Input('login-button', 'n_clicks')],
              state=[State('login-input-email', 'value'),
                     State('login-input-password', 'value')])
def cb_login(n_clicks, email, password):
    # TODO: display message when login unsuccesful
    if n_clicks:
        id, hashed_pw = login(email, password)
        if bcrypt.checkpw(password.encode(), hashed_pw):
            dash.callback_context.response.set_cookie('uid', str(id))
            return [dcc.Location(pathname='/patienten', id='_')]
        else:
            return []
    else:
        return []


# header menu callback
@app.callback(Output('app-header-button-menu', 'children'),
              Output('app-header-menu-container', 'style'),
              Input('app-header-button-menu', 'n_clicks'),
              Input('app-header-button-logout', 'n_clicks'))
def cb_header_menu(n_clicks_menu, n_clicks_logout):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if 'menu' in trigger:
        if n_clicks_menu and (n_clicks_menu % 2 != 0):
            return html.Img(src=app.get_asset_url('header-icon-menu-dark.svg')), {'display':'block'}
    if 'logout' in trigger:
        if n_clicks_logout:
            dash.callback_context.response.set_cookie('uid', '', expires=0)
            dash.callback_context.response.set_cookie('pid', '', expires=0)
            return [dcc.Location(pathname='/login', id='_')], {}
    else:
        return html.Img(src=app.get_asset_url('header-icon-menu.svg')), {'display':'none'}


# patients wildcard callback
@app.callback(Output('url-1', 'pathname'),
              Input({'type':'app-patient-card', 'index': ALL}, 'n_clicks'))
def cb_select_patient(ids):
    if len(dash.callback_context.triggered) == 1:
        pid = yaml.safe_load(dash.callback_context.triggered[0]['prop_id'].split('.')[0])
        if pid:
            dash.callback_context.response.set_cookie('pid', str(pid['index']))
            return '/dashboard'
    else:
        return '/patienten'


# dashboard switch callback
@app.callback(Output('dashboard-body', 'children'), 
              Output('dashboard-button-monitored', 'style'), 
              Output('dashboard-button-manual', 'style'), 
              Input('dashboard-button-monitored', 'n_clicks'), 
              Input('dashboard-button-manual', 'n_clicks'))
def cb_switch_dashboard(moitored, manual):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if 'monitored' in trigger:
        return cstm.DashboardListMonitored(), {'border-bottom': '3px solid #3B72FF'}, {}
    elif 'manual' in trigger:
        return cstm.DashboardListManual(), {}, {'border-bottom': '3px solid #3B72FF'}
    else:
        return cstm.DashboardListMonitored(), {'border-bottom': '3px solid #3B72FF'}, {}


# profile switch callback
@app.callback(Output('profile-body', 'children'), 
              Output('profile-button-info', 'style'), 
              Output('profile-button-medical', 'style'), 
              Output('profile-button-food', 'style'), 
              Input('profile-button-info', 'n_clicks'), 
              Input('profile-button-medical', 'n_clicks'),
              Input('profile-button-food', 'n_clicks'))
def cb_switch_profile(info, medical, food):
    trigger = dash.callback_context.triggered[0]['prop_id']
    GC_PID = flask.request.cookies.get('pid')
    patient = get_patient(GC_PID)
    if 'info' in trigger:
        return cstm.ProfileTableInfo(patient), {'border-bottom': '3px solid #3B72FF'}, {}, {}
    elif 'medical' in trigger:
        return cstm.ProfileTableMedical(patient), {}, {'border-bottom': '3px solid #3B72FF'}, {}
    elif 'food' in trigger:
        return [], {}, {}, {'border-bottom': '3px solid #3B72FF'}
    else:
        return cstm.ProfileTableInfo(patient), {'border-bottom': '3px solid #3B72FF'}, {}, {}


# start development server
if __name__ == '__main__':
    app.run_server(debug=True)