import datetime
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import cv2
import base64
import numpy as np
# import src.module.rectification as rectification

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Upload(id = 'upload-image', children=html.Button('Upload File')),
    html.Div(id='output-image-upload'),
])

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))

def update_output(content, name, date):
    if content is not None:
        return html.Div([
            html.H5(name),
            html.H6(datetime.datetime.fromtimestamp(date)),
            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Img(src=content),
            html.Hr(),
            html.Div('Raw Content'),
            html.Pre(content[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            }),
            # html.Img(src=rectification.rectify_image(content, 4, algorithm='independent')),
        ])

if __name__ == '__main__':
    app.run_server(debug=True)