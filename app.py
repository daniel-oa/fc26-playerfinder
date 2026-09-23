import streamlit as st
import pandas as pd

if 'search_results' not in st.session_state:
    st.session_state.search_results = None

def reset_filters():
    st.session_state.player_name = ''
    st.session_state.position = []
    st.session_state.overall = (47, 91)
    st.session_state.potential = (49, 95)
    st.session_state.age = (16, 44)
    st.session_state.league = 'Any League'
    st.session_state.club = 'Any Club'
    st.session_state.nationality = 'Any Nationality'
    st.session_state.height = (155, 210)
    st.session_state.min_value = None
    st.session_state.max_value = None
    st.session_state.weak_foot = (1, 5)
    st.session_state.skill_moves = (1, 5)
    st.session_state.search_results = None

st.title("FC 26 Player Finder")

@st.cache_data
def load_data():
    return pd.read_csv("FC26_20250921.csv", low_memory = False)
df = load_data()

st.write(f'Players in Database: {len(df)} Players')

player_name = st.text_input('Player Name', placeholder = 'Search by player name', key = 'player_name')

df['player_positions_list'] = df['player_positions'].str.split(', ')
positions = sorted(set(pos for player_positions in df['player_positions_list'] for pos in player_positions))
position = st.multiselect("Position", positions, placeholder = 'Choose Position(s)', key = 'position')

overall_col, potential_col = st.columns(2)
with overall_col:
    overall = st.slider('Overall Range', min_value = 47, max_value = 91, key = 'overall')
with potential_col:
    potential = st.slider('Potential Range', min_value = 49, max_value = 95, key = 'potential')

age = st.slider('Age Range', min_value=16, max_value=44, key = 'age')

league_col, club_col = st.columns(2)
with league_col:
    leagues = sorted(df['league_name'].dropna().unique().tolist())
    leagues.insert(0, 'Any League')
    league = st.selectbox('League', leagues, key = 'league')
with club_col:
    if league == 'Any League':
        clubs = sorted(df['club_name'].dropna().unique().tolist())
    else:
        clubs = sorted(df.loc[df['league_name'] == league, 'club_name'].dropna().unique().tolist())
    clubs.insert(0, 'Any Club')
    club = st.selectbox('Club', clubs, key = 'club')

nationalities = sorted(df['nationality_name'].dropna().unique().tolist())
nationalities.insert(0, 'Any Nationality')
nationality = st.selectbox('Nationality', nationalities, key = 'nationality')


height = st.slider('Height Range (Cm)', min_value = 155, max_value = 210, key = 'height')

min_col, max_col = st.columns(2)
with min_col:
    min_value = st.number_input('Minimum Value (Million Euros)', value = None, placeholder = 'Enter Minimum Value', key = 'min_value')
with max_col:
    max_value = st.number_input('Maximum Value (Million Euros)', value = None, placeholder = 'Enter Maximum Value', key = 'max_value')

wf_col, sm_col = st.columns(2)
with wf_col:
    weak_foot = st.slider('Weak Foot', min_value = 1, max_value = 5, key = 'weak_foot')
with sm_col:
    skill_moves = st.slider('Skill Moves', min_value = 1, max_value = 5, key = 'skill_moves')

search_col, reset_col = st.columns(2)
with search_col:
    search_clicked = st.button('Search', use_container_width = True)
with reset_col:
    st.button('Reset Filters', use_container_width = True, on_click = reset_filters)

if search_clicked:
    filtered = df.copy()

    if player_name:
        name_search = player_name.strip().lower()
        filtered = filtered[filtered['short_name'].str.lower().str.contains(name_search, na = False) |
                            filtered['long_name'].str.lower().str.contains(name_search, na = False)]
    if position:
        filtered = filtered[filtered['player_positions_list'].apply(lambda x: any(pos in x for pos in position))]

    if league != 'Any League':
        filtered = filtered[filtered['league_name'] == league]

    if club != 'Any Club':
        filtered = filtered[filtered['club_name'] == club]

    if nationality != 'Any Nationality':
        filtered = filtered[filtered['nationality_name'] == nationality]

    if min_value is not None:
        filtered = filtered[filtered['value_eur'] >= (min_value*1000000)]
    if max_value is not None:
        filtered = filtered[filtered['value_eur'] <= (max_value*1000000)]

    filtered = filtered[filtered['height_cm'] >= height[0]]
    filtered = filtered[filtered['height_cm'] <= height[1]]

    filtered = filtered[filtered['weak_foot'] >= weak_foot[0]]
    filtered = filtered[filtered['weak_foot'] <= weak_foot[1]]

    filtered = filtered[filtered['skill_moves'] >= skill_moves[0]]
    filtered = filtered[filtered['skill_moves'] <= skill_moves[1]]

    filtered = filtered[filtered['age'] >= age[0]]
    filtered = filtered[filtered['age'] <= age[1]]

    filtered = filtered[filtered['overall'] >= overall[0]]
    filtered = filtered[filtered['overall'] <= overall[1]]

    filtered = filtered[filtered['potential'] >= potential[0]]
    filtered = filtered[filtered['potential'] <= potential[1]]

    st.session_state.search_results = filtered


if st.session_state.search_results is not None:
    filtered = st.session_state.search_results
    st.write(f'Found {len(filtered)} Players')
    renamed_filtered  = filtered.rename(columns={'short_name': 'Player', 'age': 'Age', 'player_positions': 'Position(s)', 'overall': 'Overall', 'potential': 'Potential', 'club_name': 'Club', 'nationality_name': 'Country', 'value_eur': 'Value (€)'})
    renamed_filtered['Value (€)'] = renamed_filtered['Value (€)'].replace(0, pd.NA).astype('Int64')

    if len(filtered) == 0:
        st.info('No players match your filters.')
    else:
        st.dataframe(renamed_filtered[['Player', 'Age', 'Position(s)', 'Overall', 'Potential', 'Club', 'Country', 'Value (€)']], column_config = {'Value (€)': st.column_config.NumberColumn('Value (€)', format='€%,d')} , hide_index = True)