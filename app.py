import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc
import urllib.request as urllib2
import json

uploaded = 0
unallocated = 0
unevaluated = 0
evaluated = 0

df = pd.read_csv('https://raw.githubusercontent.com/deepakgola/tma-live-desktop/master/tma_oct22_status.csv')

url = 'https://api.github.com/repos/{owner}/{repo}/commits?per_page=1'.format(owner='deepakgola',
                                                                              repo='tma-live-desktop')
response = urllib2.urlopen(url).read()
data = json.loads(response.decode())
last_updated = data[0]['commit']['author']['date']

# Remove columns
col_list = list(df)
col_list.remove('SRNO')
col_list.remove('REGIONAL CENTRE')
col_list.remove('AI-CODE AND NAME')
col_list.remove('TOTAL STUDENTS UPLOADED TMA')
col_list.remove('PRE-ALLOCATED')
col_list.remove('PRE-EVALUATED')

# print(col_list)
sum_df = df[col_list].sum(axis=0)
sum_df = sum_df.head(7).reset_index(name='subjects')
sum_df.rename(columns={'index': 'stage'}, inplace=True)
sum_df = sum_df.sort_values(by=['subjects'], ascending=False)

uploaded = sum_df.iloc[0]['subjects']
unallocated = sum_df.iloc[2]['subjects']
evaluated = sum_df.iloc[3]['subjects']
unevaluated = sum_df.iloc[4]['subjects']

overall_pie_df = sum_df.drop([0, 1], axis=0)

fig1 = px.pie(overall_pie_df, values='subjects', names='stage', color='stage',
              color_discrete_map={'TOTAL ALLOCATED UN-EVALUATED SUBJECTS': '#e55467',
                                  'TOTAL EVALUATED SUBJECTS': 'forestgreen', 'TOTAL UN-ALLOCATED SUBJECTS': 'red'})
fig1.layout = go.Layout(
    # width=800,
    # height=520,
    plot_bgcolor='#1f2c56',
    paper_bgcolor='#1f2c56',
    hovermode='closest',
    title={
        'text': 'Overall TMA Status',
        'y': 0.93,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    titlefont={
        'color': 'white',
        'size': 20},
    legend={
        'orientation': 'h',
        'bgcolor': '#1f2c56',
        'xanchor': 'center', 'x': 0.5, 'y': -0.07},
    font=dict(
        family="sans-serif",
        size=15,
        color='white')
)

'''
Region Wise Stacked Bar Chart
'''
df_regions = df.groupby(['REGIONAL CENTRE']).sum().reset_index()
df_regions = df_regions[
    ['REGIONAL CENTRE', 'TOTAL STUDENTS UPLOADED TMA', 'TOTAL TMA UPLOADED', 'TOTAL ALLOCATED SUBJECTS',
     'TOTAL UN-ALLOCATED SUBJECTS', 'TOTAL EVALUATED SUBJECTS', 'TOTAL ALLOCATED UN-EVALUATED SUBJECTS']]
df_bar_stacked = df_regions[['REGIONAL CENTRE', 'TOTAL UN-ALLOCATED SUBJECTS', 'TOTAL EVALUATED SUBJECTS',
                             'TOTAL ALLOCATED UN-EVALUATED SUBJECTS']]

df_bar_stacked['UN-ALLOCATED %'] = df_bar_stacked['TOTAL UN-ALLOCATED SUBJECTS'] / (
        df_bar_stacked['TOTAL UN-ALLOCATED SUBJECTS'] + df_bar_stacked['TOTAL EVALUATED SUBJECTS'] + df_bar_stacked[
    'TOTAL ALLOCATED UN-EVALUATED SUBJECTS'])
df_bar_stacked['EVALUATED %'] = df_bar_stacked['TOTAL EVALUATED SUBJECTS'] / (
        df_bar_stacked['TOTAL UN-ALLOCATED SUBJECTS'] + df_bar_stacked['TOTAL EVALUATED SUBJECTS'] + df_bar_stacked[
    'TOTAL ALLOCATED UN-EVALUATED SUBJECTS'])
df_bar_stacked['ALLOCATED UN-EVALUATED %'] = df_bar_stacked['TOTAL ALLOCATED UN-EVALUATED SUBJECTS'] / (
        df_bar_stacked['TOTAL UN-ALLOCATED SUBJECTS'] + df_bar_stacked['TOTAL EVALUATED SUBJECTS'] + df_bar_stacked[
    'TOTAL ALLOCATED UN-EVALUATED SUBJECTS'])

# df1 = px.data.iris()

fig_bar_stacked = px.bar(df_bar_stacked,
                         y="REGIONAL CENTRE",
                         x=['UN-ALLOCATED %', 'ALLOCATED UN-EVALUATED %', 'EVALUATED %'],
                         orientation='h',
                         barmode='stack'
                         )
fig_bar_stacked.layout.plot_bgcolor = '#1f2c56'
fig_bar_stacked.layout.paper_bgcolor = '#1f2c56'
fig_bar_stacked.layout.font = dict(
    family="sans-serif",
    size=12,
    color='white')

fig_bar_stacked.layout.legend = {
    'orientation': 'h',
    'bgcolor': '#1f2c56',
    'xanchor': 'center', 'x': 0.5, 'y': 1.3}

# app = Dash(__name__)
app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('icons8-assignment-64.png'),
                     id='icons8-assignment-64-image',
                     style={
                         "height": "60px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H1("TMA Dashboard", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H6("Progress Tracker : TMA Evaluation October-2022",
                        style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.H6('Last Updated: ' + str(last_updated), style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),
    html.Div([
        html.Div([
            html.H6(children="Total Uploaded",
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{uploaded:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),

            html.P('',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Un-Allocated',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{unallocated:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 40}
                   ),

            html.P(f"({(unallocated / uploaded) * 100:.2f}%)",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Un-Evaluated',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{unevaluated:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 40}
                   ),

            html.P(f"({(unevaluated / uploaded) * 100:.2f}%)",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Evaluated',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{evaluated:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40}
                   ),

            html.P(f"({(evaluated / uploaded) * 100:.2f}%)",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns")

    ], className="row flex-display"),
    html.Div([
        html.Div([
            dcc.Graph(id='pie_chart_overall',
                      figure=fig1,
                      config={'displayModeBar': 'hover'}),
        ], className="create_container four columns"),

        html.Div([
            dcc.Graph(id="line_chart", figure=fig_bar_stacked)

        ], className="create_container eight columns"),
    ], className="row flex-display"),
], id="mainContainer", style={"display": "flex", "flex-direction": "column"})

if __name__ == '__main__':
    app.run_server(debug=True)
