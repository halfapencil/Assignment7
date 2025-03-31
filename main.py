from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = Dash()
app=server
df = pd.read_csv('WorldCupDataset.csv',header=[0])
app.layout = html.Div([
    html.H1(children="World Cup Finals Winners and Runner ups", style={"text-align":"center"}),
    html.H2(children="Year:"),
    dcc.Dropdown(['All','1930','1934','1938','1950','1954','1958','1962','1966','1970','1974','1978','1982','1986','1990','1994','1998','2002','2006','2010','2014','2018','2022',], value = 'All',id='year'),
    dcc.Graph(id='map'),
    html.H2(id='winner',children='Winner:'),
    html.H2(id='runnerUp',children='Runner Up:')
])
@callback(
    [Output('map','figure'),Output('winner','children'),Output('runnerUp','children')],
    Input('year','value')
)
def update_output(year):
    
    if year=='All':
        filtered_df = df
        max_wins = filtered_df.groupby('Winner')['Wins'].max()
        filtered_df = filtered_df.merge(max_wins,on='Winner',suffixes=('','_total'))
        fig = px.choropleth(filtered_df, locations='Winner',
                        color='Wins_total',
                        hover_name='Country', 
                        hover_data={'Wins_total':True},
                        color_continuous_scale=px.colors.sequential.Plasma)
        WinnerString = ""
        RunnerupString =''
    else:
        filtered_df =  df[df['Year']==int(year)]
        filtered_df = filtered_df.T
        result = [filtered_df.iloc[1,0],filtered_df.iloc[2,0]]
        data = pd.DataFrame({
            'Iso_alpha':[result[0],result[1]],
            'Place':['Winner','Runner up'],
        })
        fig= px.choropleth(data, locations='Iso_alpha',
                           color='Place')
        WinnerString = f"Winner:{result[0]}"
        RunnerupString = f"Runner up:{result[1]}"
    return fig,WinnerString,RunnerupString

if __name__=='__main__':
    app.run(debug=False)
