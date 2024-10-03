import streamlit as st
import services as srv

def initSession():
    if 'competitions' not in st.session_state:
        st.session_state.competitions = srv.load_competitions()
    if 'selected_competition' not in st.session_state:
        st.session_state.selected_competition = None
    if 'selected_season' not in st.session_state:
        st.session_state.selected_season = None
    if 'selected_match' not in st.session_state:
        st.session_state.selected_match = None
    if 'selected_player' not in st.session_state:
        st.session_state.selected_player = None
        
    return st.session_state.competitions

def getCompetitionName(competition_id: int) -> str:
    """
    Get the name of the competition based on the competition_id
    """
    competition = st.session_state.competitions[st.session_state.competitions.competition_id == competition_id]
    #print(competition)
    return competition['competition_name'].values[0]

def selectCompetition(competition_id):
    """
    Select the competition based on the competition_id
    """
    #print(competition_id)
    competition = st.session_state.competitions[st.session_state.competitions.competition_id == competition_id]
    st.session_state.selected_competition = competition[['competition_id', 'competition_name']].drop_duplicates()
    return st.session_state.selected_competition

def getSeasonName(season_id: int) -> str:
    """
    Get the name of the competition based on the competition_id
    """
    competition = st.session_state.competitions[st.session_state.competitions.season_id == season_id]
    #print(competition)
    return competition['season_name'].values[0]

def selectSeason(season_id: int):
    """
    Select the competition based on the competition_id
    """
    #print(competition_id)
    season = st.session_state.competitions[st.session_state.competitions.season_id == season_id]
    st.session_state.selected_season = season[['season_id', 'season_name']].drop_duplicates()
    return st.session_state.selected_season

def getMatchName(match_id: int) -> str:
    """
    Get the name of the competition based on the competition_id
    """
    match = st.session_state.matches[st.session_state.matches.match_id == match_id]
    #st.write(match)
    return  match['home_team'].values[0] + " x " + match['away_team'].values[0] + " - " + match['match_date'].values[0]

def selectMatch(match_id: int) -> None:
    """
    Select the competition based on the competition_id
    """
    #print(competition_id)
    match = st.session_state.matches[st.session_state.matches.match_id == match_id]
    st.session_state.selected_season = match.drop_duplicates()
