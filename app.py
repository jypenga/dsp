import dash
import flask
import bcrypt
import pickle
import sqlite3
import requests

from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State

# import frames
from frames.start import START
from frames.register import REGISTER
from frames.login import LOGIN
from frames.patients import PATIENTS

# import backend funcs
from backend.register import init_register
from backend.login import login
from backend.get import get_name

# init app
app = dash.Dash(__name__, 
                     external_stylesheets=['https://fonts.googleapis.com/css?family=Lato'])

# suppress callback exceptions
app.config.suppress_callback_exceptions = True

# layout
app.layout = html.Div([dcc.Location(id='url', refresh=False), 
html.Div([], id='app-placeholder-1', className='app-placeholder'),
html.Div([], id='app-placeholder-2', className='app-placeholder'), 
html.Div([], id='app-box')])

# content switch
@app.callback(Output('app-box', 'children'),
              [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return START
    elif pathname == '/registreren':
        return REGISTER
    elif pathname == '/login':
        return LOGIN
    elif pathname == '/patienten':
        name = get_name(flask.request.cookies.get('id'))
        return PATIENTS(name)


# initial register
@app.callback(Output('app-placeholder-1', 'children'),
              inputs=[Input('register-button', 'n_clicks')],
              state=[State('input-user', 'value'),
                    State('input-age', 'value'),
                    State('input-sex', 'value'),
                    State('input-email', 'value'),
                    State('input-phone', 'value')])
def cb_init_register(n_clicks, username, age, sex, email, tel):
    # TODO: filter register input before writing to db
    hashable_pw = bytes('abc', encoding='utf-8')
    hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())

    if n_clicks:
        init_register(username, age, sex, email, tel, hashed_pw)
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
            dash.callback_context.response.set_cookie('id', str(id))
            return [dcc.Location(pathname="/patienten", id='_')]
        else:
            return []
    else:
        return []


# start development server
if __name__ == '__main__':
    app.run_server(debug=True)