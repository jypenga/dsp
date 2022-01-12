import dash
import sqlite3

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

# init app
app = dash.Dash(__name__,
                external_stylesheets=['https://fonts.googleapis.com/css?family=Lato'])

# suppress callback exceptions
app.config.suppress_callback_exceptions = True

# layout
app.layout = html.Div([dcc.Location(id='url', refresh=False), html.Div([], id='app-placeholder'), html.Div([], id='app-box')])

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
        return PATIENTS

# initial register
@app.callback(Output('app-placeholder', 'children'),
              inputs=[Input('register-button', 'n_clicks')],
              state=[State('input-user', 'value'),
                    State('input-age', 'value'),
                    State('input-sex', 'value'),
                    State('input-email', 'value'),
                    State('input-phone', 'value')]
)
def cb_init_register(n_clicks, username, age, sex, email, tel):
    # TODO: filter register input before writing to db
    if n_clicks:
        val = init_register()
        return [html.P(f'{val} {n_clicks} {username} {age} {sex} {email} {tel}')]
    else:
        return []

# start development server
if __name__ == '__main__':
    app.run_server(debug=True)