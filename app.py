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
from frames.log import LOGS
from frames.heartrate import HEARTRATE

# import backend funcs
from backend.register import register
from backend.login import login
from backend.select import *
from backend.insert import *

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
                       html.Div([], id='app-notification-placeholder-1', className='app-placeholder'),
                       html.Div([], id='app-entry-placeholder-1', className='app-placeholder'),
                       html.Div([], id='app-placeholder-2', className='app-placeholder'),
                       html.Div([], id='app-placeholder-3', className='app-placeholder'),
                       html.Div([], id='app-box')])


# content switch
@app.callback(Output('app-box', 'children'),
              Input('url-1', 'pathname'))
def display_page(path_1):
    uid = flask.request.cookies.get('uid')
    pid = flask.request.cookies.get('pid')
    today = date.today().strftime('%d %b %Y')

    def check_path(pathname):
        return path_1 == pathname

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
    elif check_path('/logboek') and uid and pid:
        patient = get_patient(pid)
        logs = get_patient_logs(pid)
        return LOGS(today, patient, logs)
    elif check_path('/hartslag') and uid and pid:
        patient = get_patients(pid)
        return HEARTRATE(patient)
    # if first time login, but no patient selected, redirect to patients
    elif not pid:
        name = get_name(uid)
        patients = get_patients(uid)
        return PATIENTS(name, patients)
    # if not logged in, redirect to login
    else:
        return LOGIN


# notifications wildcard callback
@app.callback(Output({'type':'notification', 'index': ALL}, 'style'),
              Input({'type':'close-notification-button', 'index': ALL}, 'n_clicks'))
def cb_close_notification(n_clicks):
    if n_clicks[0]:
        return [{'display':'none'}]
    else:
        return [{}]


# initial register
@app.callback(Output('app-notification-placeholder-1', 'children'),
              Output('app-notification-placeholder-1', 'style'),
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
        return cstm.Notification('Registratie succesvol!', index=1), {'display':'block'}
    else:
        return [], {'display':'none'}


# login callback
@app.callback(Output('app-placeholder-2', 'children'),
              inputs=[Input('login-button', 'n_clicks')],
              state=[State('login-input-email', 'value'),
                     State('login-input-password', 'value')])
def cb_login(n_clicks, email, password):
    # TODO: display message when login unsuccesful
    if n_clicks:
        if not email or not password:
            return [dcc.Location(pathname='/login', id='_')]
        id, hashed_pw = login(email, password) 
        if bcrypt.checkpw(password.encode(), hashed_pw):
            dash.callback_context.response.set_cookie('uid', str(id))
            return [dcc.Location(pathname='/patienten', id='_')]
        else:
            return [dcc.Location(pathname='/login', id='_')]
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
        return cstm.ProfileTableFood(patient), {}, {}, {'border-bottom': '3px solid #3B72FF'}
    elif '.' in trigger:
        return cstm.ProfileTableInfo(patient), {'border-bottom': '3px solid #3B72FF'}, {}, {}


# add new entry buttons wildcard callback
@app.callback(Output('app-entry-placeholder-1', 'children'),
              Output('app-entry-placeholder-1', 'style'),
              Output('app-box', 'style'),
              Output({'type':'refresh-body', 'index': ALL}, 'children'),
              Input({'type':'add-button', 'index': ALL}, 'n_clicks'),
              Input({'type':'close-entry-button', 'index': ALL}, 'n_clicks'),
              Input({'type':'save-entry-button', 'index': ALL}, 'n_clicks'),
              State({'type':'entry-input', 'index': ALL}, 'date'),
              State({'type':'entry-input', 'index': ALL}, 'value'))
def cb_add_entry(n_clicks_add, n_clicks_close, n_clicks_save, dates, inputs):
    trigger = dash.callback_context.triggered[0]['prop_id']

    if dates or inputs:
        dates = [elem for elem in dates if elem]
        inputs = [elem for elem in inputs if elem]
        year, month, day = dates[0].split('-')
        inputs = [elem for elem in inputs if elem]
        inputs = inputs + [int(day), int(month), int(year)]

    pid = flask.request.cookies.get('pid')
    page = []
    if trigger == '.':
        raise dash.exceptions.PreventUpdate
    elif 'log' in trigger:
        patient = get_patient(pid)
        logs = get_patient_logs(pid)
        page = (cstm.LogsTable(patient, logs), )

    content = [], {}, {}, page

    # show new entry
    if isinstance(n_clicks_add, list) and len(n_clicks_add) > 0 and n_clicks_add[0]:
        if 'log' in trigger:
            content = cstm.NewLogEntry(date.today()), {'display':'block'}, {'opacity': '.5'}, page
        elif 'calendar' in trigger:
            print('calendar')
            content = [], {}, {}, page
    # close (cancel) new entry
    if isinstance(n_clicks_close, list) and len(n_clicks_close) > 0 and n_clicks_close[0]:
        content = [], {'display':'none'}, {'opacity': '1'}, page
    # save new entry
    if isinstance(n_clicks_save, list) and len(n_clicks_save) > 0 and n_clicks_save[0]:
        if 'log' in trigger:
            insert_log(pid, inputs)
            patient = get_patient(pid)
            logs = get_patient_logs(pid)
            page = (cstm.LogsTable(patient, logs), )
            content = cstm.Notification('Log succesvol toegevoegd!'), {'display':'block'}, {'opacity': '1'}, page
    # standard
    if len(n_clicks_add) != 1 and len(n_clicks_close) != 1 and len(n_clicks_save) != 1:
        content = [], {}, {}, page
    return content


# start development server
if __name__ == '__main__':
    app.run_server(debug=True)