import pandas as pd
from io import StringIO
from matplotlib import pyplot as plt

TESTDATA=StringIO(""""s_betap1";"s_mikro1";"s_teafozo";"s_kavefozo";"s_mikro2";"s_bojler";"s_mikro3";"m_timestamp"
3.293888888888889;0.0;0.0;0.0;0.0;0.0;0.05277777777777778;1583362801000
3.323888888888889;0.0;0.017222222222222222;0.0;0.0;0.06277777777777778;0.0;1583363700000
3.3027777777777776;0.0;0.0;0.0;0.0;0.0;0.0;1583364600000
3.2469444444444444;0.0;0.0;2.777777777777778E-4;0.03333333333333333;0.006666666666666667;0.0;1583365500000
3.213888888888889;0.0;0.0;0.0;0.0;0.0;0.08611111111111111;1583366401000
3.236388888888889;0.0;0.0;0.0;0.0;0.010277777777777778;0.04805555555555555;1583367300000
3.243611111111111;0.0;0.0;0.0;0.0;0.0;0.0;1583368200000
3.227222222222222;0.0;0.0011111111111111111;0.085;0.0;0.0016666666666666668;0.0;1583369100000
3.211388888888889;0.0;0.0;0.0;0.0;0.0;0.0;1583370000000
3.21;0.0;0.0;0.0;0.0;0.0;0.020277777777777777;1583370900000
3.2355555555555555;0.0;2.777777777777778E-4;0.0;0.005555555555555556;0.0;0.0;1583371800000
3.2133333333333334;0.0;0.0;0.0;0.0;0.03861111111111111;0.0;1583372701000
3.243333333333333;0.0;0.0;0.03861111111111111;0.0;0.0;0.0011111111111111111;1583373600000
3.2483333333333335;0.0;0.0;0.0;0.016666666666666666;8.333333333333334E-4;0.0;1583374500000
3.229722222222222;0.0;0.0;0.0;0.0;0.0;0.0;1583375400000
3.2647222222222223;0.0;0.0;0.0;0.0;0.0;0.04611111111111111;1583376300000
3.2602777777777776;0.0;0.0;0.0;0.0;0.0;0.0;1583377200000
3.2630555555555554;0.0;0.0;0.0;0.003611111111111111;0.0;0.0;1583378101000
3.2908333333333335;0.0;0.0;0.0;0.0;0.0;0.0;1583379001000
3.2916666666666665;0.0;0.0;0.0;0.0;0.04722222222222222;0.015277777777777777;1583379901000
3.361111111111111;0.0;0.0;0.0;0.0;0.0;5.555555555555556E-4;1583380801000
3.3519444444444444;0.0;0.0;0.0;0.0;0.0;0.0;1583381700000
3.3275;0.0;0.0;0.0;0.0;0.0;0.0;1583382601000
3.3125;0.0;0.0;0.0;0.0;0.0;0.0;1583383501000
3.2808333333333333;0.0;0.08888888888888889;0.0;0.0275;0.0;0.0011111111111111111;1583384400000
3.385;0.0;0.0;0.08166666666666667;0.0;0.0044444444444444444;0.0;1583385301000
3.3675;0.0;0.0;0.0;0.0;0.0;0.0;1583386201000
57.54805555555556;0.0;0.06166666666666667;0.0;0.0;54.618611111111115;0.0;1583387100000
38.704166666666666;0.0;0.0;34.791666666666664;0.0;0.0;0.0;1583388000000
5.984444444444445;0.0;0.0;1.893888888888889;0.10055555555555555;0.09333333333333334;0.0;1583388900000
5.560555555555555;0.0;0.0033333333333333335;1.7491666666666668;0.26611111111111113;0.0;0.0;1583389801000
220.19833333333332;0.0;124.065;19.938333333333333;0.2608333333333333;75.93916666666667;0.0;1583390701000
166.36833333333334;0.0;31.323333333333334;1.8125;0.2633333333333333;132.1125;0.0;1583391600000
169.37305555555557;0.0;0.0;38.04333333333334;0.27055555555555555;134.86194444444445;0.0;1583392500000
244.22916666666666;0.0;0.0;13.195833333333333;0.27444444444444444;225.1677777777778;6.8533333333333335;1583393400000
226.5822222222222;0.0;0.0;57.63777777777778;0.25666666666666665;166.245;6.115833333333334;1583394300000
212.42138888888888;0.0;0.0;16.692777777777778;0.28805555555555556;157.2875;38.84305555555556;1583395200000
238.22555555555556;0.0;0.0;37.299166666666665;0.2783333333333333;204.13333333333333;0.0;1583396100000
233.285;0.0;0.0;19.864444444444445;0.2825;213.5088888888889;8.333333333333334E-4;1583397000000
56.9675;0.0;0.0;1.8441666666666667;0.2747222222222222;36.06805555555555;16.453055555555554;1583397900000
69.40666666666667;0.0;0.0;36.59111111111111;0.2786111111111111;30.685555555555556;0.0;1583398800000
281.53027777777777;0.0;0.0;71.85194444444444;0.2677777777777778;216.52916666666667;0.0;1583399700000
22.430555555555557;0.0;0.0;1.846111111111111;0.2841666666666667;16.34;0.010277777777777778;1583400600000
24.856666666666666;0.0;0.03388888888888889;21.55027777777778;0.27666666666666667;0.0;0.0;1583401500000
65.30611111111111;0.0;0.0;1.8505555555555555;0.28;61.129444444444445;0.0;1583402400000
136.60666666666665;0.0;56.22638888888889;1.9133333333333333;0.27166666666666667;75.715;0.0;1583403303000
155.94305555555556;0.0;78.34527777777778;1.62;0.2619444444444444;75.95361111111112;0.0;1583404200000
246.8125;83.91555555555556;15.024166666666666;23.552222222222223;31.182222222222222;93.8925;0.0;1583405100000
436.2463888888889;68.40388888888889;13.20861111111111;1.7819444444444446;27.785833333333333;252.82444444444445;72.10944444444445;1583406000000
538.9077777777778;65.42805555555556;4.829722222222222;19.471944444444443;40.78388888888889;284.5652777777778;129.39055555555555;1583406900000
440.0336111111111;34.05361111111111;0.0;30.6;27.818055555555556;353.86027777777775;0.0;1583407800000
98.13388888888889;38.700833333333335;0.0;1.825;0.28888888888888886;56.76555555555556;0.0;1583408700000
190.0438888888889;0.0;0.0;20.938055555555554;0.2708333333333333;168.79361111111112;0.007222222222222222;1583409600000
192.82944444444445;0.0;0.0;1.8219444444444444;63.878055555555555;89.46055555555556;35.05222222222222;1583410502000
295.56416666666667;0.0;0.0;29.106944444444444;0.27444444444444444;241.40722222222223;28.195833333333333;1583411401000
189.26111111111112;0.0;0.012777777777777779;21.208333333333332;0.2941666666666667;168.94;0.0;1583412300000
171.91583333333332;0.0;0.0;31.705277777777777;0.2902777777777778;139.25305555555556;0.07111111111111111;1583413200000
47.659444444444446;0.0;0.0;21.081666666666667;0.3080555555555556;23.964444444444446;0.0;1583414100000
53.03666666666667;0.0;0.0;1.8697222222222223;0.30527777777777776;47.308055555555555;0.0;1583415000000
49.97638888888889;0.0;0.024166666666666666;2.0547222222222223;0.2941666666666667;30.66611111111111;13.205;1583415900000
5.500555555555556;0.0;0.0;1.691111111111111;0.2961111111111111;0.0;0.0;1583416800000
102.20722222222223;0.0;0.0;1.6961111111111111;0.2947222222222222;97.37944444444445;0.0;1583417700000
83.74027777777778;0.0;0.0;36.38444444444445;0.31166666666666665;45.64527777777778;0.030833333333333334;1583418600000
62.67888888888889;0.0;0.0;9.592222222222222;0.30722222222222223;48.363055555555555;0.0;1583419500000
6.149444444444445;0.0;8.333333333333334E-4;2.1141666666666667;0.3061111111111111;0.0;0.034444444444444444;1583420400000
109.92611111111111;0.0;0.0;1.6808333333333334;0.3011111111111111;106.21333333333334;0.0;1583421301000
73.61666666666666;0.0;0.0;44.399166666666666;0.3030555555555556;27.688055555555554;0.025555555555555557;1583422200000
145.79361111111112;0.0;0.0;1.9294444444444445;0.2841666666666667;140.2602777777778;0.0;1583423100000
5.978611111111111;0.0;0.0;2.0052777777777777;0.30277777777777776;0.0;0.04527777777777778;1583424000000
5.535;0.0;0.010555555555555556;1.6958333333333333;0.2966666666666667;0.022222222222222223;0.0;1583424900000
5.567222222222222;0.0;0.0;1.6858333333333333;0.3025;0.0;0.035;1583425800000
5.553055555555556;0.0;0.043055555555555555;1.6655555555555555;0.2941666666666667;0.0;0.0;1583426700000
5.658611111111111;0.0;0.0;1.6888888888888889;0.2997222222222222;0.011111111111111112;0.0;1583427600000
5.691944444444444;0.0;0.0;1.695;0.29388888888888887;0.0;0.0;1583428500000
5.6875;0.0;0.0;1.6994444444444445;0.30944444444444447;0.0;0.0;1583429400000
128.63222222222223;0.0;0.0;1.6697222222222223;0.2941666666666667;123.57111111111111;0.028333333333333332;1583430300000
5.645;0.0;0.0;1.711111111111111;0.31166666666666665;0.0;0.0;1583431200000
64.72777777777777;0.0;0.0;1.7177777777777778;0.31;59.659166666666664;0.0;1583432100000
5.662222222222222;0.0;0.0;1.7208333333333334;0.32;0.0;0.0;1583433000000
5.551388888888889;0.0;0.0;1.6916666666666667;0.29444444444444445;0.017777777777777778;0.0;1583433900000
5.554722222222222;0.0;0.0;1.701111111111111;0.31222222222222223;0.0;0.0;1583434800000
5.562777777777778;0.0;0.0;1.7080555555555557;0.30194444444444446;0.050833333333333335;0.0;1583435700000
25.010277777777777;0.0;0.012777777777777779;1.7105555555555556;0.29833333333333334;21.31861111111111;0.0;1583436600000
5.641111111111111;0.0;0.0;1.7236111111111112;0.3005555555555556;0.0;0.006666666666666667;1583437500000
5.687777777777778;0.0;0.01;1.7327777777777778;0.30916666666666665;0.0025;0.0;1583438400000
5.6425;0.0275;0.0;1.7322222222222223;0.31555555555555553;0.0;0.0;1583439300000
5.562777777777778;0.0;0.0;1.7219444444444445;0.3175;0.043333333333333335;0.03777777777777778;1583440201000
5.5761111111111115;0.0;0.0;1.7361111111111112;0.32083333333333336;0.0;0.0;1583441100000
5.510277777777778;0.0;0.0;1.7327777777777778;0.32305555555555554;0.0;0.0;1583442001000
5.5075;0.0;0.0;1.7352777777777777;0.3219444444444444;0.0;0.0;1583442901000
5.5088888888888885;0.0;0.0;1.7425;0.32555555555555554;0.0;0.0016666666666666668;1583443801000
25.674722222222222;0.0;0.035277777777777776;1.741111111111111;0.31916666666666665;19.593055555555555;0.0;1583444701000
5.506944444444445;0.0;0.0;1.74;0.3313888888888889;0.0;0.005;1583445600000
5.481388888888889;0.0;0.0016666666666666668;1.7238888888888888;0.3075;0.0;0.0;1583446500000
5.517222222222222;0.009444444444444445;0.0;1.74;0.31805555555555554;0.0;0.013888888888888888;1583447400000
5.497222222222222;0.0;0.0;1.7316666666666667;0.31222222222222223;0.03638888888888889;0.0;1583448300000""")

df=pd.read_csv(TESTDATA,sep=";",header='infer')
df['m_timestamp']=pd.to_datetime(df['m_timestamp'],unit='ms')
#df.set_index('m_timestamp',inplace=True)
#ax=sns.barplot(data=df.T)

df2=pd.melt(df,id_vars=['m_timestamp'],value_vars=["s_betap1","s_mikro1","s_teafozo","s_kavefozo","s_mikro2","s_bojler","s_mikro3"])
#print(df2)
#ax=sns.barplot(x="m_timestamp",y="value",hue="variable",data=df2)
#plt.show()


import altair as alt

fomero = alt.selection_multi(fields=["s_betap1"])
almero= alt.selection_multi(fields=["s_mikro1","s_teafozo","s_kavefozo","s_mikro2","s_bojler","s_mikro3"])

base =  alt.Chart(df2).encode(
    x='m_timestamp')
bar=base.mark_bar().encode(
    x='m_timestamp',
    y='value',
    color='variable',
).transform_filter(
    almero
)

line = base.mark_line(color='red').encode(
  y='value'
).transform_filter(
    fomero
)

chart =(bar).properties(
    width=1000,
    height=1000
).interactive()
chart.show()
# load a simple dataset as a pandas DataFrame
# chart = alt.Chart(df2).mark_bar().encode(
#     x='m_timestamp',
#     y='value',
#     color='variable',
# ).properties(
#     width=1000,
#     height=1000
# ).interactive()
# chart.show()