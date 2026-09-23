import streamlit as st
import pandas as pd

if 'search_results' not in st.session_state:
        st.session_state.search_results = None

st.title("FC 26 Player Finder")

df = pd.read_csv(r"FC26_20250921.csv")
st.write(f'Players in Database: {len(df)} Players')

df['player_positions_list'] = df['player_positions'].str.split(', ')

positions = sorted(set(position for positions in df['player_positions_list'] for position in positions))
position = st.multiselect("Position", positions, placeholder= 'Choose Position(s)')

overall_col, potential_col = st.columns(2)
with overall_col:
    overall = st.slider('Overall Range', value = (47,91), min_value = 47, max_value = 91)
with potential_col:
    potential = st.slider('Potential Range', value = (49,95), min_value = 49, max_value = 95)

age = st.slider('Age Range', value = (16,44), min_value=16, max_value=44)

league_col, club_col = st.columns(2)
with league_col:
    leagues = sorted(df['league_name'].dropna().unique().tolist())
    leagues.insert(0, 'Any League')
    league = st.selectbox('League', leagues)
with club_col:
    if league == 'Any League':
        clubs = sorted(df['club_name'].dropna().unique().tolist())
    else:
        clubs = sorted(df.loc[df['league_name'] == league, 'club_name'].dropna().unique().tolist())
    clubs.insert(0, 'Any Club')
    club = st.selectbox('Club', clubs)

nationalities = sorted(df['nationality_name'].dropna().unique().tolist())
nationalities.insert(0, 'Any Nationality')
nationality = st.selectbox('Nationality', nationalities)


height = st.slider('Height Range (Cm)', value = (155,210), min_value=155, max_value=210)

min_col, max_col = st.columns(2)
with min_col:
    min_value = st.number_input('Minimum Value (Million Euros)', value = None, placeholder='Enter Minimum Value')
with max_col:
    max_value = st.number_input('Maximum Value (Million Euros)', value = None, placeholder='Enter Maximum Value')

wf_col, sm_col = st.columns(2)
with wf_col:
    weak_foot = st.slider('Weak Foot', value = (1,5), min_value=1, max_value=5)
with sm_col:
    skill_moves = st.slider('Skill Moves', value = (1,5), min_value=1, max_value=5)


if st.button('Search', use_container_width=True):
    filtered = df.copy()
    
    if position != []:
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

    if height[0] is not None:
        filtered = filtered[filtered['height_cm'] >= height[0]]
    if height[1] is not None:
        filtered = filtered[filtered['height_cm'] <= height[1]]

    if weak_foot[0] is not None:
        filtered = filtered[filtered['weak_foot'] >= weak_foot[0]]
    if weak_foot[1] is not None:
        filtered = filtered[filtered['weak_foot'] <= weak_foot[1]]

    if skill_moves[0] is not None:
        filtered = filtered[filtered['skill_moves'] >= skill_moves[0]]
    if skill_moves[1] is not None:
        filtered = filtered[filtered['skill_moves'] <= skill_moves[1]]

    if age[0] is not None:
        filtered = filtered[filtered['age'] >= age[0]]
    if age[1] is not None:
        filtered = filtered[filtered['age'] <= age[1]]

    if overall[0] is not None:
        filtered = filtered[filtered['overall'] >= overall[0]]
    if overall[1] is not None:
        filtered = filtered[filtered['overall'] <= overall[1]]

    if potential[0] is not None:
        filtered = filtered[filtered['potential'] >= potential[0]]
    if potential[1] is not None:
        filtered = filtered[filtered['potential'] <= potential[1]]

    st.session_state.search_results = filtered

if st.session_state.search_results is not None:
    filtered = st.session_state.search_results
    st.write(f'Found {len(filtered)} Players')
    renamed_filtered  = filtered.rename(columns={'short_name': 'Player', 'age': 'Age', 'player_positions': 'Position(s)', 'overall': 'Overall', 'potential': 'Potential', 'club_name': 'Club', 'nationality_name': 'Country', 'value_eur': 'Value (€)'})

    st.dataframe(renamed_filtered[['Player', 'Age', 'Position(s)', 'Overall', 'Potential', 'Club', 'Country', 'Value (€)']], column_config= {'Value (€)': st.column_config.NumberColumn('Value (€)', format='€%,d')} , hide_index = True)