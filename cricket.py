import pandas as pd

class Cricket:
    """"
    A class to represent the game.
    ...
    Attributes
    -----------
    df: DataFrame
        A pandas dataframe
    stage: str
        Stage of game (i.e., group, super 12, semi, final, all).
        Default value is all.

    Methods
    ------------
    info: Information about game, teams etc
    team_run : DataFrame
    most_winning_team : DataFrame
    most_winning_innings : DataFrame
    most_fours_innings : DataFrame
    most_fours_team : DataFrame
    most_fours_match : DataFrame
    most_sixes_innings : DataFrame
    most_sixes_team : DataFrame
    most_sixes_match : DataFrame
    most_boundaries_innings : DataFrame
    most_boundaries_team : DataFrame
    most_boundaries_match : DataFrame
    most_fours_innings_player : DataFrame
    most_fours_team_player : DataFrame
    most_fours_match_player : DataFrame
    most_sixes_innings_player : DataFrame
    most_sixes_team_player : DataFrame
    most_sixes_match_player : DataFrame
    most_wide_run_team : DataFrame
    most_noball_run_team : DataFrame
    most_single_innings : DataFrame
    most_single_team : DataFrame
    most_single_match : DataFrame
    most_double_innings : DataFrame
    most_double_team : DataFrame
    most_double_match : DataFrame
    most_played_team : DataFrame
    most_played_batsman : DataFrame
    most_played_bowler : DataFrame
    most_win_match_ratio : DataFrame
    most_out_batsman : DataFrame
    most_out_power_batsman : DataFrame
    most_out_death_batsman : DataFrame
    most_wicket_innings_bowler : DataFrame
    most_wicket_match_bowler : DataFrame
    most_wicket_bowler : DataFrame
    most_wicket_power_innings_bowler : DataFrame
    most_wicket_power_match_bowler : DataFrame
    most_wicket_power_bowler : DataFrame
    most_wicket_death_innings_bowler : DataFrame
    most_wicket_death_match_bowler : DataFrame
    most_wicket_death_bowler : DataFrame
    lowest_economy_bowler : DataFrame
    lowest_economy_power_bowler : DataFrame
    lowest_economy_death_bowler : DataFrame
    lowest_average_bowler : DataFrame
    lowest_average_power_bowler : DataFrame
    lowest_average_death_bowler : DataFrame
    most_run_innings_player : DataFrame
    most_run_match_player : DataFrame
    most_run_team_player : DataFrame
    most_run_player : DataFrame
    most_average_batsman : DataFrame
    most_run_power_team : DataFrame
    most_run_power_innings_team : DataFrame
    most_run_power_player : DataFrame
    most_run_power_match_player : DataFrame
    most_strike_power_team : DataFrame
    most_strike_power_innings_team : DataFrame
    most_strike_power_player : DataFrame
    most_strike_power_match_player : DataFrame
    most_run_death_team : DataFrame
    most_run_death_player : DataFrame
    most_run_death_match_player : DataFrame
    most_strike_death_team : DataFrame
    most_strike_death_innings_team : DataFrame
    most_strike_death_player : DataFrame
    most_strike_death_match_player : DataFrame
    """
    def __init__(self, df, stage = 'all'):
        # self.df = df
        self.stage = stage
        
        if stage.lower().strip() == 'group':
            start, end = 1298146, 1298135
        elif stage.lower().strip() == 'super 12':
            start, end = 1298176, 1298147
        elif stage.lower().strip() == 'semi':
            start, end = 1298178, 1298177
        elif stage.lower().strip() == 'final':
            start, end = 1298179, 1298179
        else:
            start, end = 1298179, 1298135
            
        self.df = df.loc[start : end]
        
        # self.teams = df['current_innings'].unique()
        # self.matches = df['match_name'].unique()
        
        # self.team_runs = df.pivot_table(index = ['match_name', 'current_innings'], values= 'runs', aggfunc= 'sum')  

           
    def info(self):
        """Returns information about the tournament.

        Returns:
            str: Team number, Team names and total match
        """

        df = self.df
        self.teams = df['current_innings'].unique()
        self.matches = df['match_name'].unique()
        
        # print((f'T20 World Cup: {self.stage.capitalize()}'))        
        # print(f'Total Team in {self.stage} round:', len(self.teams))        
        # print(f'Teams: {self.teams}')        
        # print(f'Total Match in {self.stage} round:', len(self.matches))
        return (f'T20 World Cup: {self.stage.capitalize()}' + '\n... '
                f'Total Team in {self.stage} round: {len(self.teams)}' + '\n... '
                f'Teams: {self.teams}' + '\n... '
                f'Total Match in {self.stage} round: {len(self.matches)}'
                )
    
    def team_run(self):
        """match-wise team run

        Returns:
            DataFrame: match-wise team run
        """
        
        df1 = self.df.copy()
        df1.rename({'current_innings': 'Team', 'runs' : 'Run'}, axis = 1, inplace= True)        
        # self.team_runs = df.pivot_table(index = ['match_name', 'current_innings'], values= 'runs', aggfunc= 'sum')
        return df1.pivot_table(index = ['match_id', 'match_name', 'Team'], values= 'Run', aggfunc= 'sum')
    
    # def team_run_plot(self):
    #     df = self.team_run().reset_index()
        
    #     # plt.figure(figsize=(6, df.shape[1]+8))
    #     # plt.barh(df['match_name'] + "_" + df['current_innings'], df['runs'])
    #     # plt.barh(y = df['current_innings'], width = df['runs'])
    #     sns.barplot(x = df['runs'], y = df['match_name'] + '_' + df['current_innings'], hue= df['current_innings'] )
    #     plt.grid(axis = 'x')

    #     # for index, value in enumerate(df['runs']):
    #     #     plt.text(df['runs'][index], index, value, va = 'center', ha = 'center')
        
    #     plt.title(f'T20 Wolrld Cup ({self.stage}): Team Winnings')
    #     plt.xlabel('Win')
    #     plt.ylabel('Team')
    #     plt.tight_layout;
        
    
    def team_run_timeline(self, team):
        """timeline of individual team's run sequentilly.

        Returns:
            DataFrame: individual team's run in a sequence
        """
        
        df1 = self.team_run().copy().reset_index()
        
        # df['Opposition'] = df['match_name'].apply(lambda x: x[:4])       
        return df1[df1['Team'] == team.upper()].sort_values(by = 'match_id')
        
    
    def most_winning_team(self):
        """Number of Wins for each team

        Returns:
            DataFrame: Number of wins
        """
        
        df1 = self.team_run().copy()
        cache = [df1['Run'].loc[index[0]].max() for index in df1.index]
        win = df1[cache == df1['Run']].reset_index()
        win.rename({'Team' : 'winner'}, axis = 1, inplace= True)
        
        win_count = win['winner'].value_counts()
        # win_count_relative = round(win['winner'].value_counts(normalize = True)*100, 2)
        
        return pd.DataFrame({
            'Team' : win_count.index,
            'Wins' : win_count.values,
        })
    
    # def winning_team_plot(self):
    #     df = self.winning_team()
    #     # win_count = win['winner'].value_counts()
    #     # rel_win_count = win['winner'].value_counts(normalize = True)
        
    #     # plt.figure(figsize = (6, 3))
    #     plt.barh(y = df['Team'], width = df['Wins'])
    #     plt.grid(axis = 'x')

    #     for index, value in enumerate(df['win %']):
    #         plt.text(0.5, index, f'{value}%', va = 'center', ha = 'center')
        
    #     plt.title(f'T20 Wolrld Cup ({self.stage}): Team Winnings')
    #     plt.xlabel('Win')
    #     plt.ylabel('Team');
    
    
    def most_winning_innings(self):
        """Which innings wins more? Innings 1 or 2.

        Returns:
            DataFrame: innings-wise winning number
        """
        
        df1 = self.df.copy()
        df1 = df1.pivot_table(index = ['match_name', 'innings_id'], values= 'runs', aggfunc= 'sum')
        
        cache = [df1['runs'].loc[index[0]].max() for index in df1.index]
        win = df1[cache == df1['runs']].reset_index()
        
        win.rename({'innings_id' : 'Innings'}, axis = 1, inplace= True)
        win_count = win['Innings'].value_counts()
        win_count_relative = round(win['Innings'].value_counts(normalize = True)*100, 2)

        return pd.DataFrame({
            'Innings_No.' : win_count.index,
            'Wins' : win_count.values,
            'win %' : win_count_relative.values
        })

    
    def most_fours_innings(self):
        """Most fours for an innings

        Returns:
            DataFrame: Number of fours for an innings
        """
        
        df = self.df.copy()
        df_fours = df[(df['runs'] == 4) & df['isBoundary']]
        return (df_fours.pivot_table(index = ['match_name', 'current_innings'], values= 'isBoundary', aggfunc= 'count')
            .reset_index()
            .rename({'current_innings' : 'Innings', 'isBoundary' : 'Fours'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Fours', ascending = False)
            # .set_index('Country')
            )
    
    
    def most_fours_team(self):
        """Most fours for a team

        Returns:
            DataFrame: Number of  fours for a team
        """
        
        df = self.most_fours_innings().copy()

        return (df.pivot_table(index = ['Innings'], values= 'Fours', aggfunc= 'sum')
            .reset_index()
            .rename({'Innings' : 'Team'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Fours', ascending = False)
            # .set_index('Country')
            )

        
    def most_fours_match(self):
        """Most fours for a match

        Returns:
            DataFrame: Number of fours for a match
        """
        
        df = self.most_fours_innings().copy()

        return (df.pivot_table(index = ['match_name'], values= 'Fours', aggfunc= 'sum')
            .reset_index()
            .rename({'match_name' : 'Match'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Fours', ascending = False)
            # .set_index('Country')
            )
        
        
    def most_sixes_innings(self):
        """Most sixes for an innings

        Returns:
            DataFrame: Number of sixes for an innings
        """
        
        df = self.df.copy()
        df_sixes = df[(df['runs'] == 6) & df['isBoundary']]
        return (df_sixes.pivot_table(index = ['match_name', 'current_innings'], values= 'isBoundary', aggfunc= 'count')
            .reset_index()
            .rename({'current_innings' : 'Innings', 'isBoundary' : 'Sixes'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Sixes', ascending = False)
            # .set_index('Country')
            )


    def most_sixes_team(self):
        """Most sixes for a team

        Returns:
            DataFrame: Number of  sixes for a team
        """
        
        df = self.most_sixes_innings().copy()

        return (df.pivot_table(index = ['Innings'], values= 'Sixes', aggfunc= 'sum')
            .reset_index()
            .rename({'Innings' : 'Team'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Sixes', ascending = False)
            # .set_index('Country')
            )

        
    def most_sixes_match(self):
        """Most sixes for a match

        Returns:
            DataFrame: Number of sixes for a match
        """
        
        df = self.most_sixes_innings().copy()

        return (df.pivot_table(index = ['match_name'], values= 'Sixes', aggfunc= 'sum')
            .reset_index()
            .rename({'match_name' : 'Match'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Sixes', ascending = False)
            # .set_index('Country')
            )


    def most_boundaries_innings(self):
        """Most boundaries for an innings

        Returns:
            DataFrame: Number of boundaries for an innings
        """
        
        fours = self.most_fours_innings().copy()
        sixes = self.most_sixes_innings().copy()
        
        fours = fours.pivot_table(index = 'Innings', values = 'Fours', aggfunc= 'max')
        sixes = sixes.pivot_table(index = 'Innings', values = 'Sixes', aggfunc= 'max')
        
        df = pd.concat([fours, sixes], axis = 1)
        df['Boundaries'] = df['Fours'] + df['Sixes']
        return df.reset_index().sort_values('Boundaries', ascending= False)
    
    
    def most_boundaries_team(self):
        """Most boundaries for a team

        Returns:
            DataFrame: Number of  boundaries for a team
        """
        
        fours = self.most_fours_team().copy().set_index('Team')
        sixes = self.most_sixes_team().copy().set_index('Team')
        
        df = pd.concat([fours, sixes], axis = 1)
        df['Boundaries'] = df['Fours'] + df['Sixes']
        return df.reset_index().sort_values('Boundaries', ascending= False)


    def most_boundaries_match(self):
        """Most boundaries for a match

        Returns:
            DataFrame: Number of boundaries for a match
        """
        
        fours = self.most_fours_match().copy().set_index('Match')
        sixes = self.most_sixes_match().copy().set_index('Match')
        
        df = pd.concat([fours, sixes], axis = 1)
        df['Boundaries'] = df['Fours'] + df['Sixes']
        return df.reset_index().sort_values('Boundaries', ascending= False)


    def most_fours_innings_player(self):
        """Batsman with the highest fours for an innings

        Returns:
            DataFrame: Batsman with the highest fours for an innings
        """
        
        df = self.df.copy()
        df_fours = df[(df['runs'] == 4) & df['isBoundary']]
        return (df_fours.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values= 'isBoundary', aggfunc= 'count')
            .reset_index()
            .rename({'current_innings' : 'Innings', 'isBoundary' : 'Fours', 'batsman1_name' : 'Batsman'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Fours', ascending = False)
            # .set_index('Country')
            )
    
    
    def most_fours_team_player(self):
        """Batsman with the highest fours for a team
        Returns:
            DataFrame: Batsman with the highest fours for a team
        """
        
        df = self.most_fours_innings_player()

        df1 =  (df.pivot_table(index = ['Innings', 'Batsman'], values= 'Fours', aggfunc= 'sum')
            .reset_index()
            .rename({'Innings' : 'Team'}, axis = 1)
            # .drop(columns='match_name')
            # .sort_values(by = 'Fours', ascending = False)
            # .set_index('Country')
            )
        return (df1.pivot_table(index = ['Team'], values= ['Batsman', 'Fours'], aggfunc= 'max')
            .reset_index()
            .sort_values(by = 'Fours', ascending = False)
            )

        
    def most_fours_match_player(self):
        """Batsman with the highest fours for a match
        Returns:
            DataFrame: Batsman with the highest fours for a match
        """
        
        df = self.most_fours_innings_player()

        return (df.pivot_table(index = ['match_name', 'Batsman'], values= 'Fours', aggfunc= 'sum')
            .reset_index()
            .rename({'match_name' : 'Match'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Fours', ascending = False)
            # .set_index('Country')
            )


    def most_sixes_innings_player(self):
        """Batsman with the highest sixes for an innings

        Returns:
            DataFrame: Batsman with the highest sixes for an innings
        """
        
        df = self.df.copy()
        df_sixes = df[(df['runs'] == 6) & df['isBoundary']]
        return (df_sixes.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values= 'isBoundary', aggfunc= 'count')
            .reset_index()
            .rename({'current_innings' : 'Innings', 'isBoundary' : 'Sixes', 'batsman1_name' : 'Batsman'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Sixes', ascending = False)
            # .set_index('Country')
            )
    
    
    def most_sixes_team_player(self):
        """Batsman with the highest sixes for a team
        Returns:
            DataFrame: Batsman with the highest sixes for a team
        """
        
        df = self.most_sixes_innings_player()

        df1 =  (df.pivot_table(index = ['Innings', 'Batsman'], values= 'Sixes', aggfunc= 'sum')
            .reset_index()
            .rename({'Innings' : 'Team'}, axis = 1)
            # .drop(columns='match_name')
            # .sort_values(by = 'Fours', ascending = False)
            # .set_index('Country')
            )
        return (df1.pivot_table(index = ['Team'], values= ['Batsman', 'Sixes'], aggfunc= 'max')
            .reset_index()
            .sort_values(by = 'Sixes', ascending = False)
            )

        
    def most_sixes_match_player(self):
        """Batsman with the highest sixes for a match
        Returns:
            DataFrame: Batsman with the highest sixes for a match
        """
        
        df = self.most_sixes_innings_player()

        return (df.pivot_table(index = ['match_name', 'Batsman'], values= 'Sixes', aggfunc= 'sum')
            .reset_index()
            .rename({'match_name' : 'Match'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Sixes', ascending = False)
            # .set_index('Country')
            )

    
    def most_wide_run_innings_team(self):
        """The team which get most wide run in an innings
        Returns:
            DataFrame: Team and Wide run
        """
        
        df = self.df.copy()
        df_wide = df[df['isWide']]
        
        df_wide = df_wide.pivot_table(index = ['match_name', 'current_innings'], values= 'isWide', aggfunc= 'count').reset_index()
        
        return (df_wide.pivot_table(index = ['match_name', 'current_innings'], values= ['isWide'], aggfunc= 'max')
            .reset_index()
            .rename({'match_name' : 'Match', 'current_innings' : 'Team', 'isWide' : 'Wide'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Wide', ascending = False)
            # .set_index('Country')
            )

    
    def most_noball_run_innings_team(self):
        """The team which get most noball run in an innings
        Returns:
            DataFrame: Team and noball run
        """
        
        df = self.df.copy()
        df_noball = df[df['isNoball']]
        
        df_noball = df_noball.pivot_table(index = ['match_name', 'current_innings'], values= 'isNoball', aggfunc= 'count').reset_index()
        
        return (df_noball.pivot_table(index = ['match_name', 'current_innings'], values= 'isNoball', aggfunc= 'count')
            .reset_index()
            .rename({'match_name' : 'Match', 'current_innings' : 'Team', 'isNoball' : 'NoBall'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'NoBall', ascending = False)
            # .set_index('Country')
            )
       
    
    def most_single_innings(self):
        """Most single for an innings

        Returns:
            DataFrame: Number of single for an innings
        """
        
        df = self.df.copy()
        df_single = df[~df['isWide'] & ~df['isNoball'] & (df['runs'] == 1)]
        return (df_single.pivot_table(index = ['match_name', 'current_innings'], values= 'runs', aggfunc= 'sum')
            .reset_index()
            .rename({'match_name' : 'Match', 'current_innings' : 'Innings', 'runs' : 'Single'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Single', ascending = False)
            # .set_index('Country')
            )
    
    
    def most_single_team(self):
        """Most single for a team

        Returns:
            DataFrame: Number of  single for a team
        """
        
        df = self.most_single_innings().copy()

        return (df.pivot_table(index = ['Innings'], values= 'Single', aggfunc= 'sum')
            .reset_index()
            .rename({'Innings' : 'Team'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Single', ascending = False)
            # .set_index('Country')
            )

        
    def most_single_match(self):
        """Most single for a match

        Returns:
            DataFrame: Number of single for a match
        """
        
        df = self.most_single_innings().copy()

        return (df.pivot_table(index = ['Match'], values= 'Single', aggfunc= 'sum')
            .reset_index()
            # .rename({'match_name' : 'Match'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Single', ascending = False)
            # .set_index('Country')
            )
    
    
    def most_double_innings(self):
        """Most double/ tripple for an innings

        Returns:
            DataFrame: Number of double/ tripple for an innings
        """
        
        df = self.df.copy()
        df_double = df[(~df['isWide'] & ~df['isNoball']) & ((df['runs'] == 2) | (df['runs'] == 3))]
        return (df_double.pivot_table(index = ['match_name', 'current_innings'], values= 'runs', aggfunc= 'sum')
            .reset_index()
            .rename({'match_name' : 'Match', 'current_innings' : 'Innings', 'runs' : 'Runs'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Runs', ascending = False)
            # .set_index('Country')
            )
    
    
    def most_double_team(self):
        """Most double/ tripple for a team

        Returns:
            DataFrame: Number of  double/ tripple for a team
        """
        
        df = self.most_double_innings().copy()

        return (df.pivot_table(index = ['Innings'], values= 'Runs', aggfunc= 'sum')
            .reset_index()
            .rename({'Innings' : 'Team'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Runs', ascending = False)
            # .set_index('Country')
            )

        
    def most_double_match(self):
        """Most double/ tripple for a match

        Returns:
            DataFrame: Number of double/ tripple for a match
        """
        
        df = self.most_double_innings().copy()

        return (df.pivot_table(index = ['Match'], values= 'Runs', aggfunc= 'sum')
            .reset_index()
            # .rename({'match_name' : 'Match'}, axis = 1)
            # .drop(columns='match_name')
            .sort_values(by = 'Runs', ascending = False)
            # .set_index('Country')
            )
    

    def most_played_team(self):
        """The team which played most matches in T20 world cup, 2022
        Returns:
            DataFrame: Team and Number of played match
        """
        
        df = self.df.copy()               
        df = (df.pivot_table(index = ["current_innings"], values = 'match_name', aggfunc= lambda x: ', '.join(x.unique()))
            .reset_index()
            .rename({"current_innings" : 'Team', 'match_name' : 'Matches'}, axis = 1)
            )
        
        df['Match'] = df['Matches'].apply(lambda x: x.count(',') + 1)            
        return df.sort_values(by = 'Match', ascending = False)

    
    def most_played_batsman(self):
        """The batsman who played most matches in T20 world cup, 2022
        Returns:
            DataFrame: batsman name and Number of played match
        """
        
        df = self.df.copy()        
        # df = (df.groupby('batsman1_name')['match_name'].unique()
        #     .reset_index()
        #     .rename({'batsman1_name' : 'Batsman', 'match_name' : 'Matches'}, axis = 1)
        #     )
        
        df = (df.pivot_table(index = ["batsman1_name"], values = 'match_name', aggfunc= lambda x: ', '.join(x.unique()))
            .reset_index()
            .rename({'batsman1_name' : 'Batsman', 'match_name' : 'Matches'}, axis = 1)
            )
        
        df['Match'] = df['Matches'].apply(lambda x: x.count(',') + 1)            
        return df.sort_values(by = 'Match', ascending = False)


    def most_played_bowler(self):
        """The bowler who played most matches in T20 world cup, 2022
        Returns:
            DataFrame: bowler name and Number of played match
        """
        
        df = self.df.copy()               
        df = (df.pivot_table(index = ["bowler1_name"], values = 'match_name', aggfunc= lambda x: ', '.join(x.unique()))
            .reset_index()
            .rename({'bowler1_name' : 'Bowler', 'match_name' : 'Matches'}, axis = 1)
            )
        
        df['Match'] = df['Matches'].apply(lambda x: x.count(',') + 1)            
        return df.sort_values(by = 'Match', ascending = False)
    

    def most_win_match_ratio(self):
        """The team which has most win per match ratio
        Returns:
            DataFrame: win per match ratio
        """
        
        df_win = self.most_winning_team().copy().set_index('Team')
        df_match = self.most_played_team().copy().set_index('Team')
        
        df = pd.concat([df_match, df_win], axis= 1).drop(columns = 'Matches')
        df['Ratio %'] = (df['Wins'] / df['Match']*100).round(2)
        return df.reset_index().sort_values(by = 'Ratio %', ascending= False)
    
            
    def most_out_batsman(self):
        """The batsman who got out most of the times in T20 world cup, 2022
        Returns:
            DataFrame: batsman name and Number of dismissal
        """
        
        df = self.df.copy()
        
        df1 = df[df['wkt_batsman_name'].notna()]
        
        df1['wkt_text_m'] = [split[1][0]+" "+split[1] for split in df1['wkt_text'].str.split(" ")]
        
        df1['batsman1_name_m'] = [split[1][0]+" "+split[-1] for split in df1['batsman1_name'].str.split(" ")]
        df = df1[df1['wkt_text_m'] == df1['batsman1_name_m']]
        df['wkt_text_m'] = df['batsman1_name']
        
        df = (df.pivot_table(index = ['wkt_text_m'], values = 'match_name', aggfunc= lambda x: x.nunique())
            .reset_index()
            .rename({'wkt_text_m' : 'Batsman', 'match_name' : 'Out'}, axis = 1)
            .set_index('Batsman')
            )
        
        df2 = self.most_played_batsman().copy().set_index('Batsman')
        
        df = pd.concat([df, df2], axis = 1).reset_index()
        
        return df.drop(columns = ['Matches']).sort_values(by = 'Out', ascending = False)
    
    
    def most_out_power_batsman(self):
        """The batsman who got out most of the times in power play in T20 world cup, 2022
        Returns:
            DataFrame: batsman name and Number of dismissal
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 1) & (df['over'] <= 6)]
        
        df1 = df[df['wkt_batsman_name'].notna()]
        df1['wkt_text_m'] = [split[1][0]+" "+split[1] for split in df1['wkt_text'].str.split(" ")]
        df1['batsman1_name_m'] = [split[1][0]+" "+split[-1] for split in df1['batsman1_name'].str.split(" ")]
        df = df1[df1['wkt_text_m'] == df1['batsman1_name_m']]
        df['wkt_text_m'] = df['batsman1_name']
        
        df = (df.pivot_table(index = ['wkt_text_m'], values = 'match_name', aggfunc= lambda x: x.nunique())
            .reset_index()
            .rename({'wkt_text_m' : 'Batsman', 'match_name' : 'Out'}, axis = 1)
            )
        
        return df.sort_values(by = 'Out', ascending = False)
    
    
    def most_out_death_batsman(self):
        """The batsman who got out most of the times in death over in T20 world cup, 2022
        Returns:
            DataFrame: batsman name and Number of dismissal
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        
        df1 = df[df['wkt_batsman_name'].notna()]
        df1['wkt_text_m'] = [split[1][0]+" "+split[1] for split in df1['wkt_text'].str.split(" ")]
        df1['batsman1_name_m'] = [split[1][0]+" "+split[-1] for split in df1['batsman1_name'].str.split(" ")]
        df = df1[df1['wkt_text_m'] == df1['batsman1_name_m']]
        df['wkt_text_m'] = df['batsman1_name']
        
        df = (df.pivot_table(index = ['wkt_text_m'], values = 'match_name', aggfunc= lambda x: x.nunique())
            .reset_index()
            .rename({'wkt_text_m' : 'Batsman', 'match_name' : 'Out'}, axis = 1)
            )
        
        return df.sort_values(by = 'Out', ascending = False)


    def most_wicket_innings_bowler(self):
        """The bowler who got most wicket in an innings
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.df.copy()
        df1 = df[(df['wkt_text'].notna()) & (df['wkt_text'].str.contains(' b '))]
        df1['wkt_text_m'] = df1['bowler1_name']
        df = (df1.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = 'wkt_text_m', aggfunc= 'count')
            .reset_index()
            .rename({'match_name': 'Match', 'current_innings' : 'Innings', 'bowler1_name' : 'Bowler', 'wkt_text_m' : 'Wicket'}, axis = 1)
            )
    
        return df.sort_values(by = 'Wicket', ascending = False)
    
    
    def most_wicket_match_bowler(self):
        """The bowler who got most wicket in a match
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.most_wicket_innings_bowler().copy()
        
        df_match = df.pivot_table(index= ['Match'], values= ['Wicket', 'Bowler'], aggfunc= 'max').reset_index().sort_values(by = 'Wicket', ascending = False)
        
        # df_player = df.pivot_table(index= ['Bowler'], values= ['Wicket'], aggfunc= 'max').reset_index().sort_values(by = 'Wicket', ascending = False)
        
        # df = pd.merge(df_match, df_player, on='Wicket', how='left')
        
        return df_match
    
    
    def most_wicket_bowler(self):
        """The bowler who got most wicket in T20 world cup, 2022
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.most_wicket_innings_bowler().copy()
        
        df_wicket = df.pivot_table(index= ['Bowler'], values= ['Wicket'], aggfunc= 'sum').reset_index()
        
        # df_wicket['Strk rate'] = (df_run['Runs'] / df_run['Balls'] * 100).round(2)
        
        return df_wicket.sort_values(by = 'Wicket', ascending = False)
    
    
    def most_wicket_power_innings_bowler(self):
        """The bowler who got most wicket in an innings at power play
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 1) & (df['over'] <= 6)]
        
        df1 = df[(df['wkt_text'].notna()) & (df['wkt_text'].str.contains(' b '))]
        df1['wkt_text_m'] = df1['bowler1_name']
        df = (df1.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = 'wkt_text_m', aggfunc= 'count')
            .reset_index()
            .rename({'match_name': 'Match', 'current_innings' : 'Innings', 'bowler1_name' : 'Bowler', 'wkt_text_m' : 'Wicket'}, axis = 1)
            )
    
        return df.sort_values(by = 'Wicket', ascending = False)
    
    
    def most_wicket_power_match_bowler(self):
        """The bowler who got most wicket in a match at power play
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.most_wicket_power_innings_bowler().copy()
        
        df_match = df.pivot_table(index= ['Match', 'Bowler'], values= ['Wicket'], aggfunc= 'max').reset_index().sort_values(by = 'Wicket', ascending = False)
        
        # df_player = df.pivot_table(index= ['Bowler'], values= ['Wicket'], aggfunc= 'max').reset_index().sort_values(by = 'Wicket', ascending = False)
        
        # df = pd.merge(df_match, df_player, on='Wicket', how='left')
        
        return df_match.sort_values(by = 'Wicket', ascending = False)
    
    
    def most_wicket_power_bowler(self):
        """The bowler who got most wicket in T20 world cup, 2022 at power play
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.most_wicket_power_innings_bowler().copy()
        
        df_wicket = df.pivot_table(index= ['Bowler'], values= ['Wicket'], aggfunc= 'sum').reset_index()
        
        return df_wicket.sort_values(by = 'Wicket', ascending = False)
    
    
    def most_wicket_death_innings_bowler(self):
        """The bowler who got most wicket in an innings at death overs
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        
        df1 = df[(df['wkt_text'].notna()) & (df['wkt_text'].str.contains(' b '))]
        df1['wkt_text_m'] = df1['bowler1_name']
        df = (df1.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = 'wkt_text_m', aggfunc= 'count')
            .reset_index()
            .rename({'match_name': 'Match', 'current_innings' : 'Innings', 'bowler1_name' : 'Bowler', 'wkt_text_m' : 'Wicket'}, axis = 1)
            )
    
        return df.sort_values(by = 'Wicket', ascending = False)
    
    
    def most_wicket_death_match_bowler(self):
        """The bowler who got most wicket in a match at death overs
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.most_wicket_death_innings_bowler().copy()
        
        df_match = df.pivot_table(index= ['Match'], values= ['Wicket', 'Bowler'], aggfunc= 'max').reset_index().sort_values(by = 'Wicket', ascending = False)
        
        df_player = df.pivot_table(index= ['Bowler'], values= ['Wicket'], aggfunc= 'max').reset_index().sort_values(by = 'Wicket', ascending = False)
        
        df = pd.merge(df_match, df_player, on='Wicket', how='left')
        
        return df_match.sort_values(by = 'Wicket', ascending = False)
    
    
    def most_wicket_death_bowler(self):
        """The bowler who got most wicket in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: bowler name and number of wickets
        """
        
        df = self.most_wicket_death_innings_bowler().copy()
        
        df_wicket = df.pivot_table(index= ['Bowler'], values= ['Wicket'], aggfunc= 'sum').reset_index()
        
        return df_wicket.sort_values(by = 'Wicket', ascending = False)
        

    
    def lowest_economy_bowler(self):
        """The bowler with the lowest economy in T20 world cup, 2022
        Returns:
            DataFrame: bowler name and economy
        """
        
        df = self.df.copy()
                
        df_cal = df.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc = 'max').reset_index()
        
        df_economy = (df_cal.pivot_table(index = ['bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc= 'sum')
                .reset_index()
                .rename({'bowler1_name' : 'Bowler', 'bowler1_overs' : 'Over', 'bowler1_runs' : 'Runs', 'bowler1_wkts' : 'Wickets'}, axis = 1)
                )
        
        # df_economy = df_economy[df_economy['Wickets'] >= 5]
        
        df_economy[['over', 'ball']] = df_economy['Over'].astype('str').str.split('.', expand = True)
        df_economy['over'] = df_economy['over'].astype('float') + df_economy['ball'].astype('float') / 6
        
        df_economy['Economy'] = (df_economy['Runs'] / df_economy['Over']).round(2)
        
        return (df_economy.sort_values(by = 'Economy')
                .drop(columns = ['over', 'ball', 'Runs'])
                )
        
        
    def lowest_economy_power_bowler(self):
        """The bowler with the lowest economy in T20 world cup, 2022 at power play
        Returns:
            DataFrame: bowler name and economy
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 1) & (df['over'] <= 6)]
                
        df_cal = df.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc = 'max').reset_index()
        
        df_economy = (df_cal.pivot_table(index = ['bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc= 'sum')
                .reset_index()
                .rename({'bowler1_name' : 'Bowler', 'bowler1_overs' : 'Over', 'bowler1_runs' : 'Runs', 'bowler1_wkts' : 'Wickets'}, axis = 1)
                )
        
        df_economy[['over', 'ball']] = df_economy['Over'].astype('str').str.split('.', expand = True)
        df_economy['over'] = df_economy['over'].astype('float') + df_economy['ball'].astype('float') / 6
        
        df_economy['Economy'] = (df_economy['Runs'] / df_economy['Over']).round(2)
        
        return (df_economy.sort_values(by = 'Economy')
                .drop(columns = ['over', 'ball', 'Runs'])
                )  
    
    def lowest_economy_death_bowler(self):
        """The bowler with the lowest economy in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: bowler name and economy
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
                
        df_cal = df.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc = 'max').reset_index()
        
        df_economy = (df_cal.pivot_table(index = ['bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc= 'sum')
                .reset_index()
                .rename({'bowler1_name' : 'Bowler', 'bowler1_overs' : 'Over', 'bowler1_runs' : 'Runs', 'bowler1_wkts' : 'Wickets'}, axis = 1)
                )
        
        df_economy[['over', 'ball']] = df_economy['Over'].astype('str').str.split('.', expand = True)
        df_economy['over'] = df_economy['over'].astype('float') + df_economy['ball'].astype('float') / 6
        
        df_economy['Economy'] = (df_economy['Runs'] / df_economy['Over']).round(2)
        
        return (df_economy.sort_values(by = 'Economy')
                .drop(columns = ['over', 'ball', 'Runs'])
                )


    def lowest_average_bowler(self):
        """The bowler with the lowest average run consumed in T20 world cup, 2022
        Returns:
            DataFrame: bowler name and average run
        """
        
        df = self.df.copy()
                
        df_cal = df.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc = 'max').reset_index()
        
        df_avg = (df_cal.pivot_table(index = ['bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc= 'sum')
                .reset_index()
                .rename({'bowler1_name' : 'Bowler', 'bowler1_overs' : 'Over', 'bowler1_runs' : 'Runs', 'bowler1_wkts' : 'Wickets'}, axis = 1)
                )
        
        # df_avg = df_avg[df_avg['Wickets'] >= 5]
        
        df_avg['Average'] = (df_avg['Runs'] / df_avg['Wickets']).round(2)
        
        return (df_avg.sort_values(by = 'Average')
                .drop(columns = ['Runs'])
                )
       
    def lowest_average_power_bowler(self):
        """The bowler with the lowest average run consumed in T20 world cup, 2022 at power play
        Returns:
            DataFrame: bowler name and average run
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 1) & (df['over'] <= 6)]
                
        df_cal = df.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc = 'max').reset_index()
        
        df_avg = (df_cal.pivot_table(index = ['bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc= 'sum')
                .reset_index()
                .rename({'bowler1_name' : 'Bowler', 'bowler1_overs' : 'Over', 'bowler1_runs' : 'Runs', 'bowler1_wkts' : 'Wickets'}, axis = 1)
                )
        
        df_avg['Average'] = (df_avg['Runs'] / df_avg['Wickets']).round(2)
        
        return (df_avg.sort_values(by = 'Average')
                .drop(columns = ['Runs'])
                )

    
    def lowest_average_death_bowler(self):
        """The bowler with the lowest average run consumed in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: bowler name and average run
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
                
        df_cal = df.pivot_table(index = ['match_name', 'current_innings', 'bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc = 'max').reset_index()
        
        df_avg = (df_cal.pivot_table(index = ['bowler1_name'], values = ['bowler1_overs', 'bowler1_runs', 'bowler1_wkts'], aggfunc= 'sum')
                .reset_index()
                .rename({'bowler1_name' : 'Bowler', 'bowler1_overs' : 'Over', 'bowler1_runs' : 'Runs', 'bowler1_wkts' : 'Wickets'}, axis = 1)
                )
        
        df_avg['Average'] = (df_avg['Runs'] / df_avg['Wickets']).round(2)
        
        return (df_avg.sort_values(by = 'Average')
                .drop(columns = ['Runs'])
                )    


    def most_run_innings_player(self):
        """The batsman with the highest run in an innings in T20 world cup, 2022
        Returns:
            DataFrame: Batsman name, run, and strike rate
        """
        
        df = self.df.copy()

        df_run = df.pivot_table(index= ['match_name', 'current_innings', 'batsman1_name'], values= ['batsman1_runs', 'batsman1_balls'], aggfunc= 'max')
        
        df = (df_run.reset_index()
                .rename({'match_name': 'Match', 'current_innings' : 'Innings', 'batsman1_name'  : 'Batsman', 'batsman1_runs' : 'Runs', 'batsman1_balls' : 'Balls'}, axis = 1)
                )
        
        df['Strk rate'] = (df['Runs'] / df['Balls'] * 100).round(2)
            
        return (df.sort_values(by = 'Runs', ascending = False)
                )
        
    
    def most_run_match_player(self):
        """The batsman with the highest run in a match in T20 world cup, 2022
        Returns:
            DataFrame: Batsman name, run, and strike rate
        """
        
        df = self.most_run_innings_player().copy()

        df_match = df.pivot_table(index= ['Match'], values= ['Runs', 'Balls'], aggfunc= 'max').reset_index().sort_values(by = 'Runs', ascending = False)
        df_player = df.pivot_table(index= ['Batsman'], values= ['Runs'], aggfunc= 'max').reset_index().sort_values(by = 'Runs', ascending = False)
        
        df = pd.merge(df_match, df_player, on='Runs', how='left')
        
        df['Strk rate'] = (df['Runs'] / df['Balls'] * 100).round(2)
        
        return df.sort_values(by = 'Runs', ascending = False)

    
    def most_run_team_player(self):
        """The batsman with the highest run for a team in T20 world cup, 2022
        Returns:
            DataFrame: Batsman name, run, and strike rate
        """
        
        df = self.most_run_innings_player().copy()
        # out = self.most_out_batsman().set_index('Batsman')

        df_run = df.pivot_table(index= ['Innings', 'Batsman'], values= ['Runs', 'Balls'], aggfunc= 'sum').reset_index()
        
        df_run = df_run.pivot_table(index= ['Innings'], values= ['Batsman', 'Runs', 'Balls'], aggfunc= 'max').reset_index()
        
        df_run['Strk rate'] = (df_run['Runs'] / df_run['Balls'] * 100).round(2)
        
        # df = pd.merge(df_run, out, left_index= True, right_index= True)       
        # df['Avg'] = round(df['Runs'] / df['Out'], 2)
        
        return (df_run
                # .drop(columns = ['Balls', 'Out'])
                .rename({'Innings' : 'Team'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
        

    def most_run_player(self):
        """The batsman with the highest run for a team in T20 world cup, 2022
        Returns:
            DataFrame: Batsman name, run, and strike rate
        """
        
        df = self.most_run_innings_player().copy()
        # out = self.most_out_batsman().set_index('Batsman')

        df_run = df.pivot_table(index= ['Innings', 'Batsman'], values= ['Runs', 'Balls'], aggfunc= 'sum')
        
        df_run['Strk rate'] = (df_run['Runs'] / df_run['Balls'] * 100).round(2)
        
        # df = pd.merge(df_run, out, left_index= True, right_index= True)       
        # df['Avg'] = round(df['Runs'] / df['Out'], 2)
        
        return (df_run.reset_index()
                # .drop(columns = ['Balls', 'Out'])
                .rename({'Innings' : 'Team'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
    
    
    def most_average_batsman(self):
        """The batsman with the highest average run in T20 world cup, 2022
        Returns:
            DataFrame: Batsman name, run, average run, and strike rate
        """
        
        df_run = self.most_run_player().copy().set_index('Batsman')
        out = self.most_out_batsman().copy().set_index('Batsman')

        df = pd.merge(df_run, out, left_index= True, right_index= True)
        
        # df = df[df['Runs'] >= 200]       
        df['Strk rate'] = (df['Runs'] / df['Balls'] * 100).round(2)
        df['Avg'] = round(df['Runs'] / (df['Out']), 2)
        # df.replace([np.inf, -np.inf], np.nan, inplace=True)
        return (df.drop(columns = ['Balls', 'Out'])
                .reset_index()
                .sort_values(by = 'Avg', ascending = False)
                # .dropna()
                )

    def most_run_power_team(self):
        """The team with the highest run in T20 world cup, 2022 at power play
        Returns:
            DataFrame: Team name, and run
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 1) & (df['over'] <= 6)]
        
        df_run = df.pivot_table(index = ['match_name', 'current_innings'], values = ['runs'], aggfunc= 'sum')
        
        df_power = df_run.pivot_table(index = ['current_innings'], values = ['runs'], aggfunc= 'sum')
        
        return (df_power.reset_index()
                .rename({'current_innings' : 'Team', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )


    def most_run_power_innings_team(self):
        """The team with the highest run in T20 world cup, 2022 at power play
        Returns:
            DataFrame: Team name, and run
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 1) & (df['over'] <= 6)]
        
        df_run = df.pivot_table(index = ['match_name', 'current_innings'], values = ['runs'], aggfunc= 'sum')
        
        df_power = df_run.pivot_table(index = ['match_name', 'current_innings'], values = ['runs'], aggfunc= 'max')
        
        return (df_power.reset_index()
                .rename({'match_name': 'Match', 'current_innings' : 'Team', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
    
    
    def most_run_power_player(self):
        """The batsman with the highest run in T20 world cup, 2022 at powerplay
        Returns:
            DataFrame: Batsman name, and run
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 1) & (df['over'] <= 6)]
        
        df_run = df.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values = ['batsman1_runs'], aggfunc= 'max')
        
        df_power = df_run.pivot_table(index = ['batsman1_name'], values = ['batsman1_runs'], aggfunc= 'sum')
        
        return (df_power.reset_index()
                .rename({'batsman1_name' : 'Batsman', 'batsman1_runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
    
    
    def most_run_power_match_player(self):
        """The batsman with the highest run for a match in T20 world cup, 2022
        Returns:
            DataFrame: Batsman name, run, and match
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 1) & (df['over'] <= 6)]
        
        df_run = df.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values = ['batsman1_runs'], aggfunc= 'max')
        
        df_power = df_run.pivot_table(index = ['match_name', 'batsman1_name'], values = ['batsman1_runs'], aggfunc= 'max')
        
        return (df_power.reset_index()
                .rename({'match_name': 'Match', 'batsman1_name' : 'Batsman', 'batsman1_runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
    
    
    def most_strike_power_team(self):
        """The team with the highest strike rate in T20 world cup, 2022 at power play
        Returns:
            DataFrame: Team name, run, strike rate and match
        """
        
        df = self.most_run_power_team().copy()
        
        df['Strk Rate'] = (df['Runs'] / [36] * 100).round(2)
        
        return (df
                # .drop(columns = ['batsman1_balls'])
                # .rename({'match_name': 'Match', 'current_innings' : 'Team', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Strk Rate', ascending = False)
                )
    
    def most_strike_power_innings_team(self):
        """The team with the highest strike rate in T20 world cup, 2022 at power play
        Returns:
            DataFrame: Team name, run, strike rate and match
        """
        
        df = self.most_run_power_innings_team().copy()
        
        df['Strk Rate'] = (df['Runs'] / [36] * 100).round(2)
        
        return (df
                # .drop(columns = ['batsman1_balls'])
                # .rename({'match_name': 'Match', 'current_innings' : 'Team', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Strk Rate', ascending = False)
                )
    
    
    def most_strike_power_player(self):
        """The batsman with the highest strike rate in T20 world cup, 2022 at power play
        Returns:
            DataFrame: Batsman name, run, and strike rate
        """
        
        df = self.most_run_power_player().copy()
        df['Strk Rate'] = (df['Runs'] / [36] * 100).round(2)
        return df.sort_values(by = 'Strk Rate', ascending = False)
    
    
    def most_strike_power_match_player(self):
        """The batsman with the highest strike rate for a match in T20 world cup, 2022 at power play
        Returns:
            DataFrame: Batsman name, run, strike rate, and match
        """
        
        df = self.most_run_power_match_player().copy()
        df['Strk Rate'] = (df['Runs'] / [36] * 100).round(2)
        return df.sort_values(by = 'Strk Rate', ascending = False)
        
           
    
    
    def most_run_death_team(self):
        """The team with the highest run in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: Team name, run, and match
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        
        df_run = df.pivot_table(index = ['match_name', 'current_innings'], values = ['runs'], aggfunc= 'sum')
        
        df_power = df_run.pivot_table(index = ['current_innings'], values = ['runs'], aggfunc= 'sum')
        
        return (df_power.reset_index()
                .rename({'current_innings' : 'Team', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
        
    def most_run_death_innings_team(self):
        """The team with the highest run in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: Team name, run, and match
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        
        df_run = df.pivot_table(index = ['match_name', 'current_innings'], values = ['runs'], aggfunc= 'sum')
        
        df_power = df_run.pivot_table(index = ['match_name', 'current_innings'], values = ['runs'], aggfunc= 'max')
        
        return (df_power.reset_index()
                .rename({'match_name' : 'Match', 'current_innings' : 'Team', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
    
    
    def most_run_death_player(self):
        """The batsman with the highest run in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: Batsman name, and run
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        
        df_run = df.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values = ['runs'], aggfunc= 'sum')
        
        df_power = df_run.pivot_table(index = ['batsman1_name'], values = ['runs'], aggfunc= 'sum')
        
        return (df_power.reset_index()
                .rename({'batsman1_name' : 'Batsman', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
    
    
    def most_run_death_match_player(self):
        """The team with the highest run for a match in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: Team name, run, and match
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        
        df_run = df.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values = ['runs'], aggfunc= 'sum')
        
        df_power = df_run.pivot_table(index = ['match_name', 'batsman1_name'], values = ['runs'], aggfunc= 'sum')
        
        return (df_power.reset_index()
                .rename({'match_name': 'Match', 'batsman1_name' : 'Batsman', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Runs', ascending = False)
                )
    
    
    def most_strike_death_team(self):
        """The team with the highest strike rate in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: Team name, run, and strike rate
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        df['ball'] = 1
        
        df1 = df.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values = ['runs', 'ball'], aggfunc= 'sum').reset_index()
        
        df_power = df1.pivot_table(index = ['current_innings'], values = ['runs', 'ball'], aggfunc= 'sum').reset_index()
        
        df_power['Strk Rate'] = (df_power['runs'] / df_power['ball']*100).round(2)
        
        return (df_power
                .drop(columns = ['ball'])
                .rename({'match_name': 'Match', 'current_innings' : 'Team', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Strk Rate', ascending = False)
                )
    
    def most_strike_death_innings_team(self):
        """The team with the highest strike rate in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: Team name, run, and strike rate
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        df['ball'] = 1
        
        df1 = df.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values = ['runs', 'ball'], aggfunc= 'sum').reset_index()
        
        df_power = df1.pivot_table(index = ['match_name', 'current_innings'], values = ['runs', 'ball'], aggfunc= 'sum').reset_index()
        
        df_power['Strk Rate'] = (df_power['runs'] / df_power['ball']*100).round(2)
        
        return (df_power
                .drop(columns = ['ball'])
                .rename({'match_name': 'Match', 'current_innings' : 'Team', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Strk Rate', ascending = False)
                )
    
    
    def most_strike_death_player(self):
        """The batsman with the highest strike rate in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: batsman name, run, and strike rate
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]       
        df['ball'] = 1
        
        df1 = df.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values = ['runs', 'ball'], aggfunc= 'sum').reset_index()
        
        df_power = df1.pivot_table(index = ['batsman1_name'], values = ['runs', 'ball'], aggfunc= 'sum').reset_index()
        
        df_power['Strk Rate'] = (df_power['runs'] / df_power['ball']*100).round(2)
        
        return (df_power
                .drop(columns = ['ball'])
                .rename({'batsman1_name' : 'Batsman', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Strk Rate', ascending = False)
                )
    
    
    def most_strike_death_match_player(self):
        """The batsman with the highest strike rate for a match in T20 world cup, 2022 at death overs
        Returns:
            DataFrame: batsman name, run, match, and strike rate
        """
        
        df = self.df.copy()
        df = df[(df['over'] >= 16) & (df['over'] <= 20)]
        
        df1 = df.pivot_table(index = ['match_name', 'current_innings', 'batsman1_name'], values = ['runs', 'ball'], aggfunc= 'sum').reset_index()
        
        df_power = df1.pivot_table(index = ['match_name', 'batsman1_name'], values = ['runs', 'ball'], aggfunc= 'sum').reset_index()
        
        df_power['Strk Rate'] = (df_power['runs'] / df_power['ball']*100).round(2)
        
        return (df_power
                .drop(columns = ['ball'])
                .rename({'match_name': 'Match', 'batsman1_name' : 'Batsman', 'runs' : 'Runs'}, axis = 1)
                .sort_values(by = 'Strk Rate', ascending = False)
                )

# df = pd.read_csv("T-20 World cup 2022.csv").set_index('match_id').drop(columns = ['comment_id', 'home_team', 'away_team'])

# all = Cricket(df, 'all')
# group = Cricket(df, 'group')
# super_12 = Cricket(df, 'super 12')
# semi = Cricket(df, 'semi')
# final = Cricket(df, 'final')