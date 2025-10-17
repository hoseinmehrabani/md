import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# ایجاد داده‌های تصادفی
np.random.seed(0)
data = {
    'Categories': ['A', 'B', 'C', 'D', 'E'],
    'Values': np.random.randint(1, 100, size=5)
}
df = pd.DataFrame(data)

# ایجاد اپلیکیشن Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='داشبورد ساده با Dash'),

    dcc.Graph(
        id='example-graph',
        figure=px.bar(df, x='Categories', y='Values', title='نمودار میله‌ای از داده‌های تصادفی')
    ),

    html.Button('تولید مجدد داده‌ها', id='update-button'),
    html.Div(id='output-div')
])

@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    dash.dependencies.Input('update-button', 'n_clicks')
)
def update_graph(n_clicks):
    # تولید داده‌های جدید
    new_values = np.random.randint(1, 100, size=5)
    df['Values'] = new_values
    return px.bar(df, x='Categories', y='Values', title='نمودار میله‌ای از داده‌های تصادفی')

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)

