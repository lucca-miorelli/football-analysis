import dash

app = dash.Dash(__name__)
server = app.server  # Exposes the server variable for deploying to production
