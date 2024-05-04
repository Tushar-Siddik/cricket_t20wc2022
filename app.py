# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from cricket import Cricket
# from cricket import all, group, super_12, semi, final

# Incorporate data
df = pd.read_csv('data/T-20 World cup 2022.csv').set_index('match_id').drop(columns = ['comment_id', 'home_team', 'away_team'])

# Initialize the app
app = Dash(__name__)
server = app.server


all_matches = {
    'AFG v ENG': ['AFG', 'ENG'],
    'AFG v SL': ['AFG', 'SL'],
    'AUS v AFG': ['AUS', 'AFG'],
    'AUS v IRE': ['AUS', 'IRE'],
    'AUS v NZ': ['AUS', 'NZ'],
    'AUS v SL': ['AUS', 'SL'],
    'BAN v INDIA': ['BAN', 'INDIA'],
    'BAN v NED': ['BAN', 'NED'],
    'BAN v PAK': ['BAN', 'PAK'],
    'BAN v SA': ['BAN', 'SA'],
    'BAN v ZIM': ['BAN', 'ZIM'],
    'ENG v INDIA': ['ENG', 'INDIA'],
    'ENG v IRE': ['ENG', 'IRE'],
    'ENG v NZ': ['ENG', 'NZ'],
    'ENG v PAK': ['ENG', 'PAK'],
    'ENG v SL': ['ENG', 'SL'],
    'INDIA v NED': ['INDIA', 'NED'],
    'INDIA v PAK': ['INDIA', 'PAK'],
    'INDIA v SA': ['INDIA', 'SA'],
    'INDIA v ZIM': ['INDIA', 'ZIM'],
    'IRE v NZ': ['IRE', 'NZ'],
    'IRE v SCOT': ['IRE', 'SCOT'],
    'IRE v SL': ['IRE', 'SL'],
    'IRE v WI': ['IRE', 'WI'],
    'IRE v ZIM': ['IRE', 'ZIM'],
    'NAM v NED': ['NAM', 'NED'],
    'NAM v SL': ['NAM', 'SL'],
    'NAM v UAE': ['NAM', 'UAE'],
    'NED v PAK': ['NED', 'PAK'],
    'NED v SA': ['NED', 'SA'],
    'NED v SL': ['NED', 'SL'],
    'NED v UAE': ['NED', 'UAE'],
    'NED v ZIM': ['NED', 'ZIM'],
    'NZ v PAK': ['NZ', 'PAK'],
    'NZ v SL': ['NZ', 'SL'],
    'PAK v SA': ['PAK', 'SA'],
    'PAK v ZIM': ['PAK', 'ZIM'],
    'SA v ZIM': ['SA', 'ZIM'],
    'SCOT v WI': ['SCOT', 'WI'],
    'SCOT v ZIM': ['SCOT', 'ZIM'],
    'SL v UAE': ['SL', 'UAE'],
    'WI v ZIM': ['WI', 'ZIM'],
}



all_stages = {
    'all' : ['AFG', 'AUS', 'BAN', 'ENG', 'INDIA', 'IRE', 'NAM', 'NED', 'NZ', 'PAK', 'SA', 'SCOT', 'SL', 'UAE', 'WI', 'ZIM'],
    'group' : ['IRE', 'NAM', 'NED', 'SCOT', 'SL', 'UAE', 'WI', 'ZIM'],
    'super 12' : ['AFG', 'AUS', 'BAN', 'ENG', 'INDIA', 'IRE', 'NED', 'NZ', 'PAK', 'SA', 'SL', 'ZIM'],
    'semi' : ['ENG', 'INDIA', 'NZ', 'PAK'],
    'final' : ['ENG', 'PAK'],
}



# App layout
app.layout = html.Div(
    style = {'max-width' : '600px', 'text-align' : 'center', 'align-items' : 'center', 'padding' : '10px',  'background-color': '#f8f9fa'},
    children = [
    html.Div(
        children = [
            html.H1('Cricket Analysis'),
            html.H3('T20 World cup, 2022'),
            html.H5('Developer: Md. Siddiqur Rahman')
        ], 
        style = {'text-align' : 'center'}),
    
    html.Div(
        children = [
            html.H2('Main Data Set'),
            dash_table.DataTable(
                data=df.loc[:, : 'runs'].to_dict('records'), 
                page_size= 10
            )
        ]),
    
    html.Div(
        children = [
            html.Hr(),
            html.H2('Analysis', style = {'text-align' : 'center'}),
            html.Hr(),
        ]),
    
    
    # html.Hr(),
    # over by over Run timeline
    html.Div(
        style={"flex": 1, "padding": "10px"},
        children = [
            html.H3('Over by Over Run Timeline'),
            html.H4('Match'),
            dcc.Dropdown(
                list(all_matches.keys()),
                'BAN v ZIM',
                id = 'match_name',
                # inline=True
            ),
                
            html.Br(),
            html.H4('Innings'),
                
            dcc.RadioItems(
                id = 'match_innings', 
                value= 'BAN', 
                inline = True
            ),
                
            html.Br(),
            dash_table.DataTable(
                id = 'team_run_timeline_over', 
                page_size= 10
            ),
            dcc.Graph(
                figure={}, 
                id='team_run_timeline_over_graph_bar'
            ),
            dcc.Graph(
                figure={}, 
                id='team_run_timeline_over_graph_line'
            ),  
            html.Hr(), 
    ]),


    # Game stage options
    html.Div(
        children = [
            html.H3('Stage: '),
            dcc.Dropdown(
                options = list(all_stages.keys()), 
                value='all', 
                id='stage', 
                # inline=True
            ),
        ]),
    
    # information
    html.Div(
        children = [
            html.H3('Info'),
            html.Div(id = 'info'),    
        ]),
    html.Hr(),
    
    # match by match Run timeline
    html.Div(
        # style={"flex": 1, "padding": "10px"},
        children = [
            html.H3('Match by Match Run Timeline'),
            dcc.RadioItems(
                id = 'team', 
                value= 'BAN', 
                inline = True
            ),
            
            dash_table.DataTable(
                id = 'team_run_timeline', 
                page_size= 10
            ),
            dcc.Graph(
                figure={}, 
                id='team_run_timeline_graph'
            ),  
            html.Hr(), 
        ]),


    
    

    
    
    # Run analysis
    html.H2('Analysis of Run', style = {'text-align' : 'center'}),
    html.Div(children = [html.H3('Run in an innings for a batsman'),
                        dash_table.DataTable(id = 'most_run_innings_player', page_size= 10),
                        # dcc.Slider(min = 5, max = 20, step=1, id = 'most_run_innings_player_slider'),
                        dcc.Graph(figure={}, id='most_run_innings_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most run for a batsman in a team'),
                        dash_table.DataTable(id = 'most_run_team_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_run_team_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most run for a batsman'),
                        dash_table.DataTable(id = 'most_run_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_run_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most average run for a batsman (min 50 runs)'),
                        dash_table.DataTable(id = 'most_average_batsman', page_size= 10),
                        dcc.Graph(figure={}, id='most_average_batsman_graph'),  
                        html.Hr(),
    ]),
    
    
    # Bowling analysis
    html.H2('Analysis of Bowling in T20 world cup, 2022', style = {'text-align' : 'center'}),
    html.Div(children = [html.H3('Most wicket taker in an innings'),
                        dash_table.DataTable(id = 'most_wicket_innings_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='most_wicket_innings_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most wicket taker'),
                        dash_table.DataTable(id = 'most_wicket_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='most_wicket_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Bowler with the lowest Economy (min 4 overs)'),
                        dash_table.DataTable(id = 'lowest_economy_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='lowest_economy_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Bowler with the lowest Average (min 4 overs)'),
                        dash_table.DataTable(id = 'lowest_average_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='lowest_average_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Dismissed Batsman'),
                        dash_table.DataTable(id = 'most_out_batsman', page_size= 10),
                        dcc.Graph(figure={}, id='most_out_batsman_graph'),  
                        html.Hr(),
    ]),
    
    
    # Extra run analysis
    html.H2('Analysis of Extra Run: Who got most extra run?', style = {'text-align' : 'center'}),
    html.Div(children = [html.H3('Most wide run in an innings'),
                        dash_table.DataTable(id = 'most_wide_run_innings_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_wide_run_innings_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most NoBall run in an innings'),
                        dash_table.DataTable(id = 'most_noball_run_innings_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_noball_run_innings_team_graph'),  
                        html.Hr(),
    ]),
    
    
    # Most played
    html.H2('Most played analysis', style = {'text-align' : 'center'}),
    html.Div(children = [html.H3('Most played team'),
                        dash_table.DataTable(id = 'most_played_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_played_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most played Batsman'),
                        dash_table.DataTable(id = 'most_played_batsman', page_size= 10),
                        dcc.Graph(figure={}, id='most_played_batsman_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most played Bowler'),
                        dash_table.DataTable(id = 'most_played_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='most_played_bowler_graph'),  
                        html.Hr(),
    ]),
    
    
    # Most winnings
    html.H2('Most winning analysis', style = {'text-align' : 'center'}),
    html.Div(children = [html.H3('Most winning team'),
                        dash_table.DataTable(id = 'most_winning_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_winning_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most winning innings'),
                        dash_table.DataTable(id = 'most_winning_innings', page_size= 10),
                        dcc.Graph(figure={}, id='most_winning_innings_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most win/match ratio'),
                        dash_table.DataTable(id = 'most_win_match_ratio', page_size= 10),
                        dcc.Graph(figure={}, id='most_win_match_ratio_graph'),  
                        html.Hr(),
    ]),
    
    
    # boundaries
    html.H2('Most Boundaries', style = {'text-align' : 'center'}),
    html.Div(children = [html.H3('Most Fours in an innings'),
                        dash_table.DataTable(id = 'most_fours_innings', page_size= 10),
                        dcc.Graph(figure={}, id='most_fours_innings_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Fours for a team'),
                        dash_table.DataTable(id = 'most_fours_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_fours_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Fours in a match'),
                        dash_table.DataTable(id = 'most_fours_match', page_size= 10),
                        dcc.Graph(figure={}, id='most_fours_match_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Fours by a batsman in an innings'),
                        dash_table.DataTable(id = 'most_fours_innings_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_fours_innings_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Fours as a team player'),
                        dash_table.DataTable(id = 'most_fours_team_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_fours_team_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Sixes in an innings'),
                        dash_table.DataTable(id = 'most_sixes_innings', page_size= 10),
                        dcc.Graph(figure={}, id='most_sixes_innings_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Sixes for a team'),
                        dash_table.DataTable(id = 'most_sixes_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_sixes_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Sixes in a match'),
                        dash_table.DataTable(id = 'most_sixes_match', page_size= 10),
                        dcc.Graph(figure={}, id='most_sixes_match_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Sixes by a batsman in an innings'),
                        dash_table.DataTable(id = 'most_sixes_innings_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_sixes_innings_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Sixes as a team player'),
                        dash_table.DataTable(id = 'most_sixes_team_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_sixes_team_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Boundaries in an innings'),
                        dash_table.DataTable(id = 'most_boundaries_innings', page_size= 10),
                        dcc.Graph(figure={}, id='most_boundaries_innings_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Boundaries for a team'),
                        dash_table.DataTable(id = 'most_boundaries_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_boundaries_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Boundaries in a match'),
                        dash_table.DataTable(id = 'most_boundaries_match', page_size= 10),
                        dcc.Graph(figure={}, id='most_boundaries_match_graph'),  
                        html.Hr(),
    ]),
    
    
    # single, double, tripple
    html.H2('Analysis of single, double and triples', style = {'text-align' : 'center'}),
    html.Div(children = [html.H3('Most single in an innings'),
                        dash_table.DataTable(id = 'most_single_innings', page_size= 10),
                        dcc.Graph(figure={}, id='most_single_innings_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most single for a team'),
                        dash_table.DataTable(id = 'most_single_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_single_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most single in a match'),
                        dash_table.DataTable(id = 'most_single_match', page_size= 10),
                        dcc.Graph(figure={}, id='most_single_match_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most double/ tripple in an innings'),
                        dash_table.DataTable(id = 'most_double_innings', page_size= 10),
                        dcc.Graph(figure={}, id='most_double_innings_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most double/ tripple for a team'),
                        dash_table.DataTable(id = 'most_double_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_double_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most double/ tripple in a match'),
                        dash_table.DataTable(id = 'most_double_match', page_size= 10),
                        dcc.Graph(figure={}, id='most_double_match_graph'),  
                        html.Hr(),
    ]),
    
    
    # powerplay
    html.H2('Powerplay analysis', style = {'text-align' : 'center'}),  
    html.Div(children = [html.H3('Most runs in powerplay for a team'),
                        dash_table.DataTable(id = 'most_run_power_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_run_power_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most runs in powerplay for a team in an innings'),
                        dash_table.DataTable(id = 'most_run_power_innings_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_run_power_innings_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most runs in powerplay for a batsman'),
                        dash_table.DataTable(id = 'most_run_power_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_run_power_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most strike rate in powerplay for a team'),
                        dash_table.DataTable(id = 'most_strike_power_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_strike_power_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most strike rate in powerplay for a team in an innings'),
                        dash_table.DataTable(id = 'most_strike_power_innings_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_strike_power_innings_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most strike rate in powerplay for a batsman'),
                        dash_table.DataTable(id = 'most_strike_power_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_strike_power_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most strike rate in powerplay for a batsman in a match'),
                        dash_table.DataTable(id = 'most_strike_power_match_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_strike_power_match_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most wicket in powerplay innings for a bowler'),
                        dash_table.DataTable(id = 'most_wicket_power_innings_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='most_wicket_power_innings_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most wicket in powerplay for a bowler'),
                        dash_table.DataTable(id = 'most_wicket_power_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='most_wicket_power_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Lowest economy in powerplay for a bowler (min 4 overs)'),
                        dash_table.DataTable(id = 'lowest_economy_power_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='lowest_economy_power_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Lowest average in powerplay for a bowler (min 4 overs)'),
                        dash_table.DataTable(id = 'lowest_average_power_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='lowest_average_power_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Dismissed Batsman in powerplay'),
                        dash_table.DataTable(id = 'most_out_power_batsman', page_size= 10),
                        dcc.Graph(figure={}, id='most_out_power_batsman_graph'),  
                        html.Hr(),
    ]),
    
    
    # death over
    html.H2('Death over analysis', style = {'text-align' : 'center'}),  
    html.Div(children = [html.H3('Most runs indeath-over for a team'),
                        dash_table.DataTable(id = 'most_run_death_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_run_death_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most runs in death-over for a team in an innings'),
                        dash_table.DataTable(id = 'most_run_death_innings_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_run_death_innings_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most runs in death-over for a batsman'),
                        dash_table.DataTable(id = 'most_run_death_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_run_death_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most strike rate in death-over for a team'),
                        dash_table.DataTable(id = 'most_strike_death_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_strike_death_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most strike rate in death-over for a team in an innings'),
                        dash_table.DataTable(id = 'most_strike_death_innings_team', page_size= 10),
                        dcc.Graph(figure={}, id='most_strike_death_innings_team_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most strike rate in death-over for a batsman'),
                        dash_table.DataTable(id = 'most_strike_death_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_strike_death_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most strike rate in death-over for a batsman in a match'),
                        dash_table.DataTable(id = 'most_strike_death_match_player', page_size= 10),
                        dcc.Graph(figure={}, id='most_strike_death_match_player_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most wicket in death-over innings for a bowler'),
                        dash_table.DataTable(id = 'most_wicket_death_innings_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='most_wicket_death_innings_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most wicket in death-over for a bowler'),
                        dash_table.DataTable(id = 'most_wicket_death_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='most_wicket_death_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Lowest economy in death-over for a bowler (min 4 overs)'),
                        dash_table.DataTable(id = 'lowest_economy_death_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='lowest_economy_death_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Lowest average in death-over for a bowler (min 4 overs)'),
                        dash_table.DataTable(id = 'lowest_average_death_bowler', page_size= 10),
                        dcc.Graph(figure={}, id='lowest_average_death_bowler_graph'),  
                        html.Hr(),
    ]),
    
    html.Div(children = [html.H3('Most Dismissed Batsman in death-over'),
                        dash_table.DataTable(id = 'most_out_death_batsman', page_size= 10),
                        dcc.Graph(figure={}, id='most_out_death_batsman_graph'),  
                        html.Hr(),
    ]),
      
    
])


# callback
# callback


# over by over run timeline
@callback(
    Output('match_innings', 'options'),
    Input('match_name', 'value')
)
def get_info(match):
    return [{'label' : i, 'value' : i} for i in all_matches[match]]
    # return all_matches[match]

@callback(
    Output('match_innings', 'value'),
    Input('match_innings', 'options')
)
def get_info(innings):
    return innings[0]['value']


@app.callback(
    Output('team_run_timeline_over', 'data'),
    Input('match_name', 'value'),
    Input('match_innings', 'value')
)
def get_info(match, team):
    game =  Cricket(df, 'all')
    return game.team_run_timeline_over(match, team).to_dict('records')

@app.callback(
    Output('team_run_timeline_over_graph_bar', 'figure'),
    Input('match_name', 'value'),
    Input('match_innings', 'value')
)
def get_info(match, team):
    df1 = Cricket(df, 'all')
    game = df1.team_run_timeline_over(match, team)
    wicket = game[game['Wicket'] != 0]
    # fig = px.scatter(data_frame= wicket, x = 'Over', y = 'Wicket')
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x = game['Over'],
            y = game['Run'],
            text = game['Run'],
            hovertext = [f'Over: {o}<br>Run: {r}' for o, r in zip(game['Over'], game['Run'])],
            textposition= 'outside',
            name= 'Run [Over]',
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x = wicket['Over'],
            y = wicket['Wicket'],
            mode = 'markers',
            hovertext = [f'Over: {o}<br>Wicket: {w}' for o, w in zip(wicket['Over'], wicket['Wicket'])],
            name='Wicket',
            marker = dict(color= 'red', size = 12),
        )
    )
    
    # fig.update_traces(
    #     textposition='outside',  
    #     # textfont=dict(color='white')
    # )

    fig.update_layout(
        title = dict( text = f"Over by Over run and wicket<br>{match}: {team}", x=0.5),
        xaxis = dict(title = 'Over'),
        yaxis = dict(title = 'Run and Wicket')
    )
    return fig

@app.callback(
    Output('team_run_timeline_over_graph_line', 'figure'),
    Input('match_name', 'value'),
    Input('match_innings', 'value')
)
def get_info(match, team):
    df1 = Cricket(df, 'all')
    game = df1.team_run_timeline_over(match, team)
    wicket = game[game['Wicket'] != 0]
    # wicket['wicket_t'] = wicket['Wicket'].cumsum()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = game['Over'],
            y = game['Total'],
            mode = 'lines',
            line = dict(width = 5),
            hovertext = [f'Over: {o}<br>Run: {r}' for o, r in zip(game['Over'], game['Run'])],
            name= 'Total Run [Over]',
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x = wicket['Over'],
            y = wicket['Total'],
            # cliponaxis = game['Total'],
            mode = 'markers',
            marker = dict(color= 'red', size = 12),
            hovertext = [f'Over: {o}<br>Wicket: {w}' for o, w in zip(wicket['Over'], wicket['Wicket'])],
            name= 'Wicket [Over]',
        )
    )
    
    fig.update_layout(
        title = dict( text = f"Over by Over total run and wicket<br>{match}: {team}", x=0.5),
        xaxis = dict(title = 'Over'),
        yaxis = dict(title = 'Total run and Wicket')
    )
    return fig






@callback(
    Output('team', 'options'),
    Input('stage', 'value')
)
def get_info(stage):
    return [{'label' : i, 'value' : i} for i in all_stages[stage]]
    # return all_matches[match]

@callback(
    Output('team', 'value'),
    Input('team', 'options')
)
def get_info(team):
    return team[2]['value']




# information
@app.callback(
    Output('info', 'children'),
    Input('stage', 'value')
)
def get_info(stage):
    return Cricket(df, stage).info()



# match by match run timeline
@app.callback(
    Output('team_run_timeline', 'data'),
    Input('stage', 'value'),
    Input('team', 'value')
)
def get_info(stage, team):
    game =  Cricket(df, stage)
    return game.team_run_timeline(team).to_dict('records')

@app.callback(
    Output('team_run_timeline_graph', 'figure'),
    Input('stage', 'value'),
    Input('team', 'value')
)
def get_info(stage, team):
    game =  Cricket(df, stage).team_run_timeline(team)
    fig = px.line(game, x = 'match_name', y = 'Run', markers = True)
    
    fig.update_traces(
    line=dict(width=5), 
    marker=dict(size=10)
    )
    fig.update_layout(
        title = dict( text = f"Run Timeline of {team}", x=0.5),
        xaxis = dict(title = 'Match'),
        yaxis = dict(title = 'Run')
    )
    return fig


# Run analysis
@app.callback(
    Output('most_run_innings_player', 'data'),
    Input('stage', 'value')
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_innings_player()
    return game.to_dict('records')

@app.callback(
    Output('most_run_innings_player_graph', 'figure'),
    Input('stage', 'value')
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_innings_player().head()
    string = [f'Match: {m}, Balls: {b}, Strk rate: {sr}' for m, b, sr in zip(game['Match'], game['Balls'], game['Strk rate'])]

    fig = px.bar(game, x = 'Runs', y = 'Batsman', text = string)
    fig.update_traces(
        textposition='inside',  
        textfont=dict(color='white')
    )
    fig.update_layout(
        title = dict( text = 'Most run for a batsman in an innings', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_run_team_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_team_player()
    return game.to_dict('records')

@app.callback(
    Output('most_run_team_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_team_player().head()
    string = [f'Team: {t}, Balls: {b}, Strk rate: {sr}' for t, b, sr in zip(game['Team'], game['Balls'], game['Strk rate'])]

    fig = px.bar(game, x = 'Runs', y = 'Batsman', text = string)
    fig.update_traces(
        textposition='inside',  
        textfont=dict(color='white')
    )
    fig.update_layout(
        title = dict( text = 'Most run for a batsman in a team', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_run_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_player()
    return game.to_dict('records')

@app.callback(
    Output('most_run_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_player().head()
    string = [f'Team: {t}, Balls: {b}, Strk rate: {sr}' for t, b, sr in zip(game['Team'], game['Balls'], game['Strk rate'])]

    fig = px.bar(x = game['Runs'].values, y = game['Batsman'].values, text = string)
    fig.update_traces(
        textposition='inside',  
        textfont=dict(color='white')
    )
    fig.update_layout(
        title = dict( text = 'Most run for a batsman', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_average_batsman', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_average_batsman()
    game = game[game['Runs'] >= 50]
    return game.to_dict('records')

@app.callback(
    Output('most_average_batsman_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_average_batsman()
    game = game[game['Runs'] >= 50].head()
    string = [f'Team: {t}, Runs: {r}, \n Strk rate: {b}' for t, r, b in zip(game['Team'], game['Runs'], game['Strk rate'])]

    fig = px.bar(game, x = 'Avg', y = 'Batsman', text = string)
    fig.update_traces(
        textposition='inside',  
        textfont=dict(color='white')
    )
    fig.update_layout(
        title = dict( text = 'Most average run for a batsman (min 50 runs)', x=0.5),
        xaxis = dict(title = 'Average run'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


# Bowling analysis
@app.callback(
    Output('most_wicket_innings_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_innings_bowler()
    return game.to_dict('records')

@app.callback(
    Output('most_wicket_innings_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_innings_bowler().head()
    string = [f'Match: {m}\nAgainst: {i}' for m, i in zip(game['Match'], game['Innings'])]

    fig = px.bar(game, x = 'Wicket', y = 'Bowler', text = string)
    fig.update_traces(
        textposition='inside',  
        textfont=dict(color='white')
    )
    fig.update_layout(
        title = dict( text = 'Most wicket taker in an innings', x=0.5),
        xaxis = dict(title = 'Wicket'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('most_wicket_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_bowler()
    return game.to_dict('records')

@app.callback(
    Output('most_wicket_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_bowler().head()
    # string = [f'Match: {m}\nAgainst: {i}' for m, i in zip(game['Match'], game['Innings'])]

    fig = px.bar(game, x = 'Wicket', y = 'Bowler')

    fig.update_layout(
        title = dict( text = 'Most wicket taker', x=0.5),
        xaxis = dict(title = 'Wicket'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('lowest_economy_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_economy_bowler()
    game = game[game['Over'] >= 4]
    return game.to_dict('records')

@app.callback(
    Output('lowest_economy_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_economy_bowler()
    game = game[game['Over'] >= 4].head()
    # string = [f'Match: {m}\nAgainst: {i}' for m, i in zip(game['Match'], game['Innings'])]

    fig = px.bar(game, x = 'Economy', y = 'Bowler')

    fig.update_layout(
        title = dict( text = 'Lowest economy (min 4 overs)', x=0.5),
        xaxis = dict(title = 'Economy'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('lowest_average_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_average_bowler()
    game = game[game['Over'] >= 4]
    return game.to_dict('records')

@app.callback(
    Output('lowest_average_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_average_bowler()
    game = game[game['Over'] >= 4].head()

    fig = px.bar(game, x = 'Average', y = 'Bowler')

    fig.update_layout(
        title = dict( text = 'Lowest average (min 4 overs)', x=0.5),
        xaxis = dict(title = 'Average'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('most_out_batsman', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_out_batsman()
    return game.to_dict('records')

@app.callback(
    Output('most_out_batsman_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_out_batsman().head()
    string = [f'Match: {m}' for m in game['Match']]

    fig = px.bar(game, x = 'Out', y = 'Batsman', text= string)

    fig.update_layout(
        title = dict( text = 'Most Dismissed Batsman', x=0.5),
        xaxis = dict(title = 'Dismissal number'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


# Extra run
@app.callback(
    Output('most_wide_run_innings_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wide_run_innings_team()
    return game.to_dict('records')

@app.callback(
    Output('most_wide_run_innings_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wide_run_innings_team().head()
    string = [f'Team: {t}' for t in game['Team']]

    fig = px.bar(game, x = 'Wide', y = 'Match', text= string)

    fig.update_layout(
        title = dict( text = 'Most Wide run in an innings', x=0.5),
        xaxis = dict(title = 'Wide run'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_noball_run_innings_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_noball_run_innings_team()
    return game.to_dict('records')

@app.callback(
    Output('most_noball_run_innings_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_noball_run_innings_team().head()
    string = [f'Match: {m}' for m in game['Match']]

    fig = px.bar(game, x = 'NoBall', y = 'Team', text= string)

    fig.update_layout(
        title = dict( text = 'Most NoBall run in an innings', x=0.5),
        xaxis = dict(title = 'NoBall run'),
        yaxis = dict(title = 'Team')
    )
    return fig


# most played
@app.callback(
    Output('most_played_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_played_team()
    return game.to_dict('records')

@app.callback(
    Output('most_played_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_played_team().head()

    fig = px.bar(game, x = 'Match', y = 'Team')

    fig.update_layout(
        title = dict( text = 'Most played team', x=0.5),
        xaxis = dict(title = 'Match'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_played_batsman', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_played_batsman()
    return game.to_dict('records')

@app.callback(
    Output('most_played_batsman_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_played_batsman().head()

    fig = px.bar(game, x = 'Match', y = 'Batsman')

    fig.update_layout(
        title = dict( text = 'Most played Batsman', x=0.5),
        xaxis = dict(title = 'Match'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_played_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_played_bowler()
    return game.to_dict('records')

@app.callback(
    Output('most_played_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_played_bowler().head()

    fig = px.bar(game, x = 'Match', y = 'Bowler')

    fig.update_layout(
        title = dict( text = 'Most played Bowler', x=0.5),
        xaxis = dict(title = 'Match'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


# most winning
@app.callback(
    Output('most_winning_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_winning_team()
    return game.to_dict('records')

@app.callback(
    Output('most_winning_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_winning_team()

    fig = px.bar(game, x = 'Wins', y = 'Team')

    fig.update_layout(
        title = dict( text = 'Most winning team', x=0.5),
        xaxis = dict(title = 'Wins'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_winning_innings', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_winning_innings()
    return game.to_dict('records')

@app.callback(
    Output('most_winning_innings_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_winning_innings()

    fig = px.pie(game, names = 'Innings_No.', values = 'Wins')

    fig.update_layout(
        title = dict( text = 'Most winning innings', x=0.5)
    )
    return fig


@app.callback(
    Output('most_win_match_ratio', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_win_match_ratio()
    return game.to_dict('records')

@app.callback(
    Output('most_win_match_ratio_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_win_match_ratio()
    string = [f'Match: {m}, Wins: {w}' for m, w in zip(game['Match'], game['Wins'])]

    fig = px.bar(game, x = 'Ratio %', y = 'Team', text = string)

    fig.update_layout(
        title = dict( text = 'Most win/match ratio', x=0.5),
        xaxis = dict(title = 'Win %'),
        yaxis = dict(title = 'Team')
    )
    return fig


# most boundaries
@app.callback(
    Output('most_fours_innings', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_innings()
    return game.to_dict('records')

@app.callback(
    Output('most_fours_innings_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_innings().head()
    string = [f'Match: {m}' for m in game['match_name']]

    fig = px.bar(game, x = 'Fours', y = 'Innings', text = string)

    fig.update_layout(
        title = dict( text = 'Most fours in an innings', x=0.5),
        xaxis = dict(title = 'Fours'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_fours_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_team()
    return game.to_dict('records')

@app.callback(
    Output('most_fours_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_team()

    fig = px.bar(game, x = 'Fours', y = 'Team')

    fig.update_layout(
        title = dict(text = 'Most fours for a team', x=0.5),
        xaxis = dict(title = 'Fours'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_fours_match', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_match()
    return game.to_dict('records')

@app.callback(
    Output('most_fours_match_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_match().head()

    fig = px.bar(game, x = 'Fours', y = 'Match')

    fig.update_layout(
        title = dict(text = 'Most fours in a match', x=0.5),
        xaxis = dict(title = 'Fours'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_fours_innings_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_innings_player()
    return game.to_dict('records')

@app.callback(
    Output('most_fours_innings_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_innings_player().head()
    string = [f'Team: {t}, Match: {m}' for t, m in zip(game['Innings'], game['match_name'])]
    fig = px.bar(game, x = 'Fours', y = 'Batsman', text = string)

    fig.update_layout(
        title = dict(text = 'Most fours by a batsman in an innings', x=0.5),
        xaxis = dict(title = 'Fours'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_fours_team_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_team_player()
    return game.to_dict('records')

@app.callback(
    Output('most_fours_team_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_fours_team_player().head()
    string = [f'Team: {t}' for t in game['Team']]
    fig = px.bar(game, x = 'Fours', y = 'Batsman', text = string)

    fig.update_layout(
        title = dict(text = 'Most fours as a team player', x=0.5),
        xaxis = dict(title = 'Fours'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_sixes_innings', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_innings()
    return game.to_dict('records')

@app.callback(
    Output('most_sixes_innings_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_innings().head()
    string = [f'Match: {m}' for m in game['match_name']]

    fig = px.bar(game, x = 'Sixes', y = 'Innings', text = string)

    fig.update_layout(
        title = dict( text = 'Most sixes in an innings', x=0.5),
        xaxis = dict(title = 'Sixes'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_sixes_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_team()
    return game.to_dict('records')

@app.callback(
    Output('most_sixes_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_team()

    fig = px.bar(game, x = 'Sixes', y = 'Team')

    fig.update_layout(
        title = dict(text = 'Most fours for a team', x=0.5),
        xaxis = dict(title = 'Sixes'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_sixes_match', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_match()
    return game.to_dict('records')

@app.callback(
    Output('most_sixes_match_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_match().head()

    fig = px.bar(game, x = 'Sixes', y = 'Match')

    fig.update_layout(
        title = dict(text = 'Most sixes in a match', x=0.5),
        xaxis = dict(title = 'Sixes'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_sixes_innings_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_innings_player()
    return game.to_dict('records')

@app.callback(
    Output('most_sixes_innings_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_innings_player().head()
    string = [f'Team: {t}, Match: {m}' for t, m in zip(game['Innings'], game['match_name'])]
    fig = px.bar(game, x = 'Sixes', y = 'Batsman', text = string)

    fig.update_layout(
        title = dict(text = 'Most sixes by a batsman in an innings', x=0.5),
        xaxis = dict(title = 'Sixes'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_sixes_team_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_team_player()
    return game.to_dict('records')

@app.callback(
    Output('most_sixes_team_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_sixes_team_player().head()
    string = [f'Team: {t}' for t in game['Team']]
    fig = px.bar(game, x = 'Sixes', y = 'Batsman', text = string)

    fig.update_layout(
        title = dict(text = 'Most sixes as a team player', x=0.5),
        xaxis = dict(title = 'Sixes'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_boundaries_innings', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_boundaries_innings()
    return game.to_dict('records')

@app.callback(
    Output('most_boundaries_innings_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_boundaries_innings().head()
    string = [f'Fours: {f}, Sixes: {s}' for f, s in zip (game['Fours'], game['Sixes'])]

    fig = px.bar(game, x = 'Boundaries', y = 'Innings', text = string)

    fig.update_layout(
        title = dict(text = 'Most boundaries in an innings', x=0.5),
        xaxis = dict(title = 'Boundaries'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_boundaries_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_boundaries_team()
    return game.to_dict('records')

@app.callback(
    Output('most_boundaries_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_boundaries_team().head()
    string = [f'Fours: {f}, Sixes: {s}' for f, s in zip (game['Fours'], game['Sixes'])]

    fig = px.bar(game, x = 'Boundaries', y = 'Team', text = string)

    fig.update_layout(
        title = dict(text = 'Most boundaries in an innings', x=0.5),
        xaxis = dict(title = 'Boundaries'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_boundaries_match', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_boundaries_match()
    return game.to_dict('records')

@app.callback(
    Output('most_boundaries_match_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_boundaries_match().head()
    string = [f'Fours: {f}, Sixes: {s}' for f, s in zip (game['Fours'], game['Sixes'])]

    fig = px.bar(game, x = 'Boundaries', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most boundaries in a match', x=0.5),
        xaxis = dict(title = 'Boundaries'),
        yaxis = dict(title = 'Match')
    )
    return fig


# sinle, double, tripple
@app.callback(
    Output('most_single_innings', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_single_innings()
    return game.to_dict('records')

@app.callback(
    Output('most_single_innings_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_single_innings().head()
    string = [f'Team: {t}' for t in game['Innings']]

    fig = px.bar(game, x = 'Single', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most single in an innings', x=0.5),
        xaxis = dict(title = 'Single'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_single_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_single_team()
    return game.to_dict('records')

@app.callback(
    Output('most_single_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_single_team().head()

    fig = px.bar(game, x = 'Single', y = 'Team')

    fig.update_layout(
        title = dict(text = 'Most single for a team', x=0.5),
        xaxis = dict(title = 'Single'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_single_match', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_single_match()
    return game.to_dict('records')

@app.callback(
    Output('most_single_match_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_single_match().head()

    fig = px.bar(game, x = 'Single', y = 'Match')

    fig.update_layout(
        title = dict(text = 'Most single in a match', x=0.5),
        xaxis = dict(title = 'Single'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_double_innings', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_double_innings()
    return game.to_dict('records')

@app.callback(
    Output('most_double_innings_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_double_innings().head()
    string = [f'Team: {t}' for t in game['Innings']]

    fig = px.bar(game, x = 'Runs', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most Double/ Tripple in an innings', x=0.5),
        xaxis = dict(title = 'Double/ Tripple'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_double_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_double_team()
    return game.to_dict('records')

@app.callback(
    Output('most_double_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_double_team().head()

    fig = px.bar(game, x = 'Runs', y = 'Team')

    fig.update_layout(
        title = dict(text = 'Most Double/ Tripple for a team', x=0.5),
        xaxis = dict(title = 'Double/ Tripple'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_double_match', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_double_match()
    return game.to_dict('records')

@app.callback(
    Output('most_double_match_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_double_match().head()

    fig = px.bar(game, x = 'Runs', y = 'Match')

    fig.update_layout(
        title = dict(text = 'Most Double/ Tripple in a match', x=0.5),
        xaxis = dict(title = 'Double/ Tripple'),
        yaxis = dict(title = 'Match')
    )
    return fig


# power play
@app.callback(
    Output('most_run_power_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_power_team()
    return game.to_dict('records')

@app.callback(
    Output('most_run_power_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_power_team().head()

    fig = px.bar(game, x = 'Runs', y = 'Team')

    fig.update_layout(
        title = dict(text = 'Most run in powerplay for a team', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_run_power_innings_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_power_innings_team()
    return game.to_dict('records')

@app.callback(
    Output('most_run_power_innings_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_power_innings_team().head()
    string = [f'Team: {t}' for t in game['Team']]
    fig = px.bar(game, x = 'Runs', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most run in powerplay for a team in an innings', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_run_power_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_power_player()
    return game.to_dict('records')

@app.callback(
    Output('most_run_power_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_power_player().head()
    fig = px.bar(game, x = 'Runs', y = 'Batsman')

    fig.update_layout(
        title = dict(text = 'Most run in powerplay for a batsman', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_strike_power_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_power_team()
    return game.to_dict('records')

@app.callback(
    Output('most_strike_power_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_power_team().head()
    fig = px.bar(game, x = 'Strk Rate', y = 'Team')

    fig.update_layout(
        title = dict(text = 'Most strike rate in powerplay for a team', x=0.5),
        xaxis = dict(title = 'Strike Rate'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_strike_power_innings_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_power_innings_team()
    return game.to_dict('records')

@app.callback(
    Output('most_strike_power_innings_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_power_innings_team().head()
    string = [f'Team: {t}' for t in game['Team']]
    fig = px.bar(game, x = 'Strk Rate', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most strike rate in powerplay for a team in an innings', x=0.5),
        xaxis = dict(title = 'Strike Rate'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_strike_power_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_power_player()
    return game.to_dict('records')

@app.callback(
    Output('most_strike_power_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_power_player().head()
    string = [f'Run: {r}' for r in game['Runs']]
    fig = px.bar(game, x = 'Strk Rate', y = 'Batsman', text = string)

    fig.update_layout(
        title = dict(text = 'Most strike rate in powerplay for a batsman', x=0.5),
        xaxis = dict(title = 'Strike Rate'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_strike_power_match_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_power_match_player()
    return game.to_dict('records')

@app.callback(
    Output('most_strike_power_match_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_power_match_player().head()
    string = [f'Run: {b}' for b in game['Batsman']]
    fig = px.bar(game, x = 'Strk Rate', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most strike rate in powerplay for a batsman', x=0.5),
        xaxis = dict(title = 'Strike Rate'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_wicket_power_innings_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_power_innings_bowler()
    return game.to_dict('records')

@app.callback(
    Output('most_wicket_power_innings_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_power_innings_bowler().head()
    string = [f'Match: {m}\nAgainst: {i}' for m, i in zip(game['Match'], game['Innings'])]

    fig = px.bar(game, x = 'Wicket', y = 'Bowler', text = string)

    fig.update_layout(
        title = dict(text = 'Most wicket in powerplay innings for a bowler', x=0.5),
        xaxis = dict(title = 'Wicket'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('most_wicket_power_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_power_bowler()
    return game.to_dict('records')

@app.callback(
    Output('most_wicket_power_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_power_bowler().head()
    fig = px.bar(game, x = 'Wicket', y = 'Bowler')

    fig.update_layout(
        title = dict(text = 'Most wicket in powerplay for a bowler', x=0.5),
        xaxis = dict(title = 'Wicket'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('lowest_economy_power_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_economy_power_bowler()
    game = game[game['Over'] >= 4]
    return game.to_dict('records')

@app.callback(
    Output('lowest_economy_power_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_economy_power_bowler()
    game = game[game['Over'] >= 4].head()
    fig = px.bar(game, x = 'Economy', y = 'Bowler')

    fig.update_layout(
        title = dict(text = 'Lowest economy in powerplay for a bowler (min 4 overs)', x=0.5),
        xaxis = dict(title = 'Economy'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('lowest_average_power_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_average_power_bowler()
    game = game[game['Over'] >= 4]
    return game.to_dict('records')

@app.callback(
    Output('lowest_average_power_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_average_power_bowler()
    game = game[game['Over'] >= 4].head()
    fig = px.bar(game, x = 'Average', y = 'Bowler')

    fig.update_layout(
        title = dict(text = 'Lowest average in powerplay for a bowler (min 4 overs)', x=0.5),
        xaxis = dict(title = 'Average'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('most_out_power_batsman', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_out_power_batsman()
    return game.to_dict('records')

@app.callback(
    Output('most_out_power_batsman_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_out_power_batsman().head()
    fig = px.bar(game, x = 'Out', y = 'Batsman')

    fig.update_layout(
        title = dict(text = 'Most Dismissed Batsman in powerplay', x=0.5),
        xaxis = dict(title = 'Out'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


# death over
@app.callback(
    Output('most_run_death_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_death_team()
    return game.to_dict('records')

@app.callback(
    Output('most_run_death_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_death_team().head()

    fig = px.bar(game, x = 'Runs', y = 'Team')

    fig.update_layout(
        title = dict(text = 'Most run in death-over for a team', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_run_death_innings_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_death_innings_team()
    return game.to_dict('records')

@app.callback(
    Output('most_run_death_innings_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_death_innings_team().head()
    string = [f'Team: {t}' for t in game['Team']]
    fig = px.bar(game, x = 'Runs', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most run in death-over for a team in an innings', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_run_death_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_death_player()
    return game.to_dict('records')

@app.callback(
    Output('most_run_death_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_run_death_player().head()
    fig = px.bar(game, x = 'Runs', y = 'Batsman')

    fig.update_layout(
        title = dict(text = 'Most run in death-over for a batsman', x=0.5),
        xaxis = dict(title = 'Run'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_strike_death_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_death_team()
    return game.to_dict('records')

@app.callback(
    Output('most_strike_death_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_death_team().head()
    fig = px.bar(game, x = 'Strk Rate', y = 'Team')

    fig.update_layout(
        title = dict(text = 'Most strike rate in death-over for a team', x=0.5),
        xaxis = dict(title = 'Strike Rate'),
        yaxis = dict(title = 'Team')
    )
    return fig


@app.callback(
    Output('most_strike_death_innings_team', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_death_innings_team()
    return game.to_dict('records')

@app.callback(
    Output('most_strike_death_innings_team_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_death_innings_team().head()
    string = [f'Team: {t}' for t in game['Team']]
    fig = px.bar(game, x = 'Strk Rate', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most strike rate in death-over for a team in an innings', x=0.5),
        xaxis = dict(title = 'Strike Rate'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_strike_death_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_death_player()
    return game.to_dict('records')

@app.callback(
    Output('most_strike_death_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_death_player().head()
    string = [f'Run: {r}' for r in game['Runs']]
    fig = px.bar(game, x = 'Strk Rate', y = 'Batsman', text = string)

    fig.update_layout(
        title = dict(text = 'Most strike rate in death-over for a batsman', x=0.5),
        xaxis = dict(title = 'Strike Rate'),
        yaxis = dict(title = 'Batsman')
    )
    return fig


@app.callback(
    Output('most_strike_death_match_player', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_death_match_player()
    return game.to_dict('records')

@app.callback(
    Output('most_strike_death_match_player_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_strike_death_match_player().head()
    string = [f'Run: {b}' for b in game['Batsman']]
    fig = px.bar(game, x = 'Strk Rate', y = 'Match', text = string)

    fig.update_layout(
        title = dict(text = 'Most strike rate in death-over for a batsman', x=0.5),
        xaxis = dict(title = 'Strike Rate'),
        yaxis = dict(title = 'Match')
    )
    return fig


@app.callback(
    Output('most_wicket_death_innings_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_death_innings_bowler()
    return game.to_dict('records')

@app.callback(
    Output('most_wicket_death_innings_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_death_innings_bowler().head()
    string = [f'Match: {m}\nAgainst: {i}' for m, i in zip(game['Match'], game['Innings'])]

    fig = px.bar(game, x = 'Wicket', y = 'Bowler', text = string)

    fig.update_layout(
        title = dict(text = 'Most wicket in death-over innings for a bowler', x=0.5),
        xaxis = dict(title = 'Wicket'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('most_wicket_death_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_death_bowler()
    return game.to_dict('records')

@app.callback(
    Output('most_wicket_death_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_wicket_death_bowler().head()
    fig = px.bar(game, x = 'Wicket', y = 'Bowler')

    fig.update_layout(
        title = dict(text = 'Most wicket in death-over for a bowler', x=0.5),
        xaxis = dict(title = 'Wicket'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('lowest_economy_death_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_economy_death_bowler()
    game = game[game['Over'] >= 4]
    return game.to_dict('records')

@app.callback(
    Output('lowest_economy_death_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_economy_death_bowler()
    game = game[game['Over'] >= 4].head()
    fig = px.bar(game, x = 'Economy', y = 'Bowler')

    fig.update_layout(
        title = dict(text = 'Lowest economy in death-over for a bowler (min 4 overs)', x=0.5),
        xaxis = dict(title = 'Economy'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('lowest_average_death_bowler', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_average_death_bowler()
    game = game[game['Over'] >= 4]
    return game.to_dict('records')

@app.callback(
    Output('lowest_average_death_bowler_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).lowest_average_death_bowler()
    game = game[game['Over'] >= 4].head()
    fig = px.bar(game, x = 'Average', y = 'Bowler')

    fig.update_layout(
        title = dict(text = 'Lowest average in death-over for a bowler (min 4 overs)', x=0.5),
        xaxis = dict(title = 'Average'),
        yaxis = dict(title = 'Bowler')
    )
    return fig


@app.callback(
    Output('most_out_death_batsman', 'data'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_out_death_batsman()
    return game.to_dict('records')

@app.callback(
    Output('most_out_death_batsman_graph', 'figure'),
    Input('stage', 'value'),
)
def get_info(stage):
    game =  Cricket(df, stage).most_out_death_batsman().head()
    fig = px.bar(game, x = 'Out', y = 'Batsman')

    fig.update_layout(
        title = dict(text = 'Most Dismissed Batsman in death-over', x=0.5),
        xaxis = dict(title = 'Out'),
        yaxis = dict(title = 'Batsman')
    )
    return fig



# Run the app
if __name__ == '__main__':
    app.run(debug = True)
