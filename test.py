import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

# Load an image and display it using the dcc.Graph component
app.layout = html.Div([
    dcc.Graph(
        id='image',
        figure={
            'data': [{'x': [1], 'y': [1],
                     'type': 'image', 'source': 'module_test\\result\\20220112_162250_wrapped.png'}]
        }
    ),
    html.Button('Capture Image', id='button')
])

# Use the relayoutData attribute to capture the image
@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('image', 'figure')])
def capture_image(n_clicks, figure):
    # Check if the button has been clicked
    if n_clicks is not None:
        # Get the image data from the figure
        image_data = figure['data'][0]['source']

        # Save the image to a file (you'll need to write code here to do this)

        return 'Image saved!'
    return 'No image captured'

if __name__ == '__main__':
    app.run_server()
