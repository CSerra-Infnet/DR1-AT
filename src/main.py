import streamlit as st
from statsbombpy import sb
import pandas as pd
from matplotlib import pyplot as plt
import services as srv
import helper as hp
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Radar
import seaborn as sns
from matplotlib import colormaps

st.set_page_config(page_title="AT", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)


def Dashboard() -> None:
    """
    Main function to create the Dashboard
    """
    
    competitions = hp.initSession()
    
    with st.sidebar:
        st.write("### Selecione a Competição e Temporada")
        co1, co2 = st.columns(2)
        selCompetition = co1.selectbox("Competição", competitions.competition_id.unique(), format_func= lambda x: hp.getCompetitionName(x), key="competition_id")
        
        if selCompetition:
            competition = hp.selectCompetition(selCompetition)
            seasons = competitions[competitions["competition_id"]==selCompetition]
            st.session_state.seasons = seasons
            selSeason = co2.selectbox("Temporada", seasons['season_id'], format_func= lambda x: hp.getSeasonName(x), key="season_id")
            season = hp.selectSeason(selSeason)
            
    
    if selSeason:
        st.title(f"Análise da Temporada {season['season_name'].values[0]} - {competition['competition_name'].values[0]}")
        st.write("### Partidas")
        matches = sb.matches(competition_id=selCompetition, season_id=selSeason)
        st.session_state.matches = matches
        #st.write(st.session_state.matches)
        selMatch = st.selectbox("Selecione", matches['match_id'], format_func= lambda x: hp.getMatchName(x), key="match_id")
        #st.write(selMatch)
        
        if selMatch:
            match = matches[matches.match_id == selMatch]
            st.write("##### Placar final")  
            match_name = match['home_team'].values[0] + " " + str(match['home_score'].values[0]) + " x " + str(match['away_score'].values[0]) + " " + match['away_team'].values[0]              
            st.write("###### " + match_name)
            
            allEvents = sb.events(match_id=selMatch, split=True, flatten_attrs=False)
            matchEvents = sb.events(match_id=selMatch)
            col1, col2 , col3, col4, col5 = st.columns(5)
            col1.metric("Chutes", allEvents['shots'].shape[0])
            col2.metric("Passes", allEvents['passes'].shape[0])
            col3.metric("Faltas", allEvents['foul_committeds'].shape[0])
            col4.metric("Dribles", allEvents['dribbles'].shape[0])
            col5.metric("Bloqueios", allEvents['blocks'].shape[0])
            home_lineups = sb.lineups(match_id=selMatch)[match['home_team'].values[0]]
            away_lineups = sb.lineups(match_id=selMatch)[match['away_team'].values[0]]
            home_lineups['team']=match['home_team'].values[0]
            away_lineups['team']=match['away_team'].values[0]
            match_players = pd.concat([home_lineups, away_lineups])

            tab1, tab2, tab3, tab4 = st.tabs(["Escalação", "Eventos", "Analise por Jogador", "Mapa de Chutes"])
            with tab1:
                col1, col2 = st.columns(2)
                col1.write("### " + match['home_team'].values[0])
                col2.write("### " + match['away_team'].values[0])
                
                
                col1.write(home_lineups)
                col2.write(away_lineups)
            
            with tab2:
                filtered_events = srv.filter_dataframe(matchEvents)
                #filtered_events.reset_index(inplace=True)
                st.write(filtered_events)
                
                csv =  srv.convert_df(filtered_events)
                
                st.download_button(
                "Download Eventos CSV",
                csv,
                f'{match_name}-filtered-events.csv',
                "text/csv"
                )
        
                # selEventType = st.selectbox("Tipo", allEvents.keys())
                # if selEventType:
                #     events = sb.events(match_id=selMatch, split=True, flatten_attrs=False)[selEventType]
                #     st.write(events)
                    
            with tab3:
                selPlayer = st.selectbox("Selecione o jogador", match_players['player_id'], key="player_id", format_func= lambda x: match_players[match_players.player_id == x]['team'].values[0] + " - " + match_players[match_players.player_id == x]['player_name'].values[0])
                with st.spinner('Carregando dados...'):
                    if selPlayer:
                        player = match_players[match_players.player_id == selPlayer]
                        
                        player_passes = matchEvents[matchEvents.player_id == selPlayer][matchEvents.type == 'Pass']
                        
                        player_shots = matchEvents[matchEvents.player_id == selPlayer][matchEvents.type == 'Shot']
                        col1, col2 = st.columns(2)                        
                        #drawing pitch
                        pitch = Pitch(line_color = "black")
                        fig, ax = pitch.draw(figsize=(5, 3.5))

                        for i,thepass in player_passes.iterrows():
                            #if pass made by Lucy Bronze
                        
                            x=thepass['location'][0]
                            y=thepass['location'][1]
                            color = "red" if thepass["pass_outcome"] == "Incomplete" else "green"
                            #plot circle
                            passCircle=plt.Circle((x,y),2,color=color)
                            passCircle.set_alpha(.2)
                            ax.add_patch(passCircle)
                            dx=thepass['pass_end_location'][0]-x
                            dy=thepass['pass_end_location'][1]-y
                            #plot arrow
                            passArrow=plt.Arrow(x,y,dx,dy,width=3,color=color)
                            ax.add_patch(passArrow)

                        ax.set_title("Passes", fontsize = 8)
                        fig.set_size_inches(5, 3.5)
                        fig.legend(["Completo", "Incompleto"], ncols=2, labelcolor=['green', 'red'], loc='lower center')
                        col1.pyplot(fig)
                        
                        pitch = Pitch(line_color = "black")
                        fig, ax = pitch.draw(figsize=(5, 3.5))
                    
                        
                        for i,thepass in player_shots.iterrows():
                            #if pass made by Lucy Bronze
                        
                            x=thepass['location'][0]
                            y=thepass['location'][1]
                            #plot circle
                            color = "green" if thepass['shot_outcome'] == 'Goal' else "red" if thepass['shot_outcome'] == 'Blocked' else "blue"
                            passCircle=plt.Circle((x,y),2,color=color)
                            passCircle.set_alpha(.2)
                            ax.add_patch(passCircle)
                            dx=thepass['shot_end_location'][0]-x
                            dy=thepass['shot_end_location'][1]-y
                            #plot arrow
                            passArrow=plt.Arrow(x,y,dx,dy,width=3,color=color)
                            ax.add_patch(passArrow)

                        ax.set_title("Chutes", fontsize = 8)
                        fig.set_size_inches(5, 3.5)
                        fig.legend(["Normal", "Bloqueado", "Gol"], ncols=3, labelcolor=['blue', 'red', 'green'], loc='lower center')
                        
                        col2.pyplot(fig)                        
            
            with tab4:                
                # subset the shots
                df_shots = matchEvents[matchEvents.type == 'Shot'].copy()

                # subset the shots for each team
                team1, team2 = df_shots.team.unique()
                df_team1 = df_shots[df_shots.team == team1].copy()
                df_team2 = df_shots[df_shots.team == team2].copy()

                # Usually in football, the data is collected so the attacking direction is left to right.
                # We can shift the coordinates via: new_x_coordinate = right_side - old_x_coordinate
                # This is helpful for having one team shots on the left of the pitch and the other on the right
                df_team1["x"] = df_team1.apply(lambda row:  pitch.dim.right - row.location[0], axis=1) 
                df_team1["y"] = df_team1.apply(lambda row:   row.location[1], axis=1) 
                
                df_team2["x"] = df_team2.apply(lambda row:   row.location[0], axis=1) 
                df_team2["y"] = df_team2.apply(lambda row:   row.location[1], axis=1) 
                #df_team1["location"][0] = pitch.dim.right - df_team1.location[0]
                
                
                fig, axs = pitch.jointgrid(figheight=10, left=None, bottom=0.075, grid_height=0.8,
                    axis=False,  # turn off title/ endnote/ marginal axes
                    # plot without endnote/ title axes
                    endnote_height=0, title_height=0)
                # plot the hexbins
                hex1 = pitch.hexbin(df_team1.x, df_team1.y, ax=axs['pitch'],
                                    edgecolors=pitch.line_color, cmap='Reds')
                hex2 = pitch.hexbin(df_team2.x, df_team2.y, ax=axs['pitch'],
                                    edgecolors=pitch.line_color, cmap='Blues')
                # normalize the values so the colors depend on the minimum/ value for both teams
                # this ensures that darker colors mean more shots relative to both teams
                vmin = min(hex1.get_array().min(), hex2.get_array().min())
                vmax = max(hex1.get_array().max(), hex2.get_array().max())
                hex1.set_clim(vmin=vmin, vmax=vmax)
                hex2.set_clim(vmin=vmin, vmax=vmax)
                # plot kdeplots on the marginals
                team1_hist_y = sns.kdeplot(y=df_team1.y, ax=axs['left'], color="red", fill=True)
                team1_hist_x = sns.kdeplot(x=df_team1.x, ax=axs['top'], color="red", fill=True)
                team2_hist_x = sns.kdeplot(x=df_team2.x, ax=axs['top'], color="blue", fill=True)
                team2_hist_y = sns.kdeplot(y=df_team2.y, ax=axs['right'], color="blue", fill=True)
                txt1 = axs['pitch'].text(x=15, y=70, s=team1,  color="red",
                                        ha='center', va='center', fontsize=20)
                txt2 = axs['pitch'].text(x=105, y=70, s=team2,  color="blue",
                                        ha='center', va='center', fontsize=20)
                st.write(fig)

            #st.write(player_passes)
                     
            
           
        # st.write("### Partidas")
        # matches = sb.matches(competition_id=9, season_id=27)
        # st.write(matches)
        
        # st.write("### Escalação - Bayern Munich")
        # lineups = sb.lineups(match_id=3890505)["Bayern Munich"]
        # st.write(lineups)
        
        # st.write("### Eventos")
        # events = sb.events(match_id=3890505)
        # st.write(events)
        
        # st.write("### Eventos - Duelos")
        # events = sb.events(match_id=3890505, split=True, flatten_attrs=False)["duels"]
        # st.write(events)
        
        # events = sb.competition_events(
        #     country="Germany",
        #     division= "1. Bundesliga",
        #     season="2015/2016",
        #
    
    # st.write("### Competições")  
    # competitions = sb.competitions()
    # st.write(competitions)
    
    # st.write("### Partidas")
    # matches = sb.matches(competition_id=9, season_id=27)
    # st.write(matches)
    
    # st.write("### Escalação - Bayern Munich")
    # lineups = sb.lineups(match_id=3890505)["Bayern Munich"]
    # st.write(lineups)
    
    # st.write("### Eventos")
    # events = sb.events(match_id=3890505)
    # st.write(events)
    
    # st.write("### Eventos - Duelos")
    # events = sb.events(match_id=3890505, split=True, flatten_attrs=False)["duels"]
    # st.write(events)
    
    # events = sb.competition_events(
    #     country="Germany",
    #     division= "1. Bundesliga",
    #     season="2015/2016",
    #     gender="male"
    # )
    
    # st.write(grouped_events["events"])


    # grouped_events = sb.competition_events(
    #     country="Germany",
    #     division= "1. Bundesliga",
    #     season="2015/2016",
    #     split=True
    # )
    # st.write(grouped_events["dribbles"])
    
    # events = sb.events(match_id=3890505, include_360_metrics=True)
    # st.write(events)
    # comp_events = sb.competition_events(
    #             country="Europe",
    #             division="Champions League",
    #             season="2022/2023",
    #             include_360_metrics=True,
    # )
    # st.write(comp_events)
    
    
    # match_frames = sb.frames(match_id=3772072, fmt='dataframe')
    # comp_frames = sb.competition_frames(
    #     country="Germany",
    #     division= "1. Bundesliga",
    #     season="2015/2016"
    # )
    # st.write(match_frames)
    # st.write(comp_frames)
    
    #RAW files
    #sb.competitions(fmt="dict")
    

    
    
    if 'userPreferences' in st.session_state:
        st.markdown(
            f"""
            <style>
                * {{
                     color: {st.session_state.userPreferences['fontColor']} !important;
                }}
                [data-testid="stApp"]{{
                    background-color: {st.session_state.userPreferences['bgColor']} !important;
                }}
                [data-testid="stHeader"]{{
                    background-color: {st.session_state.userPreferences['bgColor']} !important;
                }}
                [data-testid="stSidebar"]{{
                    background-color: {st.session_state.userPreferences['sideColor']} !important;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    

    selected = None    
 
    # Menu lateral com carga de Arquivos e Seleção de Planilha
    # with st.sidebar:
    #     with st.container():            
    #         st.header("Preferências")
    #         # color picker para cor de background
    #         bgcolor = st.color_picker("Escolha a cor de fundo", '#f0f0f0')
            
    #          # color picker para cor de background
    #         sidecolor = st.color_picker("Escolha a cor do menu lateral", '#CCCCCC')
    #         # slider para escolher o tamanho da fonte
    #         fontColor = st.color_picker("Escolha a cor da fonte", '#000000')
    #         # slider para escolher o tamanho da fonte
    #         fontSize = None # fontSize = st.slider("Escolha o tamanho da fonte", 10, 50, 20)
    #         userPreferences = {'bgColor': bgcolor, 'sideColor':sidecolor, 'fontColor': fontColor, 'fontSize': fontSize}
    #         st.session_state.userPreferences = userPreferences
            
    #         if len(dataframe_dict) > 0:
    #             full_list = list(dataframe_dict.keys())
    #             full_list.append('Combinados')
    #             st.write("### Selecione a fonte de dados")
    #             selected = st.selectbox("planilha", full_list, on_change=srv.limpa_filtro)
            
    #         st.button(label="Carregar Excel", on_click=srv.upload_excel_file)
    #         st.button(label="Carregar CSV", on_click=srv.upload_csv_file)
            
            
            # csv =  convert_df(geo_data)
            
            # st.download_button(
            # "Download GeoData CSV",
            # csv,
            # f'geoData.csv',
            # "text/csv"
            # )
            
    # if dataframe_combined != None:   
        
    #     combined_continent = dataframe_combined[dataframe_combined['tipo'] ==  1]
    #     combined_countries = dataframe_combined[dataframe_combined['tipo'] == 2]
    #     combined_countries = combined_countries.drop(columns=['tipo'])
        
        
    if selected:
        # seleciona via checkbox quais colunas do dataframe serão exibidas
        
        st.header("Filtros")
        with st.expander("Selecione as colunas a serem exibidas"):
            srv.checkbox_container(dataframe_combined.columns if selected == 'Combinados' else  dataframe_dict[selected].columns)
        
        selected_columns = srv.get_selected_checkboxes()
        if not selected_columns:
            selected_columns = dataframe_combined.columns if selected == 'Combinados' else  dataframe_dict[selected].columns
            
        dataframe_show = dataframe_combined[selected_columns] if selected == 'Combinados' else dataframe_dict[selected][selected_columns]
        # if selected_columns:
        #     dataframe_show = dataframe_show[[col for col in dataframe_show.columns if col in selected_columns]]
        filtered_df = srv.filter_dataframe(dataframe_show)
        filtered_df.reset_index(inplace=True)
        st.write(filtered_df)
        
        csv =  srv.convert_df(filtered_df)
        
        st.download_button(
        "Download CSV",
        csv,
        f'{selected}.csv',
        "text/csv"
        )
        
        all_continents = filtered_df[filtered_df['tipo']==1]
        continents_list = all_continents['local'].unique()
        all_countries = filtered_df[filtered_df['tipo']==2]
        #countries_list = all_countries['local'].unique()
      
        countries = all_countries.melt(id_vars=['local'], value_vars=selected_columns, var_name='Ano_Mes', value_name='Valor')
        # CONVERTE A COLUNA ANO_MES PARA DATETIME E REMOVE O QUE NÃO CONSEGUIR CONVERTER (TOTAL)
        countries['Ano_Mes'] = countries['Ano_Mes'].apply(srv.convert_to_datetime)
        countries = countries[countries['Ano_Mes'].notna()]
        countries = countries.set_index(['local','Ano_Mes'])
        totals = countries.groupby(level='local').sum()
        totals.sort_values(by='Valor', ascending=False, inplace=True)
        
        # Une aos dados de localização
        localized_countries = pd.DataFrame(totals).merge(geo_data, left_on='local', right_on='name')
        localized_countries.drop(columns=['country'], inplace=True)
        
        continents = all_continents.melt(id_vars=['local'], value_vars=selected_columns, var_name='Ano_Mes', value_name='Valor')
        continents = continents.set_index(['local','Ano_Mes'])
        continents =  continents.groupby(level='local').sum()
        continents.sort_values(by='Valor', ascending=False, inplace=True)
        
        
        # metricas gerais
        st.write("# Métricas Gerais")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        total_value = continents.sum()['Valor'].astype(int)
        first_continent = continents.iloc[0]['Valor'].astype(int)
        first_country = totals.iloc[0]['Valor'].astype(int)
        mean_continent = continents.mean()['Valor'].astype(int)
        mean_month = countries.groupby(level="Ano_Mes").sum().mean()[0].astype(int)
        mean_country = totals.mean()['Valor'].astype(int)

       
        col1.metric("Total de Viagens - " + selected, f'{total_value:,}'.replace(',','.'))
        col2.metric(f"Continente nº1 - {continents.index[0]}", f'{first_continent:,}'.replace(',','.') )
        col3.metric(f"País nº1 - {totals.index[0]}", f'{first_country:,}'.replace(',','.') )
        col4.metric("Média por Continentes", f'{mean_continent:,}'.replace(',','.') )
        col5.metric("Média por Mês", f'{mean_month:,}'.replace(',','.') )
        col6.metric("Média por País", f'{mean_country:,}'.replace(',','.') )

        
        st.write("# Mapa de Viagens por País")
        st.map(localized_countries, size='Valor', zoom=1)
        #st.write(localized_countries)
        
        selected_continent = st.selectbox("Selecione o Continente", continents_list)
        if selected_continent:
            #PREPARA DADOS PARA VISUALIZAÇÃO
            # filtra countries do continente selecionadp
            countries = all_countries[all_countries['continente']==selected_continent]
            # reestrutura o dataframe verticalizando os dados
            countries = countries.melt(id_vars=['local'], value_vars=selected_columns, var_name='Ano_Mes', value_name='Valor')
            #st.write(countries)

            # CONVERTE A COLUNA ANO_MES PARA DATETIME E REMOVE O QUE NÃO CONSEGUIR CONVERTER (TOTAL)
            countries['Ano_Mes'] = countries['Ano_Mes'].apply(srv.convert_to_datetime)
            countries = countries[countries['Ano_Mes'].notna()]
            countries = countries.set_index(['local','Ano_Mes'])
            
            # Obtem os totais por pais
            totals = countries.groupby(level='local').sum()
            # Obtem os totalizados por paises e gera gráfico de pizza
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            totals.plot.pie(y='Valor', ax=ax1,  title=f'Total de Viagens por País - {selected_continent}')
            time_totals = countries.groupby(level='Ano_Mes').sum()
            time_totals.plot(kind="area", ax=ax2, title=f'Total de Viagens por Mês - {selected_continent}', xlabel='', ylabel='')
            st.write(fig)
            
            for (cat1, subdf) in countries.groupby(level='local'):
               
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
                # não ta funcionando, pq?
                ax1.set_xticklabels([pandas_datetime.strftime("%m/%Y") for pandas_datetime in subdf.loc[cat1, :].index])
                ax2.set_xticklabels([pandas_datetime.strftime("%m/%Y") for pandas_datetime in subdf.loc[cat1, :].index])
                
                subdf.loc[cat1, :].plot(kind='bar', y='Valor', ax=ax1, rot=45, xlabel='', legend=False)
                subdf.loc[cat1, :].plot(kind='hist', y='Valor', ax=ax2, rot=45, xlabel='', legend=False)
                fig.suptitle(f'Viagens por Mês - {cat1}')
                fig.tight_layout()
                #plt.show()
                st.write(fig)
                #subdf.loc[cat1, :].plot.pie(y='Valor', ax=ax1, ylabel='', legend=False)
          
       
        
    
    
if __name__ == "__main__":
    Dashboard()


 