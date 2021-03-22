import numpy as np
import matplotlib.pyplot as plt
import json,pandas
import squarify

#%% simplify 2019 data to rationalize comparison 

f='oec_tanzania_2019_h92.csv'
df=pandas.read_csv(f)
total_export = df['Trade Value'].sum() #total export in dollar
df.HS4=df.HS4.str.lower() #make string searchable
df.HS2=df.HS2.str.lower()

cat = pandas.read_csv('export1966.csv') #get 1966 data and export items/sector

other_minerals=df.loc[df.HS2.str.contains('salt'),'Trade Value'].sum()+ \
    df.loc[df.HS2.str.contains('inorganic'),'Trade Value'].sum()
# inorganic cheimcals, sulpher, salt, non-precious stone..etc

manufactured=df.loc[df.HS2.str.contains('machine'),'Trade Value'].sum()+ \
    df.loc[df.HS2.str.contains('apparel'),'Trade Value'].sum()+ \
        df.loc[df.HS2.str.contains('plastic'),'Trade Value'].sum()+ \
            df.loc[df.HS2.str.contains('glass'),'Trade Value'].sum()
# machinary, clothing apparel, plastic and glass

data_sim={'cotton':df.loc[df.HS4.str.contains('raw cotton'),'Trade Value'].sum(),\
          'coffee':df.loc[df.HS4.str.contains('coffee'),'Trade Value'].sum(),\
              'vegetable fibers':df.loc[df.HS2.str.contains('textile fibres'),'Trade Value'].sum(),\
                  'cloves':df.loc[df.HS4.str.contains('cloves'),'Trade Value'].sum(),\
                      'cashew and other nuts':df.loc[df.HS2.str.contains('fruit and nuts'),'Trade Value'].values[:2].sum(),\
                          'legume':df.loc[df.HS4.str.contains('legumes'),'Trade Value'].sum(),\
                              'petroleum':df.loc[df.HS4.str.contains('petrol'),'Trade Value'].values[:-1].sum(),\
                                  'gold':df.loc[df.HS4.str.contains('gold'),'Trade Value'].sum(),\
                                      'diamond':df.loc[df.HS4.str.contains('diamond'),'Trade Value'].sum(),\
                                          'precious stones':df.loc[df.HS4.str.contains('stones'),'Trade Value'].sum(),\
                                              'other minerals':other_minerals,\
                                                  'tobacco':df.loc[df.HS4.str.contains('raw tobacco'),'Trade Value'].sum(),\
                                                      'copper':df.loc[df.HS4.str.contains('raw copper'),'Trade Value'].sum(),\
                                                          'manufactured products':manufactured}
    
df2=pandas.DataFrame(list(data_sim.items()),columns=['export','value'])

# add simple sector category
df2['sector']='ag'
df2.loc[13,'sector']='ind'
df2.loc[(12,10,9,8,7),'sector']='min'
df2.loc[6,'sector']='oil'

# percentage
df2['percent']=df2.value/total_export*100

df2.to_csv('export2019.csv')

#%% treemap
sortcolor={'ag':'#BDD09F','min':'#DBCA69','ind':'#4E6172','misc':'#777777','oil':'#855723'}

f,ax=plt.subplots(1,2,figsize=(14,6))
files=['export1966.csv','export2019.csv']
t=['1966','2019']
t2=['25.5% GDP','6.8% GDP']

for i,x in enumerate(files):
    df=pandas.read_csv(x)
    df=df.append({'export':'miscellaneous','percent':100-sum(df.percent),'sector':'misc'},ignore_index=True)
    df=df.sort_values(['sector','percent'],ascending=False)
    df=df.replace(sortcolor)
    lab=[]
    for j in df.iterrows():
        lab.append(j[1].export.title()+' ('+str(round(j[1].percent,1))+'%)')
        # lab.append(j[1].export.title())
    s=squarify.plot(df.percent,color=df.sector,label=lab,ax=ax[i],bar_kwargs=dict(linewidth=2,edgecolor='w'))
    s.axis('off')
    s.set_title(t[i]+' ('+t2[i]+')')

plt.savefig('tanzania_export.jpg')

#%%
# j=json.load(open('tanzania_boundary.js'))
# bound=np.array(j['layers'][0]['paths'][0]['points'])
# x,y=bound[:,0]-min(bound[:,0]),max(bound[:,1])-bound[:,1]
# f,ax=plt.subplots(figsize=(6,6))
# plt.plot(x,y,'k-')
# ax.axis('off')

# plt.savefig('tanzania_boundary.pdf')



