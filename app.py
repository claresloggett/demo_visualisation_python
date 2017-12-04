"""
A tiny demo Plotly Dash app using NEISS data.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly

import pandas as pd


### Read data ###

infile = "neiss.csv"

use_fields = "case_id trmt_date age narr sex diag body_part disposition location race_text prod1_text fire_involvement hospital_stratum".split()
categorical_fields = "sex race_text diag body_part disposition location prod1_text fire_involvement hospital_stratum".split()
specified_dtypes = {field:'category' for field in categorical_fields}

data = pd.read_table(infile, usecols=use_fields,
                     parse_dates=['trmt_date'],
                     dtype=specified_dtypes, 
                     index_col=0)

# Create a short product description for each product, similarly for body parts and diagnosis
products = set(data['prod1_text'].unique())
short_products = {s:s.split('(')[0].split(',')[0].strip() for s in products}
data['product'] = data['prod1_text'].apply(lambda p: short_products[p]).astype('category')

body_parts = set(data['body_part'].unique())
short_bodyparts = {s:s.split('(')[0].strip() for s in body_parts}
data['body_part'] = data['body_part'].apply(lambda b: short_bodyparts[b]).astype('category')

# Extract day - this corresponds to the day in December 2016
data['day'] = (data['trmt_date'] - data['trmt_date'].min()).dt.days + 1


### Dash app ###

app = dash.Dash()

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div(children=[
    html.H1("NEISS data demo"),
    
    # Or, better, for all products do:
    #   options=[{'label':product, 'value':product} for product in data['products'].unique()]
    # or for top few:
    #   options=[{'label':product, 'value':product} for product in data['product'].value_counts()[:10].index]
    dcc.Checklist(
        id='product_checklist',
        options=[
            {'label':'Stairs or steps', 'value':'Stairs or steps'},
            {'label':'Floors or flooring materials', 'value':'Floors or flooring materials'},
            {'label':'Basketball', 'value':'Basketball'},
            {'label':'Beds or bedframes', 'value':'Beds or bedframes'},
            {'label':'Knives', 'value':'Knives'},
            {'label':'Ceilings and walls', 'value':'Ceilings and walls'}
        ],
        values=['Ceilings and walls','Basketball']
    ),
    
    dcc.Graph(id='age_vs_day_plot')
])


@app.callback(Output('age_vs_day_plot','figure'), [Input('product_checklist','values')])
def draw_scatterplot(product_list):
    """
    Draw a scatterplot of patient age against day-of-month, including only products in product_list.
    """
    included_data = data[ data['product'].isin(product_list) ]
    
    trace = go.Scatter(x=included_data['day'],
                       y=included_data['age'],
                       mode='markers',
                       marker={'size': 10, 'opacity': 0.7},
                       text=included_data['narr'])
   
    figure = {
        'data': [trace],
        'layout': {
            'title': 'Injury incidents',
            'xaxis': {'title': 'Day of month'},
            'yaxis': {'title': 'Age of patient'},
            'hovermode': 'closest',
        }
    }
    
    return figure

    
### Run it ###

if __name__ == '__main__':
    app.run_server()