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

Dep_to_num = {"Alpes-Maritimes" :"06", "Ardèche":"07",
            "Bouche-du-Rhône": "13","Cantal":"15","Charente":"16","Côte-d'Or" : "21", "Dordogne":"24","Gironde":"33","Hérault":"34","Indre":"36",
            "Loire-Atlantique" : "44","Nord":"59" , "Puy-de-Dôme":"63","Haute-Vienne":"87",
            "Bas-Rhin":"67", "Paris" : "75", "- Seine-Maritime":"76",
            "Seine-et-Marne":'77', "Yvelines":"78", "- Essonne" :"91", 
            "Hauts-de-Seine":"92","Seine-Saint-Denis": "93","Val-de-Marne": "94", 
            "Val-d'Oise":"95"}

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
df_diff = df_diff[['Date','Territoire','Nb de pros','Nb de bénéficiaires','Diffusion_name','Type','Fiches']]
df_diff = df_diff.fillna(0)

df_fiches_total = pd.read_csv('./ressource/df_fiches_total.csv')

df_newsletter = pd.read_csv('./ressource/data.csv')
df_newsletter = df_newsletter[['Campaign Name','Sent','Opened','Clicked']]

df_newsletter['Territoire'] = df_newsletter['Campaign Name'].str[0:2]
df_newsletter['Tx ouverture'] = round((df_newsletter['Opened'] / df_newsletter['Sent'])*100,2)
df_newsletter['Tx clic'] = round((df_newsletter['Clicked'] / df_newsletter['Opened'])*100,2)


df_listing = pd.read_csv('./ressource/Listing repérés-allDep.csv')
df_listing_count = df_listing[['Territoire','Etat']]
df_listing_count.fillna('Rien', inplace=True)
df_listing_count_vf = df_listing_count[df_listing_count.Etat.str.contains('Partenariat actif')]


today = date.today()
lastMonth = today - pd.Timedelta(days=183)


df_hebergeurs_dispo = pd.read_csv('./ressource/Hébergeur.euse.s-Tout DA.csv')
df_hebergeurs_dispo_vf = df_hebergeurs_dispo[['Département','Disponibilité','Statut','Date de début']]
df_hebergeurs_dispo_vf = df_hebergeurs_dispo_vf[(df_hebergeurs_dispo_vf.Disponibilité == "Disponible") & (df_hebergeurs_dispo_vf.Statut == "Validé")]
df_hebergeurs_dispo_vf['Date de début'] = pd.to_datetime(df_hebergeurs_dispo_vf['Date de début'])
df_hebergeurs_dispo_vf['territory'] = df_hebergeurs_dispo_vf['Département'].map(Dep_to_num)
df_hebergeurs_dispo_vf.dropna(subset=['Date de début'], inplace=True)
df_hebergeurs_dispo_final = df_hebergeurs_dispo_vf.join(
    df_hebergeurs_dispo_vf.apply(lambda v: pd.Series(pd.date_range(v['Date de début'], today.strftime("%Y-%m"), freq='M').to_period('M')), axis=1)
    .apply(pd.value_counts, axis=1)
    .fillna(0)
    .astype(int)
)
df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[:,4:]

df_hebergement = pd.read_csv('./ressource/Hébergement-Tout.csv')
df_hebergement_vf = df_hebergement[['Territoire','Statut','Date début','Date fin']]
df_hebergement_vf['territory'] = df_hebergement_vf['Territoire'].map(Dep_to_num)
df_hebergement_vf['Date fin'] = pd.to_datetime(df_hebergement_vf['Date fin'])
df_hebergement_vf['Date fin'] = df_hebergement_vf['Date fin'] .dt.strftime('%Y-%m')
df_hebergement_vf['Date début'] = pd.to_datetime(df_hebergement_vf['Date début'])
df_hebergement_vf['Date début'] = df_hebergement_vf['Date début'] .dt.strftime('%Y-%m')
df_hebergement_vf.dropna(subset=['Date début','Date fin'], inplace=True) 

df_hebergement_final = df_hebergement_vf.join(
    df_hebergement_vf.apply(lambda v: pd.Series(pd.date_range(v['Date début'], v['Date fin'], freq='M').to_period('M')), axis=1)
    .apply(pd.value_counts, axis=1)
    .fillna(0)
    .astype(int)
)

df_hebergement = df_hebergement[['Territoire','Statut','Date début','Date fin']]
df_hebergement['territory'] = df_hebergement['Territoire'].map(Dep_to_num)

df_maj_6_months = pd.read_csv("./ressource/mise_a_jour_6_mois.csv")
df_maj_6_months.set_index('territoire', inplace=True)

df_fiche_serv_on_off = pd.read_csv('./ressource/df_fiches_nb_serv.csv')

df_ville = pd.read_csv('./ressource/df_ville.csv')

df_exhaustivity = pd.read_csv('./ressource/exhaustivite_territoires.csv')

df_categorie_vf = pd.read_csv('./ressource/df_categorie_vf.csv')
df_categorie_vf['territory'] = df_categorie_vf['departement'].map(Dep_to_num)


df_prospection = pd.read_csv('/home/antoine/Bureau/Streamlit/Dashboard_indicateurs/Partenaires-Tout.csv')
df_prospection_cleaned = df_prospection[['Compte-rendu','Département (from CR)']].dropna()
df_prospection_cleaned_2 = df_prospection_cleaned['Département (from CR)'].str.split(',', expand=True)
df_prospection_cleaned_vf = pd.DataFrame(df_prospection_cleaned_2[0].value_counts()).reset_index()
df_prospection_cleaned_vf.rename(columns={"index":"Departement", 0 : "Nombre de rdv"}, inplace=True)
df_prospection_vf = df_prospection_cleaned_vf[(df_prospection_cleaned_vf.Departement != "Gironde") &
                                             (df_prospection_cleaned_vf.Departement != "Puy-de-Dôme") &
                                              (df_prospection_cleaned_vf.Departement != "Paris") &
                                              (df_prospection_cleaned_vf.Departement != "Loire-Atlantique")&
                                             (df_prospection_cleaned_vf.Departement != "Bouches-du-Rhône")&
                                             (df_prospection_cleaned_vf.Departement != "Hérault")&
                                             (df_prospection_cleaned_vf.Departement != "Seine-Maritime")&
                                             (df_prospection_cleaned_vf.Departement != "Nord")&
                                             (df_prospection_cleaned_vf.Departement != "Cantal")&
                                             (df_prospection_cleaned_vf.Departement != "Bas-Rhin") &
                                             (df_prospection_cleaned_vf.Departement != "Ille-et-Vilaine") &
                                             (df_prospection_cleaned_vf.Departement != "Val-d'Oise") &
                                             (df_prospection_cleaned_vf.Departement != "Alpes-Maritimes") &
                                             (df_prospection_cleaned_vf.Departement != "Indre") &
                                             (df_prospection_cleaned_vf.Departement != "Côte-d'Or") &
                                             (df_prospection_cleaned_vf.Departement != "Yvelines") &
                                             (df_prospection_cleaned_vf.Departement != "Hauts-de-Seine") &
                                             (df_prospection_cleaned_vf.Departement != "Drôme") &
                                             (df_prospection_cleaned_vf.Departement != "Seine-Saint-Denis") &
                                             (df_prospection_cleaned_vf.Departement != "Val-de-Marne") ]



cat_dict = {"France":'Total', "- Alpes-Maritimes (06)" :"06", "- Ardèche (07)":"07",
            "- Bouche-du-Rhône (13)": "13","- Cantal (15)":"15","- Charente (16)":"16","- Côte-d'Or (21)" : "21", "- Dordogne (24)":"24","- Gironde (33)":"33","- Hérault (34)":"34","- Indre (36)":"36",
            "- Loire-Atlantique (44)" : "44","- Nord (59)":"59" , "- Puy-de-Dôme (63)":"63","- Haute-Vienne (87)":"87",
            "- Bas-Rhin (67)":"67", "- Paris (75)" : "75", "- Seine-Maritime (76)":"76",
            "- Seine-et-Marne (77)":'77', "- Yvelines (78)":"78", "- Essonne (91)" :"91", 
            "- Hauts-de-Seine (92)":"92","- Seine-Saint-Denis (93)": "93","- Val-de-Marne (94)": "94", 
            "- Val-d'Oise (95)":"95"}

 

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

    df_fiches_total = df_fiches_total

    df_newsletter_2 = df_newsletter.sum()

    df_listing_count_vf = df_listing_count_vf

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.drop(columns = ['territory'], inplace=True)
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.astype(str)
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T
    
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T
    
    df_hebergement = df_hebergement

    df_maj_6_months = df_maj_6_months

    df_fiche_serv_on_off = df_fiche_serv_on_off

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity

    df_categorie_vf = df_categorie_vf

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

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 6) | (df_fiches_total.territory == 13)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "06") | (df_newsletter.Territoire == "13")]
    df_newsletter_2 = df_newsletter.sum()

    df_listing_count_vf = df_listing_count_vf[(df_listing_count_vf.Territoire == "06") | (df_listing_count_vf.Territoire == "13")]

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "06") | (df_hebergeurs_dispo_final.territory == "13")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "06") | (df_hebergement_final.territory == "13")]
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T
    
    df_hebergement = df_hebergement[(df_hebergement.territory == "06") | (df_hebergement.territory == "13")]

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "06") | (df_maj_6_months.index == "13")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 6) | (df_fiche_serv_on_off.territory == 13)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('06')) | (df_ville['territory'].str.startswith('13'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 6) | (df_exhaustivity.Département == 13)]

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "06") | (df_categorie_vf.territory == "13")]

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

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 7) | (df_fiches_total.territory == 15) | (df_fiches_total.territory == 63)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "07") | (df_newsletter.Territoire == "15") | (df_newsletter.Territoire == "63")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "07") | (df_hebergeurs_dispo_final.territory == "15")
     | (df_hebergeurs_dispo_final.territory == "63")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "07") | (df_hebergement_final.territory == "15") 
    | (df_hebergement_final.territory == "63")]
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T
    
    df_hebergement = df_hebergement[(df_hebergement.territory == "07") | (df_hebergement.territory == "15") | (df_hebergement.territory == "63")]

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "07") | (df_maj_6_months.index == "15") | (df_maj_6_months.index == "63")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 67) | (df_fiche_serv_on_off.territory == 15) | (df_fiche_serv_on_off.territory == 63)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('07')) | (df_ville['territory'].str.startswith('15')) | (df_ville['territory'].str.startswith('63'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 7) | (df_exhaustivity.Département == 15) | (df_exhaustivity.Département == 63)]

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "07") | (df_categorie_vf.territory == "15") | (df_categorie_vf.territory == "63")]

elif categorie == "Occitanie":
    df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "34")].dropna()
    df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 34)].dropna()
    df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "34")].dropna()
    df_orga_2 = df_orga_2[(df_orga_2.territory == 34)].dropna()
    df_orga_auto = df_orga_auto[(df_orga_auto.territory == 34)].dropna()
    df_history_data = df_history_data[(df_history_data.territoire == 34)].dropna()

    s1 = s.filter(regex="34")
    s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
    df1 = s1.iloc[:, 1:]

    df_search_users = df_search_users[(df_search_users.Territoire == 34)]

    df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('34'))]

    df_users_API = df_users_API[(df_users_API['territories'] == "34")]

    df4 = df4[(df4['territoire'].str.contains("34"))]

    df_diff = df_diff[(df_diff.Territoire.str.contains('34', na=False))]

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 34)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "34")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "34")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "34")]
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T
    
    df_hebergement = df_hebergement[(df_hebergement.territory == "34")]


    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "34")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 34)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('34'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('34'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 34)]

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "34")]

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

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 33) | (df_fiches_total.territory == 87) | (df_fiches_total.territory == 16) | (df_fiches_total.territory == 24)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "33") | (df_newsletter.Territoire == "87") | (df_newsletter.Territoire == "16") | (df_newsletter.Territoire == "24")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "33") | (df_hebergeurs_dispo_final.territory == "87")
     | (df_hebergeurs_dispo_final.territory == "16") | (df_hebergeurs_dispo_final.territory == "24")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "33") | (df_hebergement_final.territory == "87")
    | (df_hebergement_final.territory == "16")| (df_hebergement_final.territory == "24")] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T

    df_hebergement = df_hebergement[(df_hebergement.territory == "33") | (df_hebergement.territory == "87") | (df_hebergement.territory == "16") | (df_hebergement.territory == "24")]

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "33") | (df_maj_6_months.index == "87") | (df_maj_6_months.index == "16") | (df_maj_6_months.index == "24")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 33) | (df_fiche_serv_on_off.territory == 87) | (df_fiche_serv_on_off.territory == 16) | (df_fiche_serv_on_off.territory == 24)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('33')) | (df_ville['territory'].str.startswith('87')) | (df_ville['territory'].str.startswith('16')) | (df_ville['territory'].str.startswith('24'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 33) | (df_exhaustivity.Département == 87) | (df_exhaustivity.Département == 16) | (df_exhaustivity.Département == 24)]

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "33") | (df_categorie_vf.territory == "87") | (df_categorie_vf.territory == "16") | (df_categorie_vf.territory == "24")]

elif categorie == "Centre-Val-de-Loire":
    df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "36")].dropna()

    df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 36)].dropna()
    df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "36")].dropna()
    df_orga_2 = df_orga_2[(df_orga_2.territory == 36)].dropna()
    df_orga_auto = df_orga_auto[(df_orga_auto.territory == 36)].dropna()
    df_history_data = df_history_data[(df_history_data.territoire == 36)].dropna()

    s1 = s.filter(regex="34")
    s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
    df1 = s1.iloc[:, 1:]

    df_search_users = df_search_users[(df_search_users.Territoire == 36)]

    df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('36'))]

    df_users_API = df_users_API[(df_users_API['territories'] == "36")]

    df4 = df4[(df4['territoire'].str.contains("36"))]

    df_diff = df_diff[(df_diff.Territoire.str.contains('36', na=False))]

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 36)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "36")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "36")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "36")] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T

    df_hebergement = df_hebergement[(df_hebergement.territory == "36")]

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "36")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 36)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('36'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 36)]

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "36")]

elif categorie == "Pays-de-la-Loire":
    df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "44")].dropna()

    df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 44)].dropna()
    df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "44")].dropna()
    df_orga_2 = df_orga_2[(df_orga_2.territory == 44)].dropna()
    df_orga_auto = df_orga_auto[(df_orga_auto.territory == 44)].dropna()
    df_history_data = df_history_data[(df_history_data.territoire == 44)].dropna()

    s1 = s.filter(regex="44")
    s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
    df1 = s1.iloc[:, 1:]

    df_search_users = df_search_users[(df_search_users.Territoire == 44)]

    df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('44'))]

    df_users_API = df_users_API[(df_users_API['territories'] == "44")]

    df4 = df4[(df4['territoire'].str.contains("44"))]

    df_diff = df_diff[(df_diff.Territoire.str.contains('44', na=False))]

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 44)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "44")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "44") ]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "44")] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T

    df_hebergement = df_hebergement[(df_hebergement.territory == "44")]

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "44")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 44)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('44'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')
    
    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 44)]

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "44")]

elif categorie == "Normandie":
    df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "76")].dropna()

    df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 76)].dropna()
    df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "76")].dropna()
    df_orga_2 = df_orga_2[(df_orga_2.territory == 76)].dropna()
    df_orga_auto = df_orga_auto[(df_orga_auto.territory == 76)].dropna()
    df_history_data = df_history_data[(df_history_data.territoire == 76)].dropna()

    s1 = s.filter(regex="76")
    s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
    df1 = s1.iloc[:, 1:]

    df_search_users = df_search_users[(df_search_users.Territoire == 76)]

    df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('76'))]

    df_users_API = df_users_API[(df_users_API['territories'] == "76")]

    df4 = df4[(df4['territoire'].str.contains("76"))]

    df_diff = df_diff[(df_diff.Territoire.str.contains('76', na=False))]

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 76)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "76")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "76")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "76")] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T

    df_hebergement = df_hebergement[(df_hebergement.territory == "76")]

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "76")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 76)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('76'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 76)]

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "76")]

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

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 75) | (df_fiches_total.territory == 77) | (df_fiches_total.territory == 78)
    | (df_fiches_total.territory == 91) | (df_fiches_total.territory == 92) | (df_fiches_total.territory == 93) | (df_fiches_total.territory == 94)
    | (df_fiches_total.territory == 95)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "75") | (df_newsletter.Territoire == "77") | (df_newsletter.Territoire == "78") 
    | (df_newsletter.Territoire == "91")  | (df_newsletter.Territoire == "92")  | (df_newsletter.Territoire == "93")  | (df_newsletter.Territoire == "94")
    | (df_newsletter.Territoire == "95")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "75") | (df_hebergeurs_dispo_final.territory == "77")
     | (df_hebergeurs_dispo_final.territory == "78") | (df_hebergeurs_dispo_final.territory == "91") | (df_hebergeurs_dispo_final.territory == "92")
     | (df_hebergeurs_dispo_final.territory == "93") | (df_hebergeurs_dispo_final.territory == "94") | (df_hebergeurs_dispo_final.territory == "95")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "75") | (df_hebergement_final.territory == "77")
    | (df_hebergement_final.territory == "78")| (df_hebergement_final.territory == "91")| (df_hebergement_final.territory == "92")
    | (df_hebergement_final.territory == "93") | (df_hebergement_final.territory == "94") | (df_hebergement_final.territory == "95")] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T
    
    df_hebergement = df_hebergement[(df_hebergement.territory == "75") | (df_hebergement.territory == "77") | (df_hebergement.territory == "78") 
    | (df_hebergement.territory == "91") | (df_hebergement.territory == "92") | (df_hebergement.territory == "93") | (df_hebergement.territory == "94")
    | (df_hebergement.territory == "95")]

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "75") | (df_maj_6_months.index == "77") | (df_maj_6_months.index == "78") | (df_maj_6_months.index == "91")
    | (df_maj_6_months.index == "92") | (df_maj_6_months.index == "93") | (df_maj_6_months.index == "94") | (df_maj_6_months.index == "95")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 75) | (df_fiche_serv_on_off.territory == 77) | (df_fiche_serv_on_off.territory == 78) 
    | (df_fiche_serv_on_off.territory == 91) | (df_fiche_serv_on_off.territory == 92) | (df_fiche_serv_on_off.territory == 93) | (df_fiche_serv_on_off.territory == 94)
    | (df_fiche_serv_on_off.territory == 95)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('75')) | (df_ville['territory'].str.startswith('77')) | (df_ville['territory'].str.startswith('78')) | (df_ville['territory'].str.startswith('91'))
    | (df_ville['territory'].str.startswith('92')) | (df_ville['territory'].str.startswith('93')) | (df_ville['territory'].str.startswith('94')) | (df_ville['territory'].str.startswith('95'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 75) | (df_exhaustivity.Département == 77) | (df_exhaustivity.Département == 78) | (df_exhaustivity.Département == 91)
     | (df_exhaustivity.Département == 92) | (df_exhaustivity.Département == 93) | (df_exhaustivity.Département == 94) | (df_exhaustivity.Département == 95)]

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "75") | (df_categorie_vf.territory == "77") | (df_categorie_vf.territory == "78")
    | (df_categorie_vf.territory == "91") | (df_categorie_vf.territory == "92") | (df_categorie_vf.territory == "93") | (df_categorie_vf.territory == "94")
    | (df_categorie_vf.territory == "95")]

elif categorie == "Hauts-de-France":
    df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "59")].dropna()

    df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 59)].dropna()
    df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "59")].dropna()
    df_orga_2 = df_orga_2[(df_orga_2.territory == 59)].dropna()
    df_orga_auto = df_orga_auto[(df_orga_auto.territory == 59)].dropna()
    df_history_data = df_history_data[(df_history_data.territoire == 59)].dropna()

    s1 = s.filter(regex="59")
    s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
    df1 = s1.iloc[:, 1:]

    df_search_users = df_search_users[(df_search_users.Territoire == 59)]

    df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('59'))]

    df_users_API = df_users_API[(df_users_API['territories'] == "59")]

    df4 = df4[(df4['territoire'].str.contains("59"))]

    df_diff = df_diff[(df_diff.Territoire.str.contains('59', na=False))]

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 59)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "59")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "59")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "59")] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T

    df_hebergement = df_hebergement[(df_hebergement.territory == "59")] 

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "59")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 59)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('59'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 59)]    

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "59")]

elif categorie == "Grand-Est":
    df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "67")].dropna()

    df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 67)].dropna()
    df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "67")].dropna()
    df_orga_2 = df_orga_2[(df_orga_2.territory == 67)].dropna()
    df_orga_auto = df_orga_auto[(df_orga_auto.territory == 67)].dropna()
    df_history_data = df_history_data[(df_history_data.territoire == 67)].dropna()

    s1 = s.filter(regex="67")
    s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
    df1 = s1.iloc[:, 1:]

    df_search_users = df_search_users[(df_search_users.Territoire == 67)]

    df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('67'))]

    df_users_API = df_users_API[(df_users_API['territories'] == "67")]

    df4 = df4[(df4['territoire'].str.contains("67"))]

    df_diff = df_diff[(df_diff.Territoire.str.contains('67', na=False))]

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 67)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "67")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "67")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T


    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "67")] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T

    df_hebergement = df_hebergement[(df_hebergement.territory == "67")] 

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "67")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 67)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('67'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')
    
    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 67)]     

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "67")]

elif categorie == "Bourgogne-Franche-Comté":
    df_users_pro_roles = df_users_pro_roles[(df_users_pro_roles.territories == "21")].dropna()

    df_users_pro_roles_test = df_users_pro_roles_test[(df_users_pro_roles_test.territory == 21)].dropna()
    df_orga_ceated = df_orga_ceated[(df_orga_ceated.territories == "21")].dropna()
    df_orga_2 = df_orga_2[(df_orga_2.territory == 21)].dropna()
    df_orga_auto = df_orga_auto[(df_orga_auto.territory == 21)].dropna()
    df_history_data = df_history_data[(df_history_data.territoire == 21)].dropna()

    s1 = s.filter(regex="21")
    s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
    df1 = s1.iloc[:, 1:]

    df_search_users = df_search_users[(df_search_users.Territoire == 21)]

    df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains('21'))]

    df_users_API = df_users_API[(df_users_API['territories'] == "21")]

    df4 = df4[(df4['territoire'].str.contains("21"))]

    df_diff = df_diff[(df_diff.Territoire.str.contains('21', na=False))]

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == 21)]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == "21")]
    df_newsletter_2 = df_newsletter.sum()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == "21")]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T

    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == "21")] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T
    
    df_hebergement = df_hebergement[(df_hebergement.territory == "21")] 

    df_maj_6_months = df_maj_6_months[(df_maj_6_months.index == "21")]
    df_maj_6_months.loc['Total'] = df_maj_6_months.sum()
    df_maj_6_months.loc['Total','pourcentage'] = round((df_maj_6_months.loc['Total','status'] / df_maj_6_months.loc['Total','lieu_id'])*100, 2)

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == 21)]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith('21'))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == 21)]     

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == "21")]

elif categorie.startswith("-"):
    df_users_pro_roles = df_users_pro_roles[df_users_pro_roles.territories == cat_dict[categorie]].dropna()
    df_users_pro_roles_test = df_users_pro_roles_test[df_users_pro_roles_test.territory == int(cat_dict[categorie])].dropna()
    df_orga_ceated = df_orga_ceated[df_orga_ceated.territories == cat_dict[categorie]].dropna()
    df_orga_2 = df_orga_2[df_orga_2.territory == int(cat_dict[categorie])].dropna()
    df_orga_auto = df_orga_auto[df_orga_auto.territory == int(cat_dict[categorie])].dropna()
    df_history_data = df_history_data[df_history_data.territoire == int(cat_dict[categorie])].dropna()

    s1 = s.filter(regex=cat_dict[categorie])
    s1 = pd.merge(s['datePresentation'],s1, how='left', left_index=True, right_index=True)
    df1 = s1.iloc[:, 1:]

    df_search_users = df_search_users[(df_search_users.Territoire == int(cat_dict[categorie]))]

    df_relais_clean = df_relais_clean[(df_relais_clean['Territoire Rollup'].str.contains(cat_dict[categorie]))]

    df_users_API = df_users_API[df_users_API['territories'] == cat_dict[categorie]]

    df4 = df4[(df4['territoire'].str.contains(cat_dict[categorie]))]

    df_diff = df_diff[(df_diff.Territoire.str.contains(cat_dict[categorie], na=False))]

    df_fiches_total = df_fiches_total[(df_fiches_total.territory == int(cat_dict[categorie]))]

    df_newsletter = df_newsletter[(df_newsletter.Territoire == (cat_dict[categorie]))].reset_index()

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final[(df_hebergeurs_dispo_final.territory == cat_dict[categorie])]
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.groupby('territory').sum()

    df_hebergeurs_dispo_final.loc['Total'] = df_hebergeurs_dispo_final.sum()
    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.iloc[-1:]
    df_hebergeurs_dispo_final.columns = df_hebergeurs_dispo_final.columns.astype('datetime64[ns]')

    df_hebergeurs_dispo_final = df_hebergeurs_dispo_final.T


    df_hebergement_final = df_hebergement_final[(df_hebergement_final.territory == cat_dict[categorie])] 
    df_hebergement_final = df_hebergement_final.iloc[:,5:]
    df_hebergement_final.index = df_hebergement_final.index.astype(str)
    df_hebergement_final.loc['Total'] = df_hebergement_final.sum()
    df_hebergement_final = df_hebergement_final.iloc[-1:]
    df_hebergement_final = df_hebergement_final.astype(str)
    df_hebergement_final.columns = df_hebergement_final.columns.astype('datetime64[ns]')
    df_hebergement_final = df_hebergement_final.T

    df_hebergement = df_hebergement[(df_hebergement.territory == cat_dict[categorie])] 

    df_fiche_serv_on_off = df_fiche_serv_on_off[(df_fiche_serv_on_off.territory == int(cat_dict[categorie]))]

    df_ville.dropna(inplace=True)
    df_ville = df_ville[(df_ville['territory'].str.startswith(cat_dict[categorie]))]

    df_ville_vf = df_ville.groupby(['codePostal','ville']).sum().reset_index()
    df_ville_vf = df_ville_vf.drop(columns='Unnamed: 0')

    df_exhaustivity = df_exhaustivity[(df_exhaustivity.Département == int(cat_dict[categorie]))].reset_index()     

    df_categorie_vf = df_categorie_vf[(df_categorie_vf.territory == cat_dict[categorie])]

##########
## Tous ##
##########

if categorie_2 == 'Tous':

    st.title("Autonomiser les acteurs dans l'utilisation de nos outils")


    df_users_pro_roles_2 = df_users_pro_roles[df_users_pro_roles.typeAccount == 'INVITATION']


    st.markdown("### **Nombre de comptes professionnels *validés* (administrateur, éditeur, lecteur)**")

    df_users_pro_roles_n = df_users_pro_roles[df_users_pro_roles.typeAccount != 'INVITATION']
    df_users_pro_roles_n = df_users_pro_roles_n[df_users_pro_roles_n.verified == True]

    col1, col2, col3 = st.columns(3)

    if "OWNER" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_1 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_n.role.value_counts()).loc["OWNER","role"]}</font>
        <br/><font size='3'>comptes "Adminstrateurs"<br></font></center>
        """
    if "OWNER" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_4 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_2.role.value_counts()).loc["OWNER","role"]}</font>
        <br/><font size='3'>comptes "Adminstrateurs"<br></font></center>
        """

    if not "OWNER" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_1 = f"""<br>
        <center><font face='Helvetica' size='7'>{0}</font>
        <br/><font size='3'>comptes "Adminstrateurs"<br></font></center>
        """
    if not "OWNER" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_4 = html_string_1

    if "EDITOR" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_2 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_n.role.value_counts()).loc["EDITOR","role"]}</font>
        <br/><font size='3'>comptes "Editeurs"<br></font></center>
        """
    if "EDITOR" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_5 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_2.role.value_counts()).loc["EDITOR","role"]}</font>
        <br/><font size='3'>comptes "Editeurs"<br></font></center>
        """

    if not "EDITOR" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_2 = f"""<br>
        <center><font face='Helvetica' size='7'>{0}</font>
        <br/><font size='3'>comptes "Editeurs"<br></font></center>
        """
    if not "EDITOR" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_5 = html_string_2


    if "READER" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_3 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_n.role.value_counts()).loc["READER","role"]}</font>
        <br/><font size='3'>comptes "Lecteurs"<br></font></center>
        """
    if "READER" in pd.DataFrame(df_users_pro_roles_2.role.value_counts()).T.columns.to_list():
        html_string_6 = f"""<br>
        <center><font face='Helvetica' size='7'>{pd.DataFrame(df_users_pro_roles_2.role.value_counts()).loc["READER","role"]}</font>
        <br/><font size='3'>comptes "Lecteurs"<br></font></center>
        """

    if not "READER" in pd.DataFrame(df_users_pro_roles_n.role.value_counts()).T.columns.to_list():
        html_string_3 = f"""<br>
        <center><font face='Helvetica' size='7'>{0}</font>
        <br/><font size='3'>comptes "Lecteurs"<br></font></center>
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
        st.markdown("( compte actif = compte ayant fait au moins une recherche / une mise à jour dans le mois)")

        fig = go.Figure(data=[
        go.Bar(name="Owners", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["OWNER"], marker_color='#7201a8'),
        go.Bar(name="Lecteurs", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["READER"],)
        ])

    elif not "READER" in pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list() and len(pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list()) > 1:

        st.markdown("## **Nombre de comptes professionnels *actifs* par mois (administrateur, éditeur, lecteur)**")
        st.markdown("( compte actif = compte ayant fait au moins une recherche / une mise à jour dans le mois)")

        fig = go.Figure(data=[
        go.Bar(name="Owners", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["OWNER"], marker_color='#7201a8'),
        go.Bar(name="Editeurs", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["EDITOR"],)
        ])
    
    elif len(pd.DataFrame(df_users_pro_roles_test.role_x.value_counts()).T.columns.to_list()) == 1:

        st.markdown("## **Nombre de comptes professionnels *actifs* par mois (administrateur, éditeur, lecteur)**")
        st.markdown("( compte actif = compte ayant fait au moins une recherche / une mise à jour dans le mois)")

        fig = go.Figure(data=[
            go.Bar(name="Owners", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["OWNER"], marker_color='#7201a8'),
        ])

    else:
        st.markdown("## **Nombre de comptes professionnels *actifs* par mois (administrateur, éditeur, lecteur)**")
        st.markdown("( compte actif = compte ayant fait au moins une recherche / une mise à jour dans le mois)")

        fig = go.Figure(data=[
        go.Bar(name="Owners", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["OWNER"], marker_color='#7201a8'),
        go.Bar(name="Editeurs", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["EDITOR"], marker_color='#d8576b'),
        go.Bar(name="Lecteurs", x=df_users_pro_roles_final['createdAt'], y=df_users_pro_roles_final["READER"],)
        ])

    if not df_users_pro_roles_final.empty:
        # Change the bar mode
        fig.update_layout(barmode='stack')

        fig.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre de comptes professionnefig6ls",)
        fig.update_traces(hovertemplate = "Date de la création du compte pro : %{x}<br>Nbre de comptes professionnels: %{value}")

        dt_all = pd.date_range(start=df_users_pro_roles['createdAt'].iloc[0],end=df_users_pro_roles['createdAt'].iloc[-1])
        dt_obs = [d.strftime("%Y-%m") for d in pd.to_datetime(df_users_pro_roles['createdAt'])]
        dt_breaks = [d for d in dt_all.strftime("%Y-%m"
                                               ).tolist() if not d in dt_obs]
        fig.update_layout(legend=dict(orientation="h"))
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
        fig2.update_layout(legend=dict(orientation="h"))

        st.plotly_chart(fig2, use_container_width=True)

        test = pd.DataFrame(teble_2.sum()).reset_index()
        test.drop(labels=0, inplace=True)
        test['orga_sans_compte_pro_validé'] = test.iloc[1,1] - test.iloc[0,1]
        test.replace({'COUNT' : 'Organisations avec au moins un compte pro validé','Organisations sans compte pro actif':'Organisations sans compte pro validé'}, inplace=True)
        test.drop(labels=[2,4], axis=0, inplace=True)
        test.set_index("index", inplace=True)    

        fig3 = px.pie(values=test[0], names=test.index, color_discrete_sequence= [ '#7201a8', '#d8576b'],)
        fig3.update_traces(hovertemplate = "%{label}: <br>Nbre d'organisations: %{value}")
        fig3.update_layout(legend=dict(orientation="h"))


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
        fig4.update_layout(legend=dict(orientation="h"))

        st.plotly_chart(fig4, use_container_width=True)

        st.markdown('**Comptes ayant fait des mises à jour en hiver / en été**')

        df_orga_auto_season = df_orga_auto.sort_values('isCampaign').drop_duplicates(subset=['orgaName', 'isCampaign'], keep='last')

        # organisation avec màj season
        test = df_orga_auto_season.sort_values('isCampaign').drop_duplicates(subset="orgaName", keep="last")
        test[test.isCampaign == True]['index'].count()

        df_seasoned = pd.DataFrame({"Type d'orga":["Orga avec màj en hiver/été", "Orga avec màj uniquement hors hiver/été"],
                            "Nbre d'orga":[df_orga_auto_season[df_orga_auto_season.isCampaign ==True]['index'].count(),((df.iloc[0,1] + df.iloc[1,1]) - test[test.isCampaign == True]['index'].count())]})

        fig5 = px.pie(values=df_seasoned['Nbre d\'orga'], names=df_seasoned['Type d\'orga'], color_discrete_sequence= [ '#7201a8', '#d8576b'],)
        fig5.update_layout(legend=dict(orientation="h"))

        st.plotly_chart(fig5, use_container_width=True)


        st.markdown('### **Nombre de fiches mises à jour en autonomie par les comptes professionnels**')

        df_history_data_grp = df_history_data.groupby(['monthly'], as_index=False).agg({'status_PRO':'sum'})

        df_history_data_grp.rename(columns={"status_PRO":'Nbre de fiches'}, inplace=True)

        fig6 = px.line(df_history_data_grp, x="monthly", y=["Nbre de fiches"], custom_data=['variable'], color_discrete_sequence= [ '#7201a8', '#bd3786', '#2896A0']) 
        fig6.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre de fiches mises à jour par les pro",)
        fig6.update_traces(hovertemplate = "Date de la création du compte pro : %{x}<br>Nbre de fiches mises à jour par les pro: %{y}")
        fig6.update_layout(legend={'title_text':''})
        fig6.update_layout(legend=dict(orientation="h"))

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
    figSearch.update_layout(legend=dict(orientation="h"))


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
    figSearch_user.update_layout(legend=dict(orientation="h"))

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
    st.markdown("\* ne sont comptabilisé ici que les utilisateurs qui ont accepter l'utilisation de cookies")

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
    fig4.update_layout(legend=dict(orientation="h"))


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
        figProDifCum.update_layout(legend=dict(orientation="h"))

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
        figProDif.update_layout(legend=dict(orientation="h"))

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
        figDiffBenefCum.update_layout(legend=dict(orientation="h"))

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
        figDiffBenef.update_layout(legend=dict(orientation="h"))


        expander.plotly_chart(figDiffBenef, use_container_width=True)



        st.markdown("### **Nombre d'actions de diffusion**")

        df_diff_action = df_diff[['Diffusion_name','Territoire','Type','Date']]
        df_diff_action['Date'] = pd.to_datetime(df_diff_action['Date'])
        df_diff_action['Date'] = df_diff_action.Date.dt.strftime('%Y-%m')
        df_diff_action = df_diff_action[df_diff_action['Date'] > "2017-01-01"]

        df_diff_action = df_diff_action.groupby(by=[pd.Grouper(key="Date"), "Type"])["Diffusion_name"]
        df_diff_action = df_diff_action.count().reset_index()

        df_diff_action_cum=df_diff_action.sort_values(['Date']).reset_index(drop=True)
        df_diff_action_cum["cum_sale"]=df_diff_action_cum.groupby(['Type'])['Diffusion_name'].cumsum(axis=0)
        
        figAction = px.bar(df_diff_action, x="Date", y="Diffusion_name", color="Type", color_discrete_sequence= px.colors.qualitative.Dark24)

        figAction.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre d'actions réalisées",)
        figAction.update_traces(hovertemplate = "Mois de la réalisation de l'action : en %{x}<br>Nbre d'actions réalisées: %{value}")

        dt_all = pd.date_range(start=df_diff_action['Date'].iloc[0],end=df_diff_action['Date'].iloc[-1])
        dt_obs = [d.strftime("%Y-%m") for d in pd.to_datetime(df_diff_action['Date'])]
        dt_breaks = [d for d in dt_all.strftime("%Y-%m").tolist() if not d in dt_obs]

        figAction.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
        figAction.update_layout(legend=dict(orientation="h"))

        st.plotly_chart(figAction, use_container_width=True)


        expander = st.expander("Nombre d'actions de diffusion (en cumulé)")

        figActionCum = px.bar(df_diff_action_cum, x="Date", y="cum_sale", color="Type", color_discrete_sequence= px.colors.qualitative.Dark24)


        figActionCum.update_layout(xaxis=dict(tickformat="%B %Y"), xaxis_title="", yaxis_title="Nombre d'actions réalisées",)
        figActionCum.update_traces(hovertemplate = "Mois de la réalisation de l'action : en %{x}<br>Nbre d'actions réalisées: %{value}")

        dt_all = pd.date_range(start=df_diff_action_cum['Date'].iloc[0],end=df_diff_action_cum['Date'].iloc[-1])
        dt_obs = [d.strftime("%Y-%m") for d in pd.to_datetime(df_diff_action_cum['Date'])]
        dt_breaks = [d for d in dt_all.strftime("%Y-%m").tolist() if not d in dt_obs]

        figActionCum.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
        figActionCum.update_layout(legend=dict(orientation="h"))

        expander.plotly_chart(figActionCum, use_container_width=True)

    st.markdown("### **Nombre fiches sensibilisées au moins une fois**")

    if categorie != "- Indre (36)" and categorie != "Centre-Val-de-Loire":
        df_diff_fiches = df_diff[['Fiches']]
        df_diff_fiches = df_diff_fiches["Fiches"].str.split("," , expand=True)

        n = 0
        L = []
        for n in range(len(df_diff_fiches.columns)-1):
            L.extend(df_diff_fiches[n].tolist())
        L = [x for x in L if x is not None]
            
        df_sensi_nb = pd.DataFrame(L)
        df_sensi_nb.dropna(inplace=True)
        df_sensi_nb.reset_index(inplace=True)
        if 0 in df_sensi_nb.columns.to_list():  
            df_sensi_nb[0].drop_duplicates(inplace=True)
        else:
            df_sensi_nb = df_diff_fiches


        col1, col2 = st.columns(2)

        if 0 in df_sensi_nb.columns.to_list():

            html_string_c = f"""<br>
            <center><font face='Helvetica' size='7'>{df_sensi_nb[0].count()}</font>
            <br/><font size='3'>Nombre de fiches sensibilisées au moins une fois<br></font></center>
            """

            col1.markdown(html_string_c, unsafe_allow_html=True)

        else:

            html_string_c = f"""<br>
            <center><font face='Helvetica' size='7'>{round((df_sensi_nb[0].count() / df_fiche_serv_on_off[df_fiche_serv_on_off.statut != 0].statut.count())*100, 2)}%</font>
            <br/><font size='3'>Nombre de fiches sensibilisées au moins une fois<br></font></center>
            """

            col1.markdown(html_string_c, unsafe_allow_html=True)

        if not df_fiches_total.empty and 0 in df_sensi_nb.columns.to_list():

            html_string_d = f"""<br>
            """


            html_string_d = f"""<br>
            <center><font face='Helvetica' size='7'>{round((df_sensi_nb[0].count() / df_fiche_serv_on_off[df_fiche_serv_on_off.statut != 0].statut.count())*100, 2)}%</font>
            <br/><font size='3'>Pourcentage de fiches sensibilisées au moins une fois<br></font></center>
            """
    
            col2.markdown(html_string_d, unsafe_allow_html=True)


    # Nombre d'acteurs réalisant d'autres guides qui sont connectés à nos données ou avec lesquels il y a un partenariat
    st.markdown("### **Nombre d'acteurs réalisant d'autres guides qui sont connectés à nos données ou avec lesquels il y a un partenariat**")

    html_string_z = f"""<br>
    <center><font face='Helvetica' size='7'>{df_listing_count_vf.Etat.count()}</font>
    <br/><font size='3'>acteurs partenaires réalisant d'autres guides<br></font></center>
    """
  
    st.markdown(html_string_z, unsafe_allow_html=True)

# Nb d'hébergeurs disponibles

    st.markdown("### **MPLI : Nombre d'hébergeurs disponibles**")

    figHebDispo = go.Figure(data=[
        go.Line(name='Nombre d\'hébrgement diponibles', x=df_hebergeurs_dispo_final.index.astype(str), y=df_hebergeurs_dispo_final.Total, marker_color='#7201a8',
                text=df_hebergeurs_dispo_final.Total,
                textposition='top center',
                mode='lines+markers+text')   
    ])

    figHebDispo.update_xaxes(title_text="Mois où l'hébergement est disponible", title_font_family="Times New Roman")
    figHebDispo.update_yaxes(title_text="Nombre d'hébergements disponibles", title_font_family="Times New Roman")

    annotationsHebDispo = dict(xref='paper', yref='paper', x=0.055, y=1,
                                xanchor='center', yanchor='top',
                                text='Fait le: ' + str("1 janvier 2022"),
                                font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                                showarrow=False)

                           
    figHebDispo.update_layout(xaxis=dict(tickformat="%B %Y"))
    figHebDispo.update_layout(hovermode="x unified", title_font_family="Times New Roman", annotations=[annotationsHebDispo])
    figHebDispo.update_layout(legend=dict(orientation="h"))

    st.plotly_chart(figHebDispo, use_container_width=True)

# Nb d'hébergements

    st.markdown("### **MPLI : Nombre d'hébergements en cours**")

    figHeb = go.Figure(data=[
        go.Line(name='Nombre d\'hébrgement diponibles', x=df_hebergement_final.index.astype(str), y=df_hebergement_final.Total, marker_color='#7201a8',
                text=df_hebergement_final.Total,
                textposition='top center',
                mode='lines+markers+text')   
    ])

    figHeb.update_xaxes(title_text="Mois où l'hébergement est disponible", title_font_family="Times New Roman")
    figHeb.update_yaxes(title_text="Nombre d'hébergements disponibles", title_font_family="Times New Roman")

    annotationsHeb = dict(xref='paper', yref='paper', x=0.055, y=1,
                                xanchor='center', yanchor='top',
                                text='Fait le: ' + str("1 janvier 2022"),
                                font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                                showarrow=False)

                           
    figHeb.update_layout(xaxis=dict(tickformat="%B %Y"))
    figHeb.update_layout(hovermode="x unified", title_font_family="Times New Roman", annotations=[annotationsHeb])
    figHeb.update_layout(legend=dict(orientation="h"))

    st.plotly_chart(figHeb, use_container_width=True)

    st.markdown("### **MPLI : Nombre d'hébergées en recherche**")
    st.markdown("Aucun hébergées en recherche enregistrées sur ce territoire")

    st.markdown("### **MPLI : Nombre de nuitées d'hébergements**")

    df_nuité = df_hebergement[['Date début','Date fin']]
    df_nuité["Date début"] = pd.to_datetime(df_nuité["Date début"])
    df_nuité["Date fin"] = pd.to_datetime(df_nuité["Date fin"])

    df_nuité["Date début"] = df_nuité["Date début"] .dt.strftime('%Y-%m-%d')
    df_nuité["Date fin"] = df_nuité["Date fin"] .dt.strftime('%Y-%m-%d')

    df_nuité["Date début"] = pd.to_datetime(df_nuité["Date début"])
    df_nuité["Date fin"] = pd.to_datetime(df_nuité["Date fin"])

    df_nuité['Date fin'].fillna(today, inplace=True)


    if not df_nuité.empty:

        res = df_nuité.join(
        df_nuité.apply(lambda v: pd.Series(pd.date_range(v['Date début'], v['Date fin'], freq='D').to_period('M')), axis=1)
        .apply(pd.value_counts, axis=1)
        .fillna(0)
        .astype(int))

        res_vf = res.drop(columns=res.iloc[:,0:2])
        res_vf.index = res_vf.index.astype(str)
        res_vf.loc['Total']= res_vf.sum()
        res_vf = res_vf.tail(1)

        res_vf_2 = res_vf.transpose()
        res_vf_2 = res_vf_2.sort_index()
        res_vf_2.reset_index(inplace=True)
        res_vf_2.rename(columns={'index':'Date'}, inplace=True)

        figNuité = go.Figure(data=[
        go.Line(name='nombre de nuitées', x=res_vf_2.Date.astype(str), y=res_vf_2.Total, marker_color='#7201a8',
            text=res_vf_2.Total,
            textposition='top center',
            mode='lines+markers+text')   
        ])


        figNuité.update_xaxes(title_text="", title_font_family="Times New Roman")
        figNuité.update_yaxes(title_text="Nombre de nuitées d'hébergements", title_font_family="Times New Roman")

        annotationsHeb = dict(xref='paper', yref='paper', x=0.055, y=1,
                                    xanchor='center', yanchor='top',
                                    text='Fait le: ' + str("1 janvier 2022"),
                                    font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                    showarrow=False)

                            
        figNuité.update_layout(xaxis=dict(tickformat="%B %Y"))
        figNuité.update_layout(hovermode="x unified", title_font_family="Times New Roman", annotations=[annotationsHeb])
        figNuité.update_layout(legend=dict(orientation="h"))


        st.plotly_chart(figNuité, use_container_width=True)

    else:
        st.markdown("Aucune nuité enregistrée sur ce territoire")

    st.markdown("### **Pourcentage de fiches mises à jour dans les 6 derniers mois**")

    if not categorie.startswith("-"):

        html_string_k = f"""<br>
        <center><font face='Helvetica' size='6'>{df_maj_6_months.loc['Total','pourcentage']} %</font>
        <br/><font size='3'>des fiches ont été mise à jours au moins une fois pendant les 6 derniers mois<br></font></center>"
        """

        st.markdown(html_string_k, unsafe_allow_html=True)

    if categorie.startswith("-"):

        html_string_k = f"""<br>
        <center><font face='Helvetica' size='6'>{df_maj_6_months.loc[cat_dict[categorie],'pourcentage']} %</font>
        <br/><font size='3'>des fiches ont été mise à jours au moins une fois pendant les 6 derniers mois<br></font></center>"
        """

        st.markdown(html_string_k, unsafe_allow_html=True)


    st.markdown("### **Nombre de fiches et de services en ligne et en brouillon**")

    #df_fiche_serv_on_off = df_fiche_serv_on_off[df_fiche_serv_on_off.statut != 0]
    
    col1, col2 = st.columns(2)

    html_string_l = f"""<br>
    <center><font face='Helvetica' size='7'>{df_fiche_serv_on_off[df_fiche_serv_on_off.statut != 0].statut.count()}</font>
    <br/><font size='3'>Nombre de fiches en ligne<br></font></center>
    """

    col1.markdown(html_string_l, unsafe_allow_html=True)

    html_string_m = f"""<br>
    <center><font face='Helvetica' size='7'>{df_fiche_serv_on_off[df_fiche_serv_on_off.statut == 0].statut.count()}</font>
    <br/><font size='3'>Nombre de fiches en brouillon<br></font></center>
    """

    col2.markdown(html_string_m, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    html_string_n = f"""<br>
    <center><font face='Helvetica' size='7'>{df_fiche_serv_on_off[df_fiche_serv_on_off.statut != 0].Nb_services.sum()}</font>
    <br/><font size='3'>Nombre de services en ligne<br></font></center>
    """

    col1.markdown(html_string_n, unsafe_allow_html=True)

    html_string_o = f"""<br>
    <center><font face='Helvetica' size='7'>{df_fiche_serv_on_off[df_fiche_serv_on_off.statut == 0].Nb_services.sum()}</font>
    <br/><font size='3'>Nombre de services en brouillon<br></font></center>
    """

    col2.markdown(html_string_o, unsafe_allow_html=True)

    st.markdown("### **Nombre de fiches par communes**")

    list_ville = list(dict.fromkeys(df_ville_vf.ville.to_list()))
    list_ville.insert(0, "")

    test = st.selectbox("Selctionnez une commune :", list_ville)

    if test == "":
        st.write(df_ville_vf)

    else:
        st.write(df_ville_vf[df_ville_vf.ville == test])


    st.markdown("### **Nombre de fiches par type de service**")
    st.markdown("*Pour pouvoir visualiser le nombre de fiches pour un service en particulier, double_cliqué sur le service dans le légende.*")
    st.markdown("**Attention**: si une structure propose plusieurs services, elles sera comptabilisée 1 fois par service dans ce graphique")

    df_categorie_per_month = df_categorie_vf.groupby(['createdAt','categorie']).count().reset_index()
    df_categorie_per_month = df_categorie_per_month.iloc[:,:3]
    df_categorie_per_month.rename(columns={"Unnamed: 0":'Nombre_de_fiches'}, inplace=True)

    df_categorie_per_month["nbre_fiches_cum"]=df_categorie_per_month.groupby(['categorie'])['Nombre_de_fiches'].cumsum(axis=0)

    figServiceFiches = px.bar(df_categorie_per_month, x="createdAt", y="Nombre_de_fiches", color="categorie", 
             color_discrete_sequence= px.colors.qualitative.Dark24, )

    figServiceFiches.update_yaxes(title_text="Nombre de fiches en ligne par type de service", title_font_family="Times New Roman")
    figServiceFiches.update_xaxes(title_text="", title_font_family="Times New Roman")

    annotationsServFiches = dict(xref='paper', yref='paper', x=0.055, y=1,
                                    xanchor='center', yanchor='top',
                                    text='Fait le: ' + str("1 janvier 2022"),
                                    font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                    showarrow=False)

                            
    figServiceFiches.update_layout(xaxis=dict(tickformat="%B %Y"))
    figServiceFiches.update_traces(hovertemplate = "Mois de création des fiches : %{x}<br>Nbre de fiches: %{y}")
    figServiceFiches.update_layout(legend={'title_text':'Types de service'})
    figServiceFiches.update_layout(legend=dict(orientation="h"))

    st.plotly_chart(figServiceFiches, use_container_width=True)

    

    expander = st.expander("Nombre de fiches par type de service (en cumulé)")
    expander.markdown("*Lorsque vous double-cliquez sur un type de service dans la légende le nombre qui apparait est le nombre total de fiches en ligne avec proposant ce service*")

    figServiceFichesCum = px.bar(df_categorie_per_month, x="createdAt", y="nbre_fiches_cum", color="categorie", 
             color_discrete_sequence= px.colors.qualitative.Dark24, )

    figServiceFichesCum.update_yaxes(title_text="Nombre de fiches en ligne par type de service", title_font_family="Times New Roman")
    figServiceFichesCum.update_xaxes(title_text="Mois de création de la fiche", title_font_family="Times New Roman")
    annotationsServFichesCum = dict(xref='paper', yref='paper', x=0.055, y=1,
                                    xanchor='center', yanchor='top',
                                    text='Fait le: ' + str("1 janvier 2022"),
                                    font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                    showarrow=False)

                            
    figServiceFichesCum.update_layout(xaxis=dict(tickformat="%B %Y"))
    figServiceFichesCum.update_traces(hovertemplate = "Mois de création des fiches : %{x}<br>Nbre de fiches: %{y}")
    figServiceFichesCum.update_layout(legend={'title_text':'Types de service'}, width=100)
    figServiceFichesCum.update_layout(legend=dict(orientation="h"))   

    expander.plotly_chart(figServiceFichesCum, use_container_width=True)
    
    
if categorie_2 == 'Communication':
    
# Newsletter


    st.markdown("### **Nombre de lecteurs de la newsletter, de clics**")

    col1, col2 = st.columns(2)

    html_string_e = f"""<br>
    <center><font face='Helvetica' size='7'>{df_newsletter.loc[:,'Opened'].sum()}</font>
    <br/><font size='3'>Nombre de newsletters cliquées<br></font></center>
    """

    col1.markdown(html_string_e, unsafe_allow_html=True)

    html_string_f = f"""<br>
    <center><font face='Helvetica' size='7'>{df_newsletter.loc[:,'Clicked'].sum()}</font>
    <br/><font size='3'>Nombre de newsletters ouvertes<br></font></center>
    """

    col2.markdown(html_string_f, unsafe_allow_html=True)


    col1, col2 = st.columns(2)

    if categorie.startswith("-"):

        html_string_g = f"""<br>
        <center><font face='Helvetica' size='7'>{df_newsletter.loc[0,'Tx ouverture']}%</font>
        <br/><font size='3'>Pourcentage de newsletters ouvertes <br>(par rapport aux newsletters envoyées)<br></font></center>
        """

        col1.markdown(html_string_g, unsafe_allow_html=True)

        html_string_h = f"""<br>
        <center><font face='Helvetica' size='7'>{df_newsletter.loc[0,'Tx clic']}%</font>
        <br/><font size='3'>Pourcentage de newsletters cliquées <br>(par rapport aux newsletters ouvertes)<br></font></center>
        """

        col2.markdown(html_string_h, unsafe_allow_html=True)

    else:

        html_string_g = f"""<br>
        <center><font face='Helvetica' size='7'>{round((df_newsletter_2.Opened / df_newsletter_2.Sent)*100,2)}%</font>
        <br/><font size='3'>Pourcentage de newsletters ouvertes <br>(par rapport aux newsletters envoyées)<br></font></center>
        """

        col1.markdown(html_string_g, unsafe_allow_html=True)

        html_string_h = f"""<br>
        <center><font face='Helvetica' size='7'>{round((df_newsletter_2.Clicked / df_newsletter_2.Opened)*100,2)}%</font>
        <br/><font size='3'>Pourcentage de newsletters cliquées <br>(par rapport aux newsletters ouvertes)<br></font></center>
        """

        col2.markdown(html_string_h, unsafe_allow_html=True)


    st.markdown("### **Nombre de partenariats départementaux**")


if categorie_2 == 'Lancement':

    st.markdown("### **Pourcentage d'exhaustivité des territoire**")


    expander = st.expander("Définition et calcul")
    expander.write("""Le pourcentage d'exhaustivité des territoires est basé sur le nombre de types de services référencés sur chaque territoire.  
    En utilisant le nombre de services référencé dans les territoire les plus ancien (33 - 44 - 75 - 92 - 93), et en prenant en compte d'autre variable 
    comme le taux de pauvreté, le nombre d'habitant ou la superficie, nous avons déterminé le nombre de strucutures par type de services que nous devrions atteindre""")

    if categorie.startswith("-"):

        html_string_p = f"""<br>
        <center><font face='Helvetica' size='7'>{df_exhaustivity.loc[0,'Moyenne']}%</font>
        <br/><font size='3'>Pourcentage d'exhaustivité du territoire<br></font></center><br>
        """

        st.markdown(html_string_p, unsafe_allow_html=True)

    else:

        html_string_q = f"""<br>
        <center><font face='Helvetica' size='7'>{round(df_exhaustivity.Moyenne.mean(),2)}%</font>
        <br/><font size='3'>Moyenne des pourcentages d'exhaustivité des territoires<br><br>
        """

        st.markdown(html_string_q, unsafe_allow_html=True)


    expander = st.expander("Tableau des données pour chaque type de service")

    df_exhaustivity = df_exhaustivity.loc[:,"Département":]

    m = 2
    while m < 57:
        df_exhaustivity.iloc[:,m] = df_exhaustivity.iloc[:,m].astype(str) + ' %'
        m += 1

    expander.write(df_exhaustivity)

   
if categorie_2 == 'Admin/Finance':

    st.markdown("### **Nombre de rendez-vous de prospection**")

    df_prospection_vf = df_prospection_vf.sort_values(by='Nombre de rdv', ascending = True)

    figProspection = go.Figure(data=[
    go.Bar(name="Prospection", y=df_prospection_vf['Departement'], x=df_prospection_vf["Nombre de rdv"], marker_color='#7201a8', orientation="h"),
    ])

    figProspection.update_yaxes(title_text="", title_font_family="Times New Roman")
    figProspection.update_xaxes(title_text="Nombre de rdv de prospections réalisés", title_font_family="Times New Roman")
                            
    figProspection.update_traces(hovertemplate = "Département: %{y}<br>Nombre de rdv de prospection : %{x}")


    st.plotly_chart(figProspection, use_container_width=True)


    html_string_r = f"""<br>
    <center><font face='Helvetica' size='7'>{df_prospection_vf["Nombre de rdv"].sum()}</font>
    <br/><font size='3'>Nombre total de rendez-vous de prospection réalisés<br><br>
    """

    st.markdown(html_string_r, unsafe_allow_html=True)


    st.markdown("### **Nombre d'instances de co-construction au niveau régional**")

    df_co_const = df_diff[(df_diff['Type'] == "Coop") | (df_diff['Type'] == "Copil")]
    df_co_const = df_co_const[['Date','Territoire','Type']]
    df_co_const['Date'] = pd.to_datetime(df_co_const['Date'])
        
    table = pd.pivot_table(df_co_const, values='Type', index=['Territoire'],
                        columns=['Date'], aggfunc='count')

    table = table.groupby(pd.PeriodIndex(table.columns, freq='Q'), axis=1).count()
    table.reset_index(inplace = True)

    table.loc[17] = table.iloc[0:1].sum()
    table.loc[17,'Territoire'] = 'Alpes-Maritime'

    table.loc[18] = table.loc[2] + table.loc[6]
    table.loc[18,'Territoire'] = 'Auvergne-Rhône-Alpes'

    table.loc[19] = table.loc[3]
    table.loc[19,'Territoire'] = 'Nouvelle-Aquitaine'

    table.loc[20] = table.loc[4]
    table.loc[20,'Territoire'] = 'Centre-Val-de-Loire'

    table.loc[21] = table.loc[5]
    table.loc[21,'Territoire'] = 'Pays-de-la-Loire'

    table.loc[22] = table.loc[7]
    table.loc[22,'Territoire'] = 'Grand-Est'

    table.loc[23] = table.loc[8] + table.loc[10] + table.loc[11] + table.loc[12] + table.loc[13]  + table.loc[14] + table.loc[15] + table.loc[16]
    table.loc[23,'Territoire'] = 'Ile-de-France'

    table.loc[24] = table.loc[10]
    table.loc[24,'Territoire'] = 'Normandie'

    df_co_const_vf = table.loc[17:].reset_index()


    df_co_const_vf = df_co_const_vf.T.reset_index()
    df_co_const_vf.columns = df_co_const_vf.iloc[1]
    df_co_const_final = df_co_const_vf.drop(index=[1,0])

    df_co_const_final.reset_index(inplace=True)

    df_co_const_final.drop(columns="index", inplace=True)
    df_co_const_final['Territoire'] = df_co_const_final.Territoire.astype(str)

    figCo_const = go.Figure(data=[
        go.Bar(name="Alpes-Maritimes", y=df_co_const_final['Alpes-Maritime'], x=df_co_const_final["Territoire"],marker_color='#7201a8'),
        go.Bar(name="Auvergne-Rhône-Alpes", y=df_co_const_final['Auvergne-Rhône-Alpes'], x=df_co_const_final["Territoire"],marker_color='#E65A46',),
        go.Bar(name="Nouvelle-Aquitaine", y=df_co_const_final['Nouvelle-Aquitaine'], x=df_co_const_final["Territoire"],marker_color='#3E3A71',),
        go.Bar(name="Centre-Val-de-Loire", y=df_co_const_final['Centre-Val-de-Loire'], x=df_co_const_final["Territoire"],marker_color='#2896A0',),
        go.Bar(name="Pays-de-la-Loire", y=df_co_const_final['Pays-de-la-Loire'], x=df_co_const_final["Territoire"],marker_color='#231E3C',),
        go.Bar(name="Grand-Est", y=df_co_const_final['Grand-Est'], x=df_co_const_final["Territoire"],marker_color="#258a63"),
        go.Bar(name="Ile-de-France", y=df_co_const_final['Ile-de-France'], x=df_co_const_final["Territoire"],marker_color="#c9a0dc"),
        go.Bar(name="Normandie", y=df_co_const_final['Normandie'], x=df_co_const_final["Territoire"],),
        ])

    figCo_const.update_layout(barmode='stack')

    st.plotly_chart(figCo_const, use_container_width=True)
