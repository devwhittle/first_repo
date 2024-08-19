import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_team_stats(year):
    url = f"https://www.baseball-reference.com/leagues/MLB/{year}.shtml"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the pitching and batting tables
    try:
        pitching_table = soup.find('table', {'id': 'all_teams_standard_pitching'})
        batting_table = soup.find('table', {'id': 'all_teams_standard_batting'})

        if pitching_table is None or batting_table is None:
            raise ValueError("Unable to find the necessary tables on the page.")

        # Convert tables into pandas DataFrames
        pitching_df = pd.read_html(str(pitching_table))[0]
        batting_df = pd.read_html(str(batting_table))[0]

        # Clean up the DataFrames
        pitching_df.columns = pitching_df.columns.droplevel(0)
        batting_df.columns = batting_df.columns.droplevel(0)

        # Keep relevant columns
        pitching_df = pitching_df[['Tm', 'W', 'L', 'ERA', 'FIP', 'IP', 'SO', 'H', 'ER', 'BB', 'HR']]
        batting_df = batting_df[['Tm', 'R', 'H', '2B', '3B', 'HR', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS']]

        # Merge DataFrames on team name
        team_stats_df = pd.merge(pitching_df, batting_df, on='Tm')

        return team_stats_df

    except ValueError as e:
        print(f"Error: {e}")
        return None

# Example: Fetch data for 2023
team_stats_2023 = fetch_team_stats(2023)

if team_stats_2023 is not None:
    print(team_stats_2023.head())
else:
    print("Failed to fetch the data.")