import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
import datetime
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components


# option
st.set_page_config(page_title="Dasboard des indicateurs - Janvier 2022",
                   page_icon="https://pbs.twimg.com/profile_images/1321098074765361153/F4UFTeix.png",
                   initial_sidebar_state="expanded",
                   layout="wide",)


#############
## sidebar ##
############# 
st.sidebar.image("https://soliguide.fr/assets/images/logo.png", use_column_width=True)
st.sidebar.title('Indicateurs 2022')
st.sidebar.subheader('Janvier 2022')


categorie = st.sidebar.selectbox("Choisissez votre territoire :", ("France",
                                            "Région SUD", 
                                            "- Alpes-Maritimes (06)", "- Bouche-du-Rhône (13)", 
                                            "Auvergne-Rhône-Alpes",
                                            "- Ardèche (07)", "- Cantal (15)", "- Puy-de-Dôme (63)",
                                            'Occitanie',
                                            "- Hérault (34)",
                                            "Nouvelle-Aquitaine",
                                            "- Gironde (33)", "- Charente (16)", "- Haute-Vienne (87)", "- Dordogne (24)",
                                            "Centre-Val-de-Loire",
                                            "- Indre (36)", 
                                            "Pays-de-la-Loire",
                                            "- Loire-Atlantique (44)", 
                                            "Normandie",
                                            "- Seine-Maritime (76)",
                                            "Ile-de-France",
                                            "- Paris (75)", "- Seine-et-Marne (77)",
                                            "- Yvelines (78)","- Essonne (91)", "- Hauts-de-Seine (92)",
                                            "- Seine-Saint-Denis (93)","- Val-de-Marne (94)", "- Val-d'Oise (95)",
                                            "Hauts-de-France",
                                            "- Nord (59)",
                                            "Grand-Est",
                                            "- Bas-Rhin (67)",
                                            "Bourgogne-Franche-Comté",
                                            "- Côte-d'Or (21)"))

categorie_2 = st.sidebar.radio("Cercles", ("Tous","Ile-de-France", "Lancement",'Pérennisation',
                                            "Communication", 'Admin/Finance',
                                            ))


##########
## DATA ##
##########

# modifier selon la localisation de la BD
df_users_pro_roles = pd.read_csv('./ressource/df_users_pro_roles.csv')
df_users_pro_roles_test = pd.read_csv('./ressource/df_users_pro_roles_test.csv')
df_orga_ceated = pd.read_csv('./ressource/df_orga_ceated.csv')
df_orga_2 = pd.read_csv('./ressource/df_orga_2.csv')
df_orga_3 = pd.read_csv('./ressource/df_orga_3.csv')
df_orga_auto = df_orga_3.copy()
df_history_data = pd.read_csv('./ressource/df_history_data.csv')

s = pd.read_csv("./ressource/searchWithDatePresentation3.csv")
s = s.iloc[:-1,:]

df_search_users = pd.read_csv("./ressource/df_search_users.csv")

df_relais = pd.read_csv('./ressource/Organisme-allDep pas locked.csv')
df_relais_clean = df_relais[['Territoire Rollup','Relation']].dropna(subset=['Territoire Rollup'])

df_users_API = pd.read_csv("./ressource/df_users_API.csv")
df_users_API_vf = pd.DataFrame(df_users_API.value_counts()).reset_index()
df_users_API_vf = df_users_API_vf[df_users_API_vf.status.str.contains('API')].reset_index()
df_users_API_vf.drop(columns='Unnamed: 0', inplace=True)

df4 = pd.read_csv("./ressource/GAdata.csv")

df_diff = pd.read_csv('./ressource/Diffusion-allDep.csv')
df_diff = df_diff[['Date','Territoire','Nb de pros','Nb de bénéficiaires']]
df_diff = df_diff.fillna(0)


today = date.today()
lastMonth = today - pd.Timedelta(days=183)



cat_dict = {"France":'Total', "- Alpes-Maritimes (06)" :"06", "- Ardèche (07)":"07",
            "- Bouche-du-Rhône (13)": "13","- Cantal (15)":"15","- Charente (16)":"16","- Côte-d'Or (21)" : "21", "- Dordogne (24)":"24","- Gironde (33)":"33","- Hérault (34)":"34","- Indre (36)":"36",
            "- Loire-Atlantique (44)" : "44","- Nord (59)":"59" , "- Puy-de-Dôme (63)":"63","- Haute-Vienne (87)":"87",
            "- Bas-Rhin (67)":"67", "- Paris (75)" : "75", "- Seine-Maritime (76)":"76",
            "- Seine-et-Marne (77)":'77', "- Yvelines (78)":"78", "- Essonne (91)" :"91", 
            "- Hauts-de-Seine (92)":"92","- Seine-Saint-Denis (93)": "93","- Val-de-Marne (94)": "94", 
            "- Val-d'Oise (95)":"95"}

            
##########
## Tous ##
##########

if categorie_2 == 'Tous':


    ## Compte pro invité et validé ##

    if categorie == "France":
        df_users_pro_roles = df_users_pro_roles
        df_users_pro_roles_test = df_users_pro_roles_test
        df_orga_ceated = df_orga_ceated
        df_orga_2 = df_orga_2
        df_orga_auto = df_orga_auto
        df_history_data = df_history_data
        s1 = s.filter(regex='général')
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)

        s1_cum = s1[['datePresentation','Recherches général']]
        s1_cum['Recherches général cumulé'] = s1_cum['Recherches général'].cumsum()

        df_search_users = df_search_users

        df_relais_clean = df_relais_clean

        df4 = df4.groupby('Unnamed: 0').sum().reset_index()

        df_diff = df_diff




    elif categorie == "Région SUD":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "06") | (df_users_pro_roles.territories == "13")].dropna()
        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 6) | (df_users_pro_roles_test.territory == 13)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "06") | (df_orga_ceated.territories == "13")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 6) | (df_orga_2.territory == 13)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 6) | (df_orga_auto.territory == 13)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire== 6) | (df_history_data.territoire == 13)].dropna()

        s1 = pd.concat([s.filter(regex="06"), s.filter(regex="13")], axis=0)
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        s1 = s1.groupby(s1['datePresentation']).sum()
        s1 = s1.T
        s1.index = s1.iloc[:, :].index.str[:-8].tolist()
        s1 = s1.groupby(s1.index).sum()
        s1 = s1.T.reset_index()
        s1.replace({0:np.nan}, inplace=True)

        s1_cum = s1[['datePresentation','Recherches']]
        s1_cum['Recherches cumulé'] = s1_cum['Recherches'].cumsum()

        df_search_users = df_search_users[(df_search_users.Territoire == 6) | (df_search_users.Territoire == 13)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('06')) | (df_relais_clean['Territoire Rollup'].str.contains('13'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "06") | (df_users_API['territories'] == "13")]

        df4 = df4[(df4['territoire'].str.contains("06")) | (df4['territoire'].str.contains("13"))]
        df4 = df4.groupby('Unnamed: 0').sum().reset_index()

        df_diff = df_diff[(df_diff.Territoire.str.contains('06')) | (df_diff.Territoire.str.contains('13'))]



    elif categorie == "Auvergne-Rhône-Alpes":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "07") | (df_users_pro_roles.territories == "15") | (df_users_pro_roles.territories == "63")].dropna()
        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 7) | (df_users_pro_roles_test.territory == 15) | (df_users_pro_roles_test.territory == 63)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "07") | (df_orga_ceated.territories == "15") | (df_orga_ceated.territories == "63")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 7) | (df_orga_2.territory == 15) | (df_orga_2.territory == 63)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 7) | (df_orga_auto.territory == 15) | (df_orga_auto.territory == 63)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 7) | (df_history_data.territoire == 15) | (df_history_data.territoire == 63)].dropna()

        s1 = pd.concat([s.filter(regex="07"), s.filter(regex="15"), s.filter(regex="63")], axis=0)
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        s1 = s1.groupby(s1['datePresentation']).sum()
        s1 = s1.T
        s1.index = s1.iloc[:, :].index.str[:-8].tolist()
        s1 = s1.groupby(s1.index).sum()
        s1 = s1.T.reset_index()
        s1.replace({0:np.nan}, inplace=True)

        s1_cum = s1[['datePresentation','Recherches']]
        s1_cum['Recherches cumulé'] = s1_cum['Recherches'].cumsum()

        df_search_users = df_search_users[(df_search_users.Territoire == 7) | (df_search_users.Territoire == 15) | (df_search_users.Territoire == 63)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('07')) | (df_relais_clean['Territoire Rollup'].str.contains('15'))
        | (df_relais_clean['Territoire Rollup'].str.contains('63'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "07") | (df_users_API['territories'] == "15") | (df_users_API['territories'] == "63")]

        df4 = df4[(df4['territoire'].str.contains("07")) | (df4['territoire'].str.contains("15")) | (df4['territoire'].str.contains("63"))]
        df4 = df4.groupby('Unnamed: 0').sum().reset_index()

        df_diff = df_diff[(df_diff.Territoire.str.contains('07')) | (df_diff.Territoire.str.contains('15')) | (df_diff.Territoire.str.contains('63'))]

    elif categorie == "Occitanie":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "34")].dropna()
        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 34)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "34")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 34)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 34)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 34)].dropna()

        s1 = s.filter(regex="34")
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        #s1.replace({np.nan:0}, inplace=True)
        df1 = s1.iloc[:, 1:]

        df_search_users = df_search_users[(df_search_users.Territoire == 34)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('34'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "34")]

        df4 = df4[(df4['territoire'].str.contains("34"))]

        df_diff = df_diff[(df_diff.Territoire.str.contains('34', na=False))]


    elif categorie == "Nouvelle-Aquitaine":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "33") | (df_users_pro_roles.territories == "87") | (df_users_pro_roles.territories == "16") | 
        (df_users_pro_roles.territories == "24")].dropna()

        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 33) | (df_users_pro_roles_test.territory == 87) | (df_users_pro_roles_test.territory == 16) | (df_users_pro_roles_test.territory == 24)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "33") | (df_orga_ceated.territories == "87") | (df_orga_ceated.territories == "16") | (df_orga_ceated.territories == "24")].dropna()

        df_orga_2 = df_orga_2[(df_orga_2.territory == 33) | (df_orga_2.territory == 87) | (df_orga_2.territory == 16) | (df_orga_2.territory == 24)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 33) | (df_orga_auto.territory == 87) | (df_orga_auto.territory == 16) | (df_orga_auto.territory == 24)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 33) | (df_history_data.territoire == 87) | (df_history_data.territoire == 16) | (df_history_data.territoire == 24)].dropna()

        s1 = pd.concat([s.filter(regex="33"), s.filter(regex="87"), s.filter(regex="16"), s.filter(regex="24")], axis=0)
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        s1 = s1.groupby(s1['datePresentation']).sum()
        s1 = s1.T
        s1.index = s1.iloc[:, :].index.str[:-8].tolist()
        s1 = s1.groupby(s1.index).sum()
        s1 = s1.T.reset_index()
        s1.replace({0:np.nan}, inplace=True)

        s1_cum = s1[['datePresentation','Recherches']]
        s1_cum['Recherches cumulé'] = s1_cum['Recherches'].cumsum()

        df_search_users = df_search_users[(df_search_users.Territoire == 33) | (df_search_users.Territoire == 87) | (df_search_users.Territoire == 16) | (df_search_users.Territoire == 24)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('33')) | (df_relais_clean['Territoire Rollup'].str.contains('87'))
        | (df_relais_clean['Territoire Rollup'].str.contains('16')) | (df_relais_clean['Territoire Rollup'].str.contains('24'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "33") | (df_users_API['territories'] == "87") | (df_users_API['territories'] == "16")
        | (df_users_API['territories'] == "24")]

        df4 = df4[(df4['territoire'].str.contains("33")) | (df4['territoire'].str.contains("87")) | (df4['territoire'].str.contains("16")) | (df4['territoire'].str.contains("24"))]
        df4 = df4.groupby('Unnamed: 0').sum().reset_index()

        df_diff = df_diff[(df_diff.Territoire.str.contains('33')) | (df_diff.Territoire.str.contains('87')) | (df_diff.Territoire.str.contains('16'))| (df_diff.Territoire.str.contains('24'))]


    elif categorie == "Centre-Val-de-Loire":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "36")].dropna()

        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 36)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "36")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 36)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 36)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 36)].dropna()

        s1 = s.filter(regex="34")
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        #s1.replace({np.nan:0}, inplace=True)
        df1 = s1.iloc[:, 1:]

        df_search_users = df_search_users[(df_search_users.Territoire == 36)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('36'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "36")]

        df4 = df4[(df4['territoire'].str.contains("36"))]

        df_diff = df_diff[(df_diff.Territoire.str.contains('36', na=False))]

    elif categorie == "Pays-de-la-Loire":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "44")].dropna()

        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 44)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "44")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 44)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 44)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 44)].dropna()

        s1 = s.filter(regex="44")
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        #s1.replace({np.nan:0}, inplace=True)
        df1 = s1.iloc[:, 1:]

        df_search_users = df_search_users[(df_search_users.Territoire == 44)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('44'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "44")]

        df4 = df4[(df4['territoire'].str.contains("44"))]

        df_diff = df_diff[(df_diff.Territoire.str.contains('44', na=False))]

    elif categorie == "Normandie":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "76")].dropna()

        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 76)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "76")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 76)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 76)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 76)].dropna()

        s1 = s.filter(regex="76")
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        #s1.replace({np.nan:0}, inplace=True)
        df1 = s1.iloc[:, 1:]

        df_search_users = df_search_users[(df_search_users.Territoire == 76)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('76'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "76")]

        df4 = df4[(df4['territoire'].str.contains("76"))]

        df_diff = df_diff[(df_diff.Territoire.str.contains('76', na=False))]

    elif categorie == "Ile-de-France":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "75") | (df_users_pro_roles.territories == "77") | (df_users_pro_roles.territories == "78")
        | (df_users_pro_roles.territories == "91")| (df_users_pro_roles.territories == "92")| (df_users_pro_roles.territories == "93")| (df_users_pro_roles.territories == "94")
        | (df_users_pro_roles.territories == "95")].dropna()

        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 75) | (df_users_pro_roles_test.territory == 77) | (df_users_pro_roles_test.territory == 78)
        | (df_users_pro_roles_test.territory == 91)| (df_users_pro_roles_test.territory == 92)| (df_users_pro_roles_test.territory == 93)| (df_users_pro_roles_test.territory == 94)
        | (df_users_pro_roles_test.territory == 95)].dropna()

        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "75") | (df_orga_ceated.territories == "77") | (df_orga_ceated.territories == "78") | (df_orga_ceated.territories == "91")
        | (df_orga_ceated.territories == "92") |(df_orga_ceated.territories == "93") | (df_orga_ceated.territories == "94") | (df_orga_ceated.territories == "95")].dropna()

        df_orga_2 = df_orga_2[(df_orga_2.territory == 75) | (df_orga_2.territory == 77) | (df_orga_2.territory == 78) | (df_orga_2.territory == 91)
        | (df_orga_2.territory == 92) |(df_orga_2.territory == 93) | (df_orga_2.territory == 94) | (df_orga_2.territory == 95)].dropna()

        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 75) | (df_orga_auto.territory == 77) | (df_orga_auto.territory == 78) | (df_orga_auto.territory == 91)
        | (df_orga_auto.territory == 92) |(df_orga_auto.territory == 93) | (df_orga_auto.territory == 94) | (df_orga_auto.territory == 95)].dropna()

        df_history_data = df_history_data[(df_history_data.territoire == 75) | (df_history_data.territoire == 77) | (df_history_data.territoire == 78) | (df_history_data.territoire == 91)
        | (df_history_data.territoire == 92) |(df_history_data.territoire == 93) | (df_history_data.territoire == 94) | (df_history_data.territoire == 95)].dropna()

        s1 = pd.concat([s.filter(regex="75"), s.filter(regex="77"), s.filter(regex="78"), s.filter(regex="91"), s.filter(regex="92"), s.filter(regex="93"), s.filter(regex="94"), s.filter(regex="95")], axis=0)
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        s1 = s1.groupby(s1['datePresentation']).sum()
        s1 = s1.T
        s1.index = s1.iloc[:, :].index.str[:-8].tolist()
        s1 = s1.groupby(s1.index).sum()
        s1 = s1.T.reset_index()
        s1.replace({0:np.nan}, inplace=True)

        s1_cum = s1[['datePresentation','Recherches']]
        s1_cum['Recherches cumulé'] = s1_cum['Recherches'].cumsum()

        df_search_users = df_search_users[(df_search_users.Territoire == 75) | (df_search_users.Territoire == 77) | (df_search_users.Territoire == 78) | (df_search_users.Territoire == 91)
        | (df_search_users.Territoire == 92) | (df_search_users.Territoire == 93) | (df_search_users.Territoire == 93) | (df_search_users.Territoire == 95)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('75')) | (df_relais_clean['Territoire Rollup'].str.contains('77'))
        | (df_relais_clean['Territoire Rollup'].str.contains('78')) | (df_relais_clean['Territoire Rollup'].str.contains('91')) | (df_relais_clean['Territoire Rollup'].str.contains('92'))
        | (df_relais_clean['Territoire Rollup'].str.contains('93'))| (df_relais_clean['Territoire Rollup'].str.contains('94'))| (df_relais_clean['Territoire Rollup'].str.contains('95'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "75") | (df_users_API['territories'] == "77") | (df_users_API['territories'] == "78")
        | (df_users_API['territories'] == "91") | (df_users_API['territories'] == "92") | (df_users_API['territories'] == "93") | (df_users_API['territories'] == "94")
        | (df_users_API['territories'] == "95")]

        df4 = df4[(df4['territoire'].str.contains("75")) | (df4['territoire'].str.contains("77")) | (df4['territoire'].str.contains("78")) | (df4['territoire'].str.contains("91"))
        | (df4['territoire'].str.contains("92")) | (df4['territoire'].str.contains("93")) | (df4['territoire'].str.contains("94")) | (df4['territoire'].str.contains("95"))]
        df4 = df4.groupby('Unnamed: 0').sum().reset_index()

        df_diff = df_diff[(df_diff.Territoire.str.contains('75')) | (df_diff.Territoire.str.contains('77')) | (df_diff.Territoire.str.contains('78'))
        | (df_diff.Territoire.str.contains('91')) | (df_diff.Territoire.str.contains('92')) | (df_diff.Territoire.str.contains('93')) | (df_diff.Territoire.str.contains('94'))
        | (df_diff.Territoire.str.contains('95'))]



    elif categorie == "Hauts-de-France":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "59")].dropna()

        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 59)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "59")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 59)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 59)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 59)].dropna()

        s1 = s.filter(regex="59")
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        #s1.replace({np.nan:0}, inplace=True)
        df1 = s1.iloc[:, 1:]

        df_search_users = df_search_users[(df_search_users.Territoire == 59)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('59'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "59")]

        df4 = df4[(df4['territoire'].str.contains("59"))]

        df_diff = df_diff[(df_diff.Territoire.str.contains('59', na=False))]


    elif categorie == "Grand-Est":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "67")].dropna()

        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 67)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "67")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 67)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 67)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 67)].dropna()

        s1 = s.filter(regex="67")
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        #s1.replace({np.nan:0}, inplace=True)
        df1 = s1.iloc[:, 1:]

        df_search_users = df_search_users[(df_search_users.Territoire == 67)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('67'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "67")]

        df4 = df4[(df4['territoire'].str.contains("67"))]

        df_diff = df_diff[(df_diff.Territoire.str.contains('67', na=False))]

    elif categorie == "Bourgogne-Franche-Comté":
        df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "21")].dropna()

        df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 21)].dropna()
        df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "21")].dropna()
        df_orga_2 = df_orga_2[(df_orga_2.territory == 21)].dropna()
        df_orga_auto = df_orga_auto[(df_orga_auto.territory == 21)].dropna()
        df_history_data = df_history_data[(df_history_data.territoire == 21)].dropna()

        s1 = s.filter(regex="21")
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        #s1.replace({np.nan:0}, inplace=True)
        df1 = s1.iloc[:, 1:]

        df_search_users = df_search_users[(df_search_users.Territoire == 21)]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('21'))]

        df_users_API = df_users_API[(df_users_API['territories'] == "21")]

        df4 = df4[(df4['territoire'].str.contains("21"))]

        df_diff = df_diff[(df_diff.Territoire.str.contains('21', na=False))]


    elif categorie.startswith("-"):
        df_users_pro_roles = df_users_pro_roles[df_users_pro_roles.territories == cat_dict[categorie]].dropna()
        df_users_pro_roles_test = df_users_pro_roles_test[df_users_pro_roles_test.territory == int(cat_dict[categorie])].dropna()
        df_orga_ceated = df_orga_ceated[df_orga_ceated.territories == cat_dict[categorie]].dropna()
        df_orga_2 = df_orga_2[df_orga_2.territory == int(cat_dict[categorie])].dropna()
        df_orga_auto = df_orga_auto[df_orga_auto.territory == int(cat_dict[categorie])].dropna()
        df_history_data = df_history_data[df_history_data.territoire == int(cat_dict[categorie])].dropna()

        s1 = s.filter(regex=cat_dict[categorie])
        s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
        #s1.replace({np.nan:0}, inplace=True)
        df1 = s1.iloc[:, 1:]

        df_search_users = df_search_users[(df_search_users.Territoire == int(cat_dict[categorie]))]

        df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains(cat_dict[categorie]))]

        df_users_API = df_users_API[df_users_API['territories'] == cat_dict[categorie]]

        df4 = df4[(df4['territoire'].str.contains(cat_dict[categorie]))]

        df_diff = df_diff[(df_diff.Territoire.str.contains(cat_dict[categorie], na=False))]

        
    df_users_pro_roles_2 = df_users_pro_roles[df_users_pro_roles.typeAccount == 'INVITATION']


    st.markdown("### **Nombre de comptes professionnels *validés* (administrateur, éditeur, lecteur)**")

    df_users_pro_roles_n = df_users_pro_roles[df_users_pro_roles.typeAccount != 'INVITATION']
    df_users_pro_roles_n = df_users_pro_roles_n[df_users_pro_roles_n.verified == True]

    col1, col2, col3 = st.columns(3)

    if "OWNER" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_1 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_n.role.value_counts()).loc["OWNER","role"]}</font>
        <br/><font size='3'>comptes "OWNER"<br></font></center>
        """
    if "OWNER" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_4 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_2.role.value_counts()).loc["OWNER","role"]}</font>
        <br/><font size='3'>comptes "OWNER"<br></font></center>
        """

    if not "OWNER" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_1 = f"""<br>
        <center><font face='Helvetica' size='7'>{0}</font>
        <br/><font size='3'>comptes "OWNER"<br></font></center>
        """
    if not "OWNER" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_4 = html_string_1

    if "EDITOR" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_2 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_n.role.value_counts()).loc["EDITOR","role"]}</font>
        <br/><font size='3'>comptes "EDITEUR"<br></font></center>
        """
    if "EDITOR" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_5 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_2.role.value_counts()).loc["EDITOR","role"]}</font>
        <br/><font size='3'>comptes "EDITEUR"<br></font></center>
        """

    if not "EDITOR" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_2 = f"""<br>
        <center><font face='Helvetica' size='7'>{0}</font>
        <br/><font size='3'>comptes "EDITEUR"<br></font></center>
        """
    if not "EDITOR" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_5 = html_string_2


    if "READER" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_3 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_n.role.value_counts()).loc["READER","role"]}</font>
        <br/><font size='3'>comptes "LECTEUR"<br></font></center>
        """
    if "READER" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_6 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_2.role.value_counts()).loc["READER","role"]}</font>
        <br/><font size='3'>comptes "LECTEUR"<br></font></center>
        """

    if not "READER" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_3 = f"""<br>
        <center><font face='Helvetica' size='7'>{0}</font>
        <br/><font size='3'>comptes "LECTEUR"<br></font></center>
        """
    if not "READER" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_6 = html_string_3


    col1.markdown(html_string_1, unsafe_allow_html=True)
    col2.markdown(html_string_2, unsafe_allow_html=True)
    col3.markdown(html_string_3, unsafe_allow_html=True)

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)
    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown("### **Nombre de comptes professionnels *invités* (administrateur, éditeur, lecteur)**")

    col1, col2, col3 = st.columns(3)

    col1.markdown(html_string_4, unsafe_allow_html=True)
    col2.markdown(html_string_5, unsafe_allow_html=True)
    col3.markdown(html_string_6, unsafe_allow_html=True)

    st.markdown(html_string, unsafe_allow_html=True)
    st.markdown(html_string, unsafe_allow_html=True)

    df_users_pro_roles_final = df_users_pro_roles_test.join(pd.get_dummies(df_users_pro_roles_test['role_x']))
    df_users_pro_roles_final = df_users_pro_roles_final.groupby('createdAt').sum()

    df_users_pro_roles_final.reset_index(inplace=True)


    if not "OWNER" in pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list():
        pass

    elif not "EDITOR" in pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list() and len(pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list()) > 1:

        st.markdown("## **Nombre de comptes professionnels *actifs* par mois (administrateur, éditeur, lecteur)**")

        fig = go.Figure(data=[
        go.Bar(name="Owners", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["OWNER"], marker_color='#7201a8'),
        go.Bar(name="Lecteurs", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["READER"],)
        ])

    elif not "READER" in pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list() and len(pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list()) > 1:

        st.markdown("## **Nombre de comptes professionnels *actifs* par mois (administrateur, éditeur, lecteur)**")

        fig = go.Figure(data=[
        go.Bar(name="Owners", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["OWNER"], marker_color='#7201a8'),
        go.Bar(name="Editeurs", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["EDITOR"],)
        ])
    
    elif len(pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list()) == 1:

        st.markdown("## **Nombre de comptes professionnels *actifs* par mois (administrateur, éditeur, lecteur)**")

        fig = go.Figure(data=[
            go.Bar(name="Owners", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["OWNER"], marker_color='#7201a8'),
        ])

    else:
        st.markdown("### **Nombre de comptes professionnels *actifs* par mois (administrateur, éditeur, lecteur)**")

        fig = go.Figure(data=[
        go.Bar(name="Owners", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["OWNER"], marker_color='#7201a8'),
        go.Bar(name="Editeurs", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["EDITOR"], marker_color='#d8576b'),
        go.Bar(name="Lecteurs", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["READER"],)
        ])

    if not df_users_pro_roles_final.empty:
        # Change the bar mode
        fig.update_layout(barmode='stack')

        fig.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre de comptes professionnels",)
        fig.update_traces(hovertemplate = "Date de la création du compte pro : %{x}<br>Nbre de comptes professionnels: %{value}")

        dt_all = pd.date_range(start=df_users_pro_roles['createdAt'].iloc[0],end=df_users_pro_roles['createdAt'].iloc[-1])
        dt_obs = [d.strftime("%Y-%m") for d in pd.to_datetime(df_users_pro_roles['createdAt'])]
        dt_breaks = [d for d in dt_all.strftime("%Y-%m").tolist() if not d in dt_obs]

        fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

        st.plotly_chart(fig, use_container_width=True)


    st.markdown("### **Nombre d'organisation créé par mois** (et celles ayant au moins un compte pro validé)")

    df_orga_ceated_month = pd.DataFrame(df_orga_ceated.groupby('createdAt')['organization_id'].count()).reset_index()


    # Création d'une table avec le nombre d'orga avec au moins un utilisateur
    table = pd.pivot_table(df_orga_2,index=['createdAt'],aggfunc={'COUNT':np.sum}).reset_index()
    teble_2 = pd.merge(table,df_orga_ceated_month, on='createdAt')

    if teble_2.empty :
        st.markdown("Aucune organisation créée sur ce territoire")
    else:
        teble_2['Organisations sans compte pro actif'] = teble_2.organization_id - teble_2.COUNT
        teble_2["Pourcentage"] = ((teble_2.COUNT / teble_2.organization_id)*100).round(2)

        ## pass the text to the second graph_object only
        fig2 = go.Figure(data=[
            go.Line(name='Organisations créées', x=teble_2.createdAt, y=teble_2.organization_id, marker_color='#7201a8'),
            go.Line(name='Organisations avec au moins un compte pro validé', x=teble_2.createdAt, y=teble_2.COUNT, marker_color='#bd3786',
                text=[f"<b>{percent_change:.0f}%" if percent_change > 0 else f"{percent_change:.0f}%" 
                    for percent_change in teble_2.Pourcentage],
                textposition='top center',
                mode='lines+markers+text')   
        ])
        fig2.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre d'organisations",)
        fig2.update_traces(hovertemplate = "Date de la création de compte organisation : %{x}<br>Nbre d'organisation: %{y}")

        st.plotly_chart(fig2, use_container_width=True)

        test = pd.DataFrame(teble_2.sum()).reset_index()
        test.drop(labels=0, inplace=True)
        test['orga_sans_compte_pro_validé'] = test.iloc[1,1] - test.iloc[0,1]
        test.replace({'COUNT' : 'Organisations avec au moins un compte pro validé','Organisations sans compte pro actif':'Organisations sans compte pro validé'}, inplace=True)
        test.drop(labels=[2,4], axis=0, inplace=True)
        test.set_index("index", inplace=True)    

        fig3 = px.pie(values=test[0], names=test.index, color_discrete_sequence= [ '#7201a8', '#d8576b'],)
        fig3.update_traces(hovertemplate = "%{label}: <br>Nbre d'organisations: %{value}")


        st.plotly_chart(fig3, use_container_width=True)


        st.markdown('### **Nombre d\'organismes "autonomes"**')
        
        df_orga_auto.drop_duplicates(subset='orgaName', inplace=True)

        col1, col2 = st.columns(2)

        html_string_9 = f"""<br>
        <center><font face='Helvetica' size='7'>{df_orga_auto.orgaName.count()}</font>
        <br/><font size='3'>Nombre d'organisations<br>avec au moins une mise à jour</font></center>
        """
        html_string_10 = f"""<br>
        <center><font face='Helvetica' size='7'>{df_orga_auto[df_orga_auto.created_at  > lastMonth.strftime('%Y-%m-%d')]['orgaName'].count()}</font>
        <br/><font size='3'>Nombre d'organisations<br>avec au moins une mise à jour (dans les 6 derniers mois)<br></font></center>
        """

        col1.markdown(html_string_9, unsafe_allow_html=True)
        col2.markdown(html_string_10, unsafe_allow_html=True)

        df = pd.DataFrame({'cat': ["Organisations dont la dernière mise à jour à plus de 6 mois", "Organisations dont la dernière mise à jour à moins de 6 mois"],
                    'Nbre_orga': [df_orga_auto[df_orga_auto.created_at  < lastMonth.strftime('%Y-%m-%d')]['orgaName'].count(), df_orga_auto[df_orga_auto.created_at  >= lastMonth.strftime('%Y-%m-%d')]['orgaName'].count()]})

        df.loc[2] = ["Organisations qui n'a jamais fait de mise à jour", teble_2.organization_id.sum() - (df_orga_auto[df_orga_auto.created_at  < lastMonth.strftime('%Y-%m-%d')]['orgaName'].count() + df_orga_auto[df_orga_auto.created_at  > lastMonth.strftime('%Y-%m-%d')]['orgaName'].count())]
        
        fig4 = px.pie(values=df.Nbre_orga, names=df.cat, color_discrete_sequence= [ '#7201a8', '#d8576b'],)
        fig4.update_traces(textinfo='percent + value')
        fig4.update_traces(hovertemplate = "%{label}: <br>Nbre d'organisations: %{value}")


        st.plotly_chart(fig4, use_container_width=True)

        st.markdown('**Comptes ayant fait des mises à jour en hiver / en été**')

        df_orga_auto_season = df_orga_auto.sort_values('isCampaign').drop_duplicates(subset=['orgaName', 'isCampaign'], keep='last')

        # organisation avec màj season
        test = df_orga_auto_season.sort_values('isCampaign').drop_duplicates(subset="orgaName", keep="last")
        test[test.isCampaign == True]['index'].count()

        df_seasoned = pd.DataFrame({"Type d'orga":["Orga avec màj en hiver/été", "Orga avec màj uniquement hors hiver/été"],
                            "Nbre d'orga":[df_orga_auto_season[df_orga_auto_season.isCampaign ==True]['index'].count(),((df.iloc[0,1] + df.iloc[1,1]) - test[test.isCampaign == True]['index'].count())]})

        fig5 = px.pie(values=df_seasoned['Nbre d\'orga'], names=df_seasoned['Type d\'orga'], color_discrete_sequence= [ '#7201a8', '#d8576b'],)

        st.plotly_chart(fig5, use_container_width=True)
        
     
        st.markdown('### **Nombre de fiches mises à jour en autonomie par les comptes professionnels**')

        df_history_data_grp = df_history_data.groupby(['monthly'], as_index=False).agg({'status_PRO':'sum'})

        df_history_data_grp.rename(columns={"status_PRO":'Nbre de fiches'}, inplace=True)

        fig6 = px.line(df_history_data_grp, x="monthly", y=["Nbre de fiches"], custom_data=['variable'], color_discrete_sequence= [ '#7201a8', '#bd3786', '#2896A0']) 
        fig6.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre de fiches mises à jour par les pro",)
        fig6.update_traces(hovertemplate = "Date de la création du compte pro : %{x}<br>Nbre de fiches mises à jour par les pro: %{y}")
        fig6.update_layout(legend={'title_text':''})

        st.plotly_chart(fig6, use_container_width=True)

        
# Diffuser nos dispositifs sur les territoires

    st.title("Diffuser nos dispositifs sur les territoires")

    st.markdown('### **Nombre de recherches**')
    st.markdown('#### *-par catégorie : *')

    figSearch = px.line(s1,x='datePresentation', y=s1.columns.values.tolist()[1:])
    figSearch.update_xaxes(title_text="Date des recherches", title_standoff=0.6, title_font_family="Times New Roman")
    figSearch.update_yaxes(title_text="Nombre de recherches (non cumulé)", title_font_family="Times New Roman")

    annotationsSearch = dict(xref='paper', yref='paper', x=0.055, y=1,
                                xanchor='center', yanchor='top',
                                text='Fait le: ' + str("1 janvier 2022"),
                                font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                                showarrow=False)
    figSearch.update_traces( mode='lines+markers', hovertemplate=None)
                            
    figSearch.update_layout(xaxis=dict(tickformat="%B %Y"))
    figSearch.update_layout(hovermode="x", title_font_family="Times New Roman", annotations=[annotationsSearch])


    st.plotly_chart(figSearch, use_container_width=True)

    st.markdown('#### *-par type d\'utilisateur : *')

    df_search_users['createdAt'] = pd.to_datetime(df_search_users['createdAt'])
    df_search_users = df_search_users[df_search_users.createdAt < "2022-01-01"]
    df_search_users['createdAt'] = df_search_users.createdAt.dt.strftime('%Y-%m')
    df_search_users.fillna('inconnu', inplace=True)

    df_search_users = df_search_users.join(pd.get_dummies(df_search_users['status']))
    df_search_users.drop(columns=['categorie','status'], inplace=True)
    df_search_users_month = df_search_users.groupby('createdAt').sum()
    df_search_users_month.reset_index(inplace=True)

    if len(df_search_users_month.columns.to_list()) == 9 or categorie == "France":

        figSearch_user = go.Figure(data=[
            go.Line(name='Equipe Soliguide', x=df_search_users_month.createdAt, y=df_search_users_month.ADMIN_SOLIGUIDE, marker_color='#7201a8'),
            go.Line(name='Equipe Territoriale', x=df_search_users_month.createdAt, y=df_search_users_month.ADMIN_TERRITORY, marker_color='#bd3786'),
            go.Line(name='Utilisateurs API', x=df_search_users_month.createdAt, y=df_search_users_month.API_USER, marker_color='#bd3786'),
            go.Line(name='Acteurs', x=df_search_users_month.createdAt, y=df_search_users_month.PRO,),
            go.Line(name='Inconnu', x=df_search_users_month.createdAt, y=df_search_users_month.inconnu,

                mode='lines+markers')   
        ])

    if len(df_search_users_month.columns.to_list()) == 4:

        figSearch_user = go.Figure(data=[
            go.Line(name='Inconnu', x=df_search_users_month.createdAt, y=df_search_users_month.inconnu,

                mode='lines+markers')   
        ])
    elif "PRO" not in df_search_users_month.columns.to_list() and "API_USER" not in df_search_users_month.columns.to_list():

        figSearch_user = go.Figure(data=[
            go.Line(name='Equipe Soliguide', x=df_search_users_month.createdAt, y=df_search_users_month.ADMIN_SOLIGUIDE, marker_color='#7201a8'),
            go.Line(name='Inconnu', x=df_search_users_month.createdAt, y=df_search_users_month.inconnu,

                mode='lines+markers')   
        ])

    elif "API_USER" not in df_search_users_month.columns.to_list() and "ADMIN_TERRITORY" in df_search_users_month.columns.to_list():

        figSearch_user = go.Figure(data=[
            go.Line(name='Equipe Soliguide', x=df_search_users_month.createdAt, y=df_search_users_month.ADMIN_SOLIGUIDE, marker_color='#7201a8'),
            go.Line(name='Equipe Territoriale', x=df_search_users_month.createdAt, y=df_search_users_month.ADMIN_TERRITORY, marker_color='#bd3786'),
            go.Line(name='Acteurs', x=df_search_users_month.createdAt, y=df_search_users_month.PRO,),
            go.Line(name='Inconnu', x=df_search_users_month.createdAt, y=df_search_users_month.inconnu,

                mode='lines+markers')   
        ])

    elif "ADMIN_TERRITORY" not in df_search_users_month.columns.to_list() and "API_USER" not in df_search_users_month.columns.to_list():

        figSearch_user = go.Figure(data=[
            go.Line(name='Equipe Soliguide', x=df_search_users_month.createdAt, y=df_search_users_month.ADMIN_SOLIGUIDE, marker_color='#7201a8'),
            go.Line(name='Acteurs', x=df_search_users_month.createdAt, y=df_search_users_month.PRO,),
            go.Line(name='Inconnu', x=df_search_users_month.createdAt, y=df_search_users_month.inconnu,

                mode='lines+markers')   
        ])

    elif "ADMIN_TERRITORY" not in df_search_users_month.columns.to_list():

        figSearch_user = go.Figure(data=[
            go.Line(name='Equipe Soliguide', x=df_search_users_month.createdAt, y=df_search_users_month.ADMIN_SOLIGUIDE, marker_color='#7201a8'),
            go.Line(name='Utilisateurs API', x=df_search_users_month.createdAt, y=df_search_users_month.API_USER, marker_color='#bd3786'),
            go.Line(name='Acteurs', x=df_search_users_month.createdAt, y=df_search_users_month.PRO,),
            go.Line(name='Inconnu', x=df_search_users_month.createdAt, y=df_search_users_month.inconnu,

                mode='lines+markers')   
        ])

    figSearch_user.update_xaxes(title_text="Date des recherches", title_standoff=0.6, title_font_family="Times New Roman")
    figSearch_user.update_yaxes(title_text="Nombre de recherches (non cumulé)", title_font_family="Times New Roman")

    annotationsSearch_user = dict(xref='paper', yref='paper', x=0.055, y=1,
                                xanchor='center', yanchor='top',
                                text='Fait le: ' + str("1 janvier 2022"),
                                font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                                showarrow=False)
    figSearch_user.update_traces( mode='lines+markers', hovertemplate=None)
                            
    figSearch_user.update_layout(xaxis=dict(tickformat="%B %Y"))
    figSearch_user.update_layout(hovermode="x", title_font_family="Times New Roman", annotations=[annotationsSearch_user])

    st.plotly_chart(figSearch_user, use_container_width=True)
    # ## Nombre d'organismes "relais de diffusion"

    st.markdown('### **Nombre d\'organismes "relais de diffusion & de partenaires API**"')

    df_relais_clean['Relais'] = df_relais_clean.Relation.str.contains('elais')

    df_relais_vf = pd.DataFrame(df_relais_clean.Relais.value_counts())

    # Nombre de compte API

    col1, col2 = st.columns(2)

    if not df_relais_vf.empty and True in df_relais_vf.index.to_list():
        html_string_a = f"""<br>
        <center><font face='Helvetica' size='7'>{df_relais_vf.loc[True,'Relais']}</font>
        <br/><font size='3'>Organismes relais de "Diffusion"<br></font></center>
        """
        col1.markdown(html_string_a, unsafe_allow_html=True)

    df_users_API_vf = pd.DataFrame(df_users_API.value_counts()).reset_index()
    df_users_API_vf = df_users_API_vf[df_users_API_vf.status.str.contains('API')].reset_index()


    html_string_b = f"""<br>
    <center><font face='Helvetica' size='7'>{df_users_API_vf[0].sum()}</font>
    <br/><font size='3'>partenaires API*<br></font></center>
    """

    col2.markdown(html_string_b, unsafe_allow_html=True)
    
    st.markdown("### **Nombre d'utilisateurs* **")
    st.markdown("* *ne sont comptabilisé ici que les utilisateurs qui ont accepter l'utilisation de cookies*")

    df4 = df4.iloc[:-1,:]

    fig4 = px.line(df4, x='Unnamed: 0', y=['Utilisateurs']) 

    fig4.update_xaxes(title_text="Intervalle de temps en mois", title_standoff=0.6, title_font_family="Times New Roman")
    fig4.update_yaxes(title_text="Nombre d'utilisateurs/sessions/pages vues", title_font_family="Times New Roman")
    annotations = dict(xref='paper', yref='paper', x=0.055, y=1,
                                 xanchor='center', yanchor='top',
                                 text='Fait le: ' + str("1 janvier 2022"),
                                 font=dict(family='Arial',
                                           size=12,
                                           color='rgb(150,150,150)'),
                                 showarrow=False)
    fig4.update_traces( mode='lines+markers', hovertemplate=None)
    fig4.update_layout(hovermode="x unified", title_font_family="Times New Roman", annotations=[annotations])
    fig4.update_layout(xaxis=dict(tickformat="%B-%Y"))
    fig4.update_layout(hovermode="x unified", title_font_family="Times New Roman", annotations=[annotations],
                      legend={'title_text':''})


    st.plotly_chart(fig4, use_container_width=True)



    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### **Nombre de professionnels et bénévoles de l’action sociale touchés par une action de diffusion**")

    if len(df_diff['Date']) < 1:
        st.markdown('Aucune action de diffusion n\'a été enregistrée su rce territoire')
    else:
        df_diff_pro_benef = df_diff[['Date','Territoire','Nb de pros','Nb de bénéficiaires']]
        df_diff_pro_benef['Date'] = pd.to_datetime(df_diff_pro_benef.Date)

        df_diff_pro_benef = df_diff_pro_benef[df_diff_pro_benef['Date'] > "2017-01-01"]

        df_diff_pro_benef['Date'] = df_diff_pro_benef.Date.dt.strftime('%Y-%m')

        df_diff_pro = pd.DataFrame(df_diff_pro_benef.groupby('Date')['Nb de pros'].sum())
        df_diff_pro.reset_index(inplace=True)

        df_diff_pro_cum = df_diff_pro.copy()
        df_diff_pro_cum['Nb de pros'] = df_diff_pro_cum['Nb de pros'].cumsum()

        figProDifCum = go.Figure(data=[
        go.Bar(name="Pro", x=df_diff_pro_cum['Date'], y=df_diff_pro_cum["Nb de pros"], marker_color='#7201a8'),
        ])

        figProDifCum.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre de comptes professionnels",)
        figProDifCum.update_traces(hovertemplate = "Date de la mise à jour : le %{x}<br>Nbre de comptes professionnels: %{value}")

        dt_all = pd.date_range(start=df_diff_pro_cum['Date'].iloc[0],end=df_diff_pro_cum['Date'].iloc[-1])
        dt_obs = [d.strftime("%Y-%m") for d in pd.to_datetime(df_diff_pro_cum['Date'])]
        dt_breaks = [d for d in dt_all.strftime("%Y-%m").tolist() if not d in dt_obs]

        figProDifCum.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

        st.plotly_chart(figProDifCum, use_container_width=True)


        expander = st.expander("Nombre de professionnels touchés (par mois)")

        figProDif = go.Figure(data=[
        go.Bar(name="Pro", x=df_diff_pro['Date'], y=df_diff_pro["Nb de pros"], marker_color='#7201a8'),
        ])

        figProDif.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre de comptes professionnels",)
        figProDif.update_traces(hovertemplate = "Date de la mise à jour : le %{x}<br>Nbre de comptes professionnels: %{value}")

        dt_all = pd.date_range(start=df_diff_pro['Date'].iloc[0],end=df_diff_pro['Date'].iloc[-1])
        dt_obs = [d.strftime("%Y-%m") for d in pd.to_datetime(df_diff_pro['Date'])]
        dt_breaks = [d for d in dt_all.strftime("%Y-%m").tolist() if not d in dt_obs]

        figProDif.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

        expander.plotly_chart(figProDif, use_container_width=True)


        ### Nombre de bénéficiaires

        st.markdown("### **Nombre de bénéficiaires de l’action sociale touchés par une action de diffusion**")

        df_diff_bénéf = pd.DataFrame(df_diff_pro_benef.groupby('Date')['Nb de bénéficiaires'].sum())
        df_diff_bénéf.reset_index(inplace=True)

        df_diff_bénéf_cum = df_diff_bénéf.copy()
        df_diff_bénéf_cum['Nb de bénéficiaires'] = df_diff_bénéf_cum['Nb de bénéficiaires'].cumsum()

        figDiffBenefCum = go.Figure(data=[
            go.Bar(name="Nb de bénéficiaires", x=df_diff_bénéf_cum['Date'], y=df_diff_bénéf_cum["Nb de bénéficiaires"], marker_color='#d8576b'),
        ])

        figDiffBenefCum.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre de bénéficiaires",)
        figDiffBenefCum.update_traces(hovertemplate = "Date de la mise à jour : le %{x}<br>Nbre de bénéficiaires: %{value}")

        dt_all = pd.date_range(start=df_diff_bénéf_cum['Date'].iloc[0],end=df_diff_bénéf_cum['Date'].iloc[-1])
        dt_obs = [d.strftime("%Y-%m") for d in pd.to_datetime(df_diff_bénéf_cum['Date'])]
        dt_breaks = [d for d in dt_all.strftime("%Y-%m").tolist() if not d in dt_obs]

        figDiffBenefCum.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

        st.plotly_chart(figDiffBenefCum, use_container_width=True)


        expander = st.expander("Nombre de bénéficiaires touchés (par mois)")

        figDiffBenef = go.Figure(data=[
            go.Bar(name="Pro", x=df_diff_bénéf['Date'], y=df_diff_bénéf["Nb de bénéficiaires"], marker_color='#d8576b'),
        ])

        figDiffBenef.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre de bénéficiaires",)
        figDiffBenef.update_traces(hovertemplate = "Date de la mise à jour : le %{x}<br>Nbre de bénéficiaires: %{value}")

        dt_all = pd.date_range(start=df_diff_bénéf_cum['Date'].iloc[0],end=df_diff_bénéf_cum['Date'].iloc[-1])
        dt_obs = [d.strftime("%Y-%m") for d in pd.to_datetime(df_diff_bénéf_cum['Date'])]
        dt_breaks = [d for d in dt_all.strftime("%Y-%m").tolist() if not d in dt_obs]

        figDiffBenef.update_xaxes(rangebreaks=[dict(values=dt_breaks)])


        expander.plotly_chart(figDiffBenef, use_container_width=True)


