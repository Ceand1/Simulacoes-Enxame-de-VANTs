import math as mt
b = 0.111
PROB_PH = 0.6
x = 50
y = 50
c1 = 0.045
c2 = 0.131
U = 6
vx1 = []
vy1 = []
vx2 = []
vy2 = []
#Calcula pm
def prop_pm(mb):
    return mt.exp((-b)*mb)
    
#calcula pv
def prob_pw(theta):
    return mt.exp(c1*U)*mt.exp(U*c2*(mt.cos(theta)-1))

#calcula p_queima
def pburn(map, theta):
    return PROB_PH*(1+map.p_veg)*(1+map.p_den)*map.p_m*(prob_pw(theta))
    
#Causa o efeito do vento
def efWind(map,x,y):
    if(U >= 5 and map[x][y+1].value == 2):
        map[x][y+1].value = 3
        vx1.append(x)
        vy1.append(y+1)
    
    if(U >= 6 and map[x][y+2].value == 2):
        map[x][y+2].value = 3
        vx1.append(x)
        vy1.append(y+2)

    if(U >= 6 and map[x-1][y+1].value == 2):
        map[x-1][y+1].value = 3
        vx1.append(x-1)
        vy1.append(y+1)

    if(U >= 6 and map[x+1][y+1].value == 2):
        map[x+1][y+1].value = 3
        vx1.append(x+1)
        vy1.append(y+1)
