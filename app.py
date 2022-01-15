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

# import frames
from frames.start import START
from frames.register import REGISTER
from frames.login import LOGIN

from frames.patients import PATIENTS
from frames.dashboard import DASHBOARD


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
app.layout = html.Div([dcc.Location(id='url', refresh=False), 
html.Div([], id='app-placeholder-1', className='app-placeholder'),
html.Div([], id='app-placeholder-2', className='app-placeholder'),
html.Div([], id='app-placeholder-3', className='app-placeholder'),
html.Div([], id='app-box')])


# content switch
@app.callback(Output('app-box', 'children'),
              [Input('url', 'pathname')]
)
def display_page(pathname):
    # TODO: block access when not logged in, i.e. cookie not set
    if pathname == '/':
        return START
    elif pathname == '/registreren':
        return REGISTER
    elif pathname == '/login':
        return LOGIN
    elif pathname == '/patienten':
        GC_UID = flask.request.cookies.get('uid')
        name = get_name(GC_UID)
        patients = get_patients(GC_UID)
        return PATIENTS(name, patients)
    elif pathname == '/dashboard':
        GC_PID = flask.request.cookies.get('pid')
        patient = get_patient(GC_PID)
        today = date.today().strftime('%d %b %Y')
        return DASHBOARD(today, patient)


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
        return [html.P(f'{n_clicks} {username} {age} {sex} {email} {tel}')]
    else:
        return []


# login callback
@app.callback(Output('app-placeholder-2', 'children'),
              inputs=[Input('login-button', 'n_clicks')],
              state=[State('login-input-email', 'value'),
                     State('login-input-password', 'value')])
def cb_login(n_clicks, email, password):
    if n_clicks:
        id, hashed_pw = login(email, password)
        if bcrypt.checkpw(password.encode(), hashed_pw):
            dash.callback_context.response.set_cookie('uid', str(id))
            return [dcc.Location(pathname="/patienten", id='_')]
        else:
            return []
    else:
        return []


# patients wildcard callback
@app.callback(Output('app-placeholder-3', 'children'),
              Input({'type':'app-patient-card', 'index': ALL}, 'n_clicks'))
def cb_select_patient(ids):
    if len(dash.callback_context.triggered) == 1:
        pid = yaml.safe_load(dash.callback_context.triggered[0]['prop_id'].split('.')[0])
        if pid:
            dash.callback_context.response.set_cookie('pid', str(pid['index']))
            return [dcc.Location(pathname="/dashboard", id='_')]
    else:
        return []


# dashboard switch callback
@app.callback(Output('dashboard-body', 'children'), 
              Output('dashboard-button-monitored', 'style'), 
              Output('dashboard-button-manual', 'style'), 
              Input('dashboard-button-monitored', 'n_clicks'), 
              Input('dashboard-button-manual', 'n_clicks'),
              )
def cb_switch_dashboard(moitored, manual):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if 'monitored' in trigger:
        return cstm.DashboardListMonitored(), {'border-bottom': '3px solid #3B72FF'}, {}
    elif 'manual' in trigger:
        return cstm.DashboardListManual(), {}, {'border-bottom': '3px solid #3B72FF'}
    else:
        return cstm.DashboardListMonitored(), {'border-bottom': '3px solid #3B72FF'}, {}


# start development server
if __name__ == '__main__':
    app.run_server(debug=True)