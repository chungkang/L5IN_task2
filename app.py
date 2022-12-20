# import datetime
# from dash import Dash, dcc, html
# from dash.dependencies import Input, Output, State
# import cv2
# import base64
# import numpy as np
# # import src.module.rectification as rectification

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = Dash(__name__, external_stylesheets=external_stylesheets)
# app.layout = html.Div([
#     dcc.Upload(id = 'upload-image', children=html.Button('Upload File')),
#     html.Div(id='output-image-upload'),
# ])

# @app.callback(Output('output-image-upload', 'children'),
#               Input('upload-image', 'contents'),
#               State('upload-image', 'filename'),
#               State('upload-image', 'last_modified'))

# def update_output(content, name, date):
#     if content is not None:
#         return html.Div([
#             html.H5(name),
#             html.H6(datetime.datetime.fromtimestamp(date)),
#             # HTML images accept base64 encoded strings in the same format
#             # that is supplied by the upload
#             html.Img(src=content),
#             html.Hr(),
#             html.Div('Raw Content'),
#             html.Pre(content[0:200] + '...', style={
#                 'whiteSpace': 'pre-wrap',
#                 'wordBreak': 'break-all'
#             }),
#             # html.Img(src=rectification.rectify_image(content, 4, algorithm='independent')),
#         ])

# if __name__ == '__main__':
#     app.run_server(debug=True)



import base64
from io import BytesIO
from PIL import Image
from dash import Dash, dcc, html

app = Dash(__name__)

# Open the image
im = Image.open('module_test\\result\\20220112_162250_warped.png')

# Encode the image as a base64 string
buffered = BytesIO()
im.save(buffered, format="PNG")
encoded_image = base64.b64encode(buffered.getvalue()).decode()

# Create the layout for the Dash app
app.layout = html.Div([
    # Display the image
    dcc.Graph(
        id='image',
        figure={
            'data': [{
                'x': [1],
                'y': [1],
                'type': 'image',
                'source': 'data:image/png;base64,{}'.format(encoded_image),
                'sizing': 'stretch'
            }]
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
