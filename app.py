from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import base64
from io import BytesIO
from PIL import Image
import datetime
import numpy as np
import cv2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Open the image
im = Image.open('module_test\\result\\20220112_162250_wrapped.png')

# Encode the image as a base64 string
buffered = BytesIO()
im.save(buffered, format="PNG")
encoded_image = base64.b64encode(buffered.getvalue()).decode()

# Create the layout for the Dash app
app.layout = html.Div([
    dcc.Upload(id = 'upload-image', children=html.Button('Upload File')),
    html.Div(id='output-image-upload'),
    html.Button('Rectify', id='rectification_button', n_clicks=0),
])

# Use the relayoutData attribute to crop the image
@app.callback(
    Output('output-image-upload', 'children'),
    # Output('image', 'figure'),
    Input('upload-image', 'contents'),
    # Input('image', 'relayoutData'),
    State('upload-image', 'filename'),
    State('upload-image', 'last_modified'),
    Input('rectification_button', 'n_clicks'),
)

def update_output(content, name, date, n_clicks):
    if content is not None:
        return html.Div([
            html.H5(name),
            html.H6(datetime.datetime.fromtimestamp(date)),
            # Display the image
            dcc.Graph(
                    id='image',
                    figure={
                        'data': [{
                            # 'x': [1],
                            # 'y': [1],
                            'type': 'image',
                            'source': content,
                            # 'sizing': 'stretch'
                        }]
                    },
                    style={'width': '1000px', 'height': '800px'}
            ),
            html.Hr(),
        ])
    
    # Check if the button has been clicked
    if n_clicks is not None:
        print("smt")
        return 'Script executed'
    return 'No script executed'

def update_image(relayout_data):
    # Check if the user has selected a region to crop
    if 'xaxis.range[0]' in relayout_data:
        # Extract the coordinates of the selected region
        x0 =    ['xaxis.range[0]']
        x1 = relayout_data['xaxis.range[1]']
        y0 = relayout_data['yaxis.range[0]']
        y1 = relayout_data['yaxis.range[1]']

        # Crop the image using the selected region
        # (you'll need to write code here to actually perform the cropping)
        print(x0," ",x1," ",y0," ",y1)

        # Update the figure with the cropped image
        figure = {
            'data': [{
                'x': [1],
                'y': [1],
                'type': 'image',
                'source': 'data:image/png;base64,{}'.format(encoded_image),
                'sizing': 'stretch',
            }]
        }
        return figure

    # If no region is selected, return the original figure
    return {
        'data': [{
                'x': [1],
                'y': [1],
                'type': 'image',
                'source': 'data:image/png;base64,{}'.format(encoded_image),
                'sizing': 'stretch'
            }]
    }

if __name__ == '__main__':
    app.run_server(debug=True)
