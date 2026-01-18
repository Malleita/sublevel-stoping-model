#prueba
import math
import random
import gurobipy as gp
from gurobipy import GRB


m = gp.Model("obj_ejemplo")

cas = 1   #caserones +1
sub_c = 3   #subcaserones +1
#Parametros manuales en este caso para un caseron de 3 sub

#======= CONJUNTOS ==========

#caserones
C = range(cas) 
#subcaserones
S = {c: range(sub_c) for c in C}
#ultimo de los subcaserones
US = {c: range(sub_c -1, sub_c) for c in C}
#chimeneas del caseron c
CH = {c: range(sub_c) for c in C}
#presedencias
P_c = {
    1: None,
    2: 1, 
    3: 2
}
#galerias, tipo 1 y tipo dos
G_1 = {c: range(sub_c) for c in C}
G_2 = {c: range(sub_c) for c in C}
#Bateas
B = {c: range(sub_c) for c in C}
#Bateas del subcaseron c
SB_c = range(sub_c)
#tipo de drill
Dr = range(3)
#Conjunto de maquinarias
I_h = range(1) #perforadoras verticales
I_u = range(1,2) #perforadoras radiales
I_d = range(2,3)
I_c = range(3,4)
I_val = 4
J_val = 1
K_val = 1
I = range(I_val)
J = range(J_val) 
K = range(K_val)
#Periodos
T = range(15)

#======= PARAMETROS ======
for k in C:
    Mass_drill = {
        c: random.randint(1,5)
        for c in S[k]
    }
    Mass_blast = {
        c: random.randint(1,5)
        for c in S[k]
    }
    Mass_extr = {
        c: random.randint(1,5)
        for c in S[k]
    }
Lambda = {
    "i": 1.0,
    "j": 1.0,
    "k": 1.0
}

#duracion del periodo
T_t = {
    t: 8
    for t in T
}


#======= Variables ======
for k in C:
    #------------------------
    # #(x esta en orden sub-caseron, tiempo, tipo de drill)
    x = m.addVars(S[k], T, Dr,vtype=GRB.BINARY,name="x")
    y = m.addVars(S[k], T,vtype=GRB.BINARY,name="y")
    z = m.addVars(S[k], T,vtype=GRB.BINARY,name="z")
    #------------------------
    x_bar = m.addVars(S[k], T, Dr,vtype=GRB.BINARY,name="x_bar")
    y_bar = m.addVars(S[k], T,vtype=GRB.BINARY,name="y_bar")
    z_bar = m.addVars(S[k], T,vtype=GRB.BINARY,name="z_bar")
    #------------------------
    x_hat = m.addVars(I, S[k], T, Dr,vtype=GRB.CONTINUOUS,lb=0,ub=1,name="x_hat")
    y_hat = m.addVars(J, S[k], T,vtype=GRB.CONTINUOUS,lb=0,ub=1,name="y_hat")
    z_hat = m.addVars(K, S[k], T,vtype=GRB.CONTINUOUS,lb=0,ub=1,name="z_hat")

#=========== restricciones ============

#---- tiempo ------

for i in I_h:
    for t in T:
        for n in C:
            m.addConstr(
                gp.quicksum(x_hat[i,g,t,0] for g in G_1[n]) <= T_t[t] * Lambda["i"]
            )

for i in I_h:
    for t in T:
        for n in C:
            m.addConstr(
                gp.quicksum(x_hat[i,g,t,0] for g in G_2[n]) <= T_t[t] * Lambda["i"]
            )

for j in J:
    for t in T:
        for n in C:
            m.addConstr(
            gp.quicksum(y_hat[j,g,t] for g in G_1[n]) <= T_t[t] * Lambda["j"]
        )

for j in J:
    for t in T:
        for c in C:
            m.addConstr(
                gp.quicksum(y_hat[j,g,t] for g in G_2[c]) <= T_t[t] * Lambda["j"]
            )

for k in K:
    for t in T:
        for c in C:
            m.addConstr(
                gp.quicksum(z_hat[k,g,t] for g in G_1[c]) <= T_t[t] * Lambda["k"]
            )

for k in K:
    for t in T:
        for c in C:
            m.addConstr(
                gp.quicksum(z_hat[k,g,t] for g in G_2[c]) <= T_t[t] * Lambda["k"]
            )

for i in I_d:
    for t in T:
        for n in C:
            m.addConstr(
                gp.quicksum(x_hat[i,c,t,1] for c in S[n]) <= T_t[t] * Lambda["i"]
            )

for j in J:
    for t in T:
        for n in C:
            m.addConstr(
                gp.quicksum(y_hat[j,c,t] for c in S[n]) <= T_t[t] * Lambda["j"]
            )

for k in K:
    for t in T:
        for n in C:
            m.addConstr(
                gp.quicksum(y_hat[j,c,t] for c in S[n]) <= T_t[t] * Lambda["j"]
            )

for c in C:
    for t in T:
        m.addConstr((gp.quicksum(
            T_t[t] * (
                gp.quicksum(x_hat[i,m,t,0] for i in I_h) +
                gp.quicksum(y_hat[j,m,t]   for j in J)   +
                gp.quicksum(z_hat[k,m,t]   for k in K)
            )
            for m in G_1(c)
        ) + 
        gp.quicksum(
            T_t[t] * (
                gp.quicksum(x_hat[i,n,t,0] for i in I_h) +
                gp.quicksum(y_hat[j,n,t]   for j in J)   +
                gp.quicksum(z_hat[k,n,t]   for k in K)
            )
            for n in G_2(c)
        ) +
        gp.quicksum(
            T_t[t] * (
                gp.quicksum(x_hat[i,nu,t,2] for i in I_h) +
                gp.quicksum(y_hat[j,nu,t]   for j in J)   +
                gp.quicksum(z_hat[k,nu,t]   for k in K)
            )
            for nu in S[c]
        ) +
        gp.quicksum(
            T_t[t] * (
                gp.quicksum(x_hat[i,b,t,2] for i in I_h) +
                gp.quicksum(y_hat[j,b,t]   for j in J)   +
                gp.quicksum(z_hat[k,b,t]   for k in K)
            )
            for b in B[c]
        ) +
        gp.quicksum(
            T_t[t] * (
                gp.quicksum(x_hat[i,l,t,2] for i in I_h) +
                gp.quicksum(y_hat[j,l,t]   for j in J)   +
                gp.quicksum(z_hat[k,l,t]   for k in K)
            )
            for l in CH[c]
        ))
        <= T_t[t]
        ) 

#---- Progreso acumulado ------

for n in C:
    for nu in S[n]:
        for c in G_1[nu]:
            for t in T:
                m.addConstr(
                    x_bar[c,t,0]*Mass_drill[c] <= gp.quicksum(x_hat[i,c,tau,0] * T_t[tau] for i in I_h for tau in range(0,t+1))
                )

for n in C:
    for nu in S[n]:
        for c in G_2[nu]:
            for t in T:
                m.addConstr(
                    x_bar[c,t,0]*Mass_drill[c] <= gp.quicksum(x_hat[i,c,tau,0] * T_t[tau] for i in I_h for tau in range(0,t+1))
                )

for n in C:
    for nu in S[n]:
        for c in G_1[nu]:
            for t in T:
                m.addConstr(
                    y_bar[c,t]*Mass_blast[c] <= gp.quicksum(y_hat[j,c,tau] * T_t[tau] for j in J for tau in range(0,t+1))
                )

for n in C:
    for nu in S[n]:
        for c in G_2[nu]:
            for t in T:
                m.addConstr(
                    y_bar[c,t]*Mass_blast[c] <= gp.quicksum(y_hat[j,c,tau] * T_t[tau] for j in J for tau in range(0,t+1))
                )

for n in C:
    for nu in S[n]:
        for c in G_1[nu]:
            for t in T:
                m.addConstr(
                    z_bar[c,t]*Mass_extr[c] <= gp.quicksum(z_hat[k,c,tau] * T_t[tau] for k in K for tau in range(0,t+1))
                )

for n in C:
    for c in S[n]:
        for t in T:
            m.addConstr(
                x_bar[c,t,2] * Mass_drill[c] <= gp.quicksum(x_hat[i,c,tau,2] * T_t[tau] for i in I_d for tau in range(0,t+1))
            )

for n in C:
    for c in S[n]:
        for t in T:
            m.addConstr(
                y_bar[c,t] * Mass_blast[c] <= gp.quicksum(y_hat[j,c,tau] * T_t[tau] for j in J for tau in range(0,t+1))
            )

for n in C:
    for c in S[n]:
        for t in T:
            m.addConstr(
                z_bar[c,t] * Mass_extr[c] <= gp.quicksum(z_hat[k,c,tau] * T_t[tau] for k in K for tau in range(0,t+1))
            )

#---- Restricciones de vinculo y finalizacion ------

# Esta muy rara la notacion por el S_n
for n in C:
    for c in G_1[n]:
        m.addConstr(
            1 == gp.quicksum(x[c,t,0]) for t in T
        )

for n in C:
    for c in G_2[n]:
        m.addConstr(
            1 == gp.quicksum(x[c,t,0]) for t in T
        )

for n in C:
    for c in G_1[n]:
        m.addConstr(
            1 == gp.quicksum(y[c,t]) for t in T
        )

for n in C:
    for c in G_1[n]:
        m.addConstr(
            1 == gp.quicksum(y[c,t]) for t in T
        )

for n in C:
    for c in G_1[n]:
        m.addConstr(
            1 == gp.quicksum(z[c,t]) for t in T
        )

for n in C:
    for c in G_1[n]:
        m.addConstr(
            1 == gp.quicksum(z[c,t]) for t in T
        )

for n in C:
    for c in S[n]:
        m.addConstr(
            1 == gp.quicksum(x[c,t,2]) for t in T
        )

for n in C:
    for c in S[n]:
        m.addConstr(
            1 == gp.quicksum(y[c,t]) for t in T
        )

for n in C:
    for c in S[n]:
        m.addConstr(
            1 == gp.quicksum(z[c,t]) for t in T
        )

for n in C:
    for c in G_1[n]:
        for t in T:
            m.addConstr(
                x[c,t,0] <= x_bar[c,t,0]
            )

for n in C:
    for c in G_2[n]:
        for t in T:
            m.addConstr(
                x[c,t,0] <= x_bar[c,t,0]
            )

for n in C:
    for c in G_1[n]:
        for t in T:
            m.addConstr(
                y[c,t] <= y_bar[c,t]
            )

for n in C:
    for c in G_2[n]:
        for t in T:
            m.addConstr(
                y[c,t] <= y_bar[c,t]
            )

for n in C:
    for c in G_1[n]:
        for t in T:
            m.addConstr(
                z[c,t] <= z_bar[c,t]
            )

for n in C:
    for c in G_2[n]:
        for t in T:
            m.addConstr(
                z[c,t] <= z_bar[c,t]
            )

for n in C:
    for c in S[n]:
        for t in t:
            x[c,t,2] <= x_bar[c,t,2]

#estas creo que no son necesarias --------
for n in C:
    for c in S[n]:
        for t in t:
            y[c,t] <= y_bar[c,t]

for n in C:
    for c in S[n]:
        for t in t:
            z[c,t] <= z_bar[c,t]

