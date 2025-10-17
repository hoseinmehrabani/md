from IPython.utils.coloransi import value
from click import style
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
df=px.data.stocks()
# #step 1 dataset
# df=pd.DataFrame({
#     'city':['tehran','qom','ahvaz','esfhan'],
#     'papulation':[8,5,7,2]
# })
# #step 2 charts:
# fig=px.pie(df,values='papulation',names='city')
# #step 3 layout
# app=Dash(__name__,title='first dash')
# app.layout=dcc.Graph(figure=fig)
# #step 4 callbacks
#
# #step 5 RUN
# if __name__=='__main__':
#     app.run_server()
# fig_1=px.line(df,x='date',y='GOOG')
# fig_2=px.line(df,x='date',y='AAPL')
#
# app=Dash(__name__,title='dash')
# app.layout(html.Div(children=[
#     html.H1(children='Dash'),
#     html.P(children='Dash jnjbbfhg  kjh'),
#     html.A(children='Dash',href='http://toplearn.com'),
#
#     ],style={'text-align':'center','color':'black'}),
#     html.Div(children=[
#         dcc.Graph(figure=fig_1),
#         dcc.Graph(figure=fig_2)
#     ],style={'display':'flex'})
# ])
#
# if __name__ == "__main__":
#     app.run_server(debug=True)
app=Dash(__name__)
app.layout=html.Div(children=[
    html.label('radio items'),
    dcc.RadioItems(options=['tehran','qom','shriaz'],value='shriaz'),
    html.label('check list'),
    dcc.Checklist(options=['tehran','qom','shriaz'],value=['shriaz','qom']),
    html.label('input'),
    dcc.Input(type='text',placeholder='Select a stock',value='toplearn'),
    html.Hr(),
    html.label('slider'),
    dcc.Slider(min=1,max=5,value=2),
    dcc.Slider(min=1,max=5,step=1),
    html.Hr(),
    dcc.RangeSlider(min=1,max=5,step=2),
    html.Hr(),
    html.label('dropdown'),
    dcc.Dropdown(options=['tehran','qom','shriaz'],value='shriaz'),
    html.label('multi dropdown'),
    dcc.Dropdown(options=['tehran','qom','shriaz'],value='shriaz',multi=True),
    html.label('text area'),
    dcc.Textarea(placeholder='Select a stock',value='toplearn'),
])
#داشبورد تعاملی
app.layout(html.Div(children=[
    dcc.Input(type='text',value='toplearn',id='input'),
    html.Br(),
    html.P(children='Output',id='output'),

]))
@app.callback(Output('output','children'),
              Input(component_id='input', component_property='value'))
def update(i):
    return "Output" +str(i)
if __name__ == '__main__':
    app.run_server(debug=True)
df=px.data.stocks()
app=Dash(__name__)
app.layout(html.Div(children=[
    dcc.Dropdown(df.colums[1:],value='toplearn',id='input',multi=True),
    html.Br(),
    dcc.Graph(id='output_chart'),
]))
@app.callback(Output('output_chart','figure'),
              Input(component_id='input', component_property='value'))
def update_chart(x):
    fig=px.line(df,x='date',y=x)
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)

app=Dash(__name__)
app.layout(html.Div(children=[
    html.label("x axes:"),
    dcc.RadioItems(df.colums[:4],value=df.colums[0],id="i1"),
    html.Br(),
    html.label("y axes:"),
    dcc.RadioItems(df.colums[:4], value=df.colums[1], id="i2"),
    html.Br(),
    dcc.Graph(id='chart'),

]))
@app.callback(Output('chart','figure'),
              Input(component_id='i1', component_property='value'),
              Input(component_id='i2', component_property='value'))
def update_chart(x,y):
    fig=px.line(df,x=x,y=y)
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
df=px.data.model_wide()
app=Dash(__name__)
app.layout(html.Div(children=[
    html.label("which model"),
    html.Br(),
    dcc.RadioItems(df.colums[1:],df.colums[1],id="input_data"),
    dcc.Graph(id='fig1'),
    dcc.Graph(id='fig2'),
]))
@app.callback(Output('fig1','figure'),
              Output(component_id='fig2',component_property='figure'),
              Input(component_id='input_data', component_property='value'))
def update_chart(i):
    fig1=px.pie(df,names="nation",values=i)
    fig2=px.bar(df,x="nation",y=i)
    return fig1,fig2
if __name__ == '__main__':
    app.run_server(debug=True)