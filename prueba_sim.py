#prueba
import math
import random
import gurobipy as gp
from gurobipy import GRB


m = gp.Model("obj_ejemplo")

cas = 1   #caserones +1
sub_c = 1   #subcaserones +1
#Parametros manuales en este caso para un caseron de 3 sub

#======= CONJUNTOS ==========
#actividades
Act = range(cas*4*sub_c)
#caserones
C = range(cas) 
#subcaserones
S = {c: range(sub_c*c,sub_c*(c+1)) for c in C}
#ultimo de los subcaserones
#US = {c: (3*(c+1) - 1) for c in C}
#chimeneas del caseron c
#CH = {c: range(sub_c) for c in C}
#presedencias
P_c = {
    0: None,
    1: 0, 
    2: 1
}
#galerias, tipo 1 y tipo dos
G_1 = {c : range(sub_c*(c+1),sub_c*(c+2)) for c in C}
G_2 = {c : range(sub_c*(c+2),sub_c*(c+3)) for c in C}
#Bateas
B = {c : range(sub_c*(c+3),sub_c*(c+4)) for c in C} #<-------Fijense que esto este cambiado
#Bateas del subcaseron c
SB_c = {n: list(B[n]) for n in C}
SB_of_sub = {}
for n in C:
    for idx, c_sub in enumerate(S[n]):
        SB_of_sub[c_sub] = SB_c[n][idx]
#tipo de drill
Dr = range(4)
#Conjunto de maquinarias
I_h = range(1) #perforadoras verticales
I_u = range(1,2) #perforadoras radiales
I_d = range(2,3)
I_c = range(3,4)
I_h_v = 1
I_u_v = 1
I_d_v = 1
I_c_v = 1
I_val = 4
J_val = 1
K_val = 1
I = range(I_val)
J = range(J_val) 
K = range(K_val)
#Periodos
time_l = 15
T = range(time_l)
range(1,time_l)
#======= PARAMETROS ======
Mass_drill = {c: random.randint(1,5) for n in C for c in S[n]}
Mass_blast = {c: random.randint(1,5) for n in C for c in S[n]}
Mass_extr  = {c: random.randint(1,5) for n in C for c in S[n]}

Lambda = {
    "i": 1.0,
    "j": 1.0,
    "k": 1.0
}
#Masa bateas

Mass_drill_B = {b: random.randint(1, 5) for n in C for b in B[n]}
Mass_blast_B = {b: random.randint(1, 5) for n in C for b in B[n]}
Mass_extr_B  = {b: random.randint(1, 5) for n in C for b in B[n]}

# Masas para galerías 
Mass_drill_G = {g: random.randint(1,5) for n in C for g in list(G_1[n]) + list(G_2[n])}
Mass_blast_G = {g: random.randint(1,5) for n in C for g in list(G_1[n]) + list(G_2[n])}
Mass_extr_G  = {g: random.randint(1,5) for n in C for g in list(G_1[n]) + list(G_2[n])}


#duracion del periodo
T_t = {
    t: 8
    for t in T
}


#======= Variables ======
#------------------------
#(x esta en orden actividad, tiempo, tipo de drill)
x = m.addVars(Act, T, Dr,vtype=GRB.BINARY,name="x")
y = m.addVars(Act, T,vtype=GRB.BINARY,name="y")
z = m.addVars(Act, T,vtype=GRB.BINARY,name="z")
#------------------------
x_bar = m.addVars(Act, T, Dr,vtype=GRB.BINARY,name="x_bar")
y_bar = m.addVars(Act, T,vtype=GRB.BINARY,name="y_bar")
z_bar = m.addVars(Act, T,vtype=GRB.BINARY,name="z_bar")
#------------------------
x_hat = m.addVars(I, Act, T, Dr,vtype=GRB.CONTINUOUS,lb=0,ub=1,name="x_hat")
y_hat = m.addVars(J, Act, T,vtype=GRB.CONTINUOUS,lb=0,ub=1,name="y_hat")
z_hat = m.addVars(K, Act, T,vtype=GRB.CONTINUOUS,lb=0,ub=1,name="z_hat")
#------------------------
zC    = m.addVars(C, T, vtype=GRB.BINARY, name="zC")                    
zbarC = m.addVars(C, T, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="zbarC") 

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
        m.addConstr(
            gp.quicksum(
                T_t[t] * (
                    gp.quicksum(x_hat[ih, g, t, 0] for ih in I_h) +
                    gp.quicksum(y_hat[j,  g, t]    for j  in J)   +
                    gp.quicksum(z_hat[k,  g, t]    for k  in K)
                )
                for g in G_1[c]
            )
            +
            gp.quicksum(
                T_t[t] * (
                    gp.quicksum(x_hat[ih, g, t, 0] for ih in I_h) +
                    gp.quicksum(y_hat[j,  g, t]    for j  in J)   +
                    gp.quicksum(z_hat[k,  g, t]    for k  in K)
                )
                for g in G_2[c]
            )
            +
            gp.quicksum(
                T_t[t] * (
                    gp.quicksum(x_hat[idr, nu, t, 2] for idr in I_d) +
                    gp.quicksum(y_hat[j,   nu, t]    for j   in J)   +
                    gp.quicksum(z_hat[k,   nu, t]    for k   in K)
                )
                for nu in S[c]
            )
            <= T_t[t]
        )

#---- Progreso acumulado ------

for n in C:
    for c in G_1[n]:
        for t in T:
            m.addConstr(
                x_bar[c,t,0] * Mass_drill_G[c]
                <= gp.quicksum(
                    x_hat[i,c,tau,0] * T_t[tau]
                    for i in I_h
                    for tau in range(0, t+1)
                )
            )

            m.addConstr(
                y_bar[c,t] * Mass_blast_G[c]
                <= gp.quicksum(
                    y_hat[j,c,tau] * T_t[tau]
                    for j in J
                    for tau in range(0, t+1)
                )
            )

            m.addConstr(
                z_bar[c,t] * Mass_extr_G[c]
                <= gp.quicksum(
                    z_hat[k,c,tau] * T_t[tau]
                    for k in K
                    for tau in range(0, t+1)
                )
            )

for n in C:
    for c in G_2[n]:
        for t in T:
            m.addConstr(
                x_bar[c,t,0] * Mass_drill_G[c]
                <= gp.quicksum(
                    x_hat[i,c,tau,0] * T_t[tau]
                    for i in I_h
                    for tau in range(0, t+1)
                )
            )

            m.addConstr(
                y_bar[c,t] * Mass_blast_G[c]
                <= gp.quicksum(
                    y_hat[j,c,tau] * T_t[tau]
                    for j in J
                    for tau in range(0, t+1)
                )
            )

            m.addConstr(
                z_bar[c,t] * Mass_extr_G[c]
                <= gp.quicksum(
                    z_hat[k,c,tau] * T_t[tau]
                    for k in K
                    for tau in range(0, t+1)
                )
            )

for n in C:
    for c in S[n]:
        for t in T:
            m.addConstr(
                x_bar[c,t,2] * Mass_drill[c]
                <= gp.quicksum(
                    x_hat[i,c,tau,2] * T_t[tau]
                    for i in I_d
                    for tau in range(0, t+1)
                )
            )

            m.addConstr(
                y_bar[c,t] * Mass_blast[c]
                <= gp.quicksum(
                    y_hat[j,c,tau] * T_t[tau]
                    for j in J
                    for tau in range(0, t+1)
                )
            )

            m.addConstr(
                z_bar[c,t] * Mass_extr[c]
                <= gp.quicksum(
                    z_hat[k,c,tau] * T_t[tau]
                    for k in K
                    for tau in range(0, t+1)
                )
            )

#---- Restricciones de vinculo y finalizacion ------

for n in C:
    for c in G_1[n]:
        m.addConstr(gp.quicksum(x[c,t,0] for t in T) == 1)
        m.addConstr(gp.quicksum(y[c,t]   for t in T) == 1)
        m.addConstr(gp.quicksum(z[c,t]   for t in T) == 1)

for n in C:
    for c in G_2[n]:
        m.addConstr(gp.quicksum(x[c,t,0] for t in T) == 1)
        m.addConstr(gp.quicksum(y[c,t]   for t in T) == 1)
        m.addConstr(gp.quicksum(z[c,t]   for t in T) == 1)

for n in C:
    for c in S[n]:
        m.addConstr(gp.quicksum(x[c,t,2] for t in T) == 1)
        m.addConstr(gp.quicksum(y[c,t]   for t in T) == 1)
        m.addConstr(gp.quicksum(z[c,t]   for t in T) == 1)

for n in C:
    for c in G_1[n]:
        for t in T:
            m.addConstr(x[c,t,0] <= x_bar[c,t,0])
            m.addConstr(y[c,t]   <= y_bar[c,t])
            m.addConstr(z[c,t]   <= z_bar[c,t])

for n in C:
    for c in G_2[n]:
        for t in T:
            m.addConstr(x[c,t,0] <= x_bar[c,t,0])
            m.addConstr(y[c,t]   <= y_bar[c,t])
            m.addConstr(z[c,t]   <= z_bar[c,t])

for n in C:
    for c in S[n]:
        for t in T:
            m.addConstr(x[c,t,2] <= x_bar[c,t,2])
            m.addConstr(y[c,t]   <= y_bar[c,t])
            m.addConstr(z[c,t]   <= z_bar[c,t])

#======= Secuencias de procesos =======

for n in C:
    for c in G_1[n]:
        for t in range(1,time_l):
            m.addConstr(
                gp.quicksum(y_hat[j,c,t] for j in J) <= J_val * x_bar[c,t - 1,0]
            )

for n in C:
    for c in G_1[n]:
        for t in range(1,time_l):
            m.addConstr(
                gp.quicksum(y_hat[j,c,t] for j in J) <= J_val * x_bar[c,t - 1,0]
            )

for n in C:
    for c in G_1[n]:
        for t in range(1,time_l):
            m.addConstr(
                gp.quicksum(z_hat[k,c,t] for k in K) <= J_val * y_bar[c,t - 1]
            )

for n in C:
    for c in G_2[n]:
        for t in range(1,time_l):
            m.addConstr(
                gp.quicksum(z_hat[k,c,t] for k in K) <= J_val * y_bar[c,t - 1]
            )

for n in C:
    for c in S[n]:
        for t in range(1,time_l):
            m.addConstr(
                gp.quicksum(y_hat[j,c,t] for j in J) <= J_val * x_bar[c,t-1,2]
            )

for n in C:
    for c in S[n]:
        for t in range(1,time_l):
            m.addConstr(
                gp.quicksum(z_hat[k,c,t] for k in K) <= J_val * y_bar[c,t - 1]
            )

# ---- Precedencia estricta ----

for n in C:
    for c in G_1[n]:
        for t in range(1, time_l):
            for pred in P_c:
                if P_c[pred] is None:
                    continue

                m.addConstr(
                    gp.quicksum(x_hat[i,c,t,0] for i in I_h)
                    <= len(I_h) * z_bar[pred, t-1]
                )

                m.addConstr(
                    gp.quicksum(y_hat[j,c,t] for j in J)
                    <= len(J) * z_bar[pred, t-1]
                )

                m.addConstr(
                    gp.quicksum(z_hat[k,c,t] for k in K)
                    <= len(K) * z_bar[pred, t-1]
                )


for n in C:
    for c in G_2[n]:
        for t in range(1, time_l):
            for pred in P_c:
                if P_c[pred] is None:
                    continue

                m.addConstr(
                    gp.quicksum(x_hat[i,c,t,0] for i in I_h)
                    <= len(I_h) * z_bar[pred, t-1]
                )

                m.addConstr(
                    gp.quicksum(y_hat[j,c,t] for j in J)
                    <= len(J) * z_bar[pred, t-1]
                )

                m.addConstr(
                    gp.quicksum(z_hat[k,c,t] for k in K)
                    <= len(K) * z_bar[pred, t-1]
                )


for n in C:
    for c in S[n]:
        for t in range(1, time_l):
            for pred in P_c:
                if P_c[pred] is None:
                    continue

                m.addConstr(
                    gp.quicksum(x_hat[i,c,t,2] for i in I_d)
                    <= len(I_d) * z_bar[pred, t-1]
                )

                m.addConstr(
                    gp.quicksum(y_hat[j,c,t] for j in J)
                    <= len(J) * z_bar[pred, t-1]
                )

                m.addConstr(
                    gp.quicksum(z_hat[k,c,t] for k in K)
                    <= len(K) * z_bar[pred, t-1]
                )

#----- Restricciones del objetivo -------

for n in C:
    for c in G_1[n]:
        for t in range(1, time_l):
            m.addConstr(
                x_bar[c,t,0] >= x_bar[c,t-1,0]
            )
            m.addConstr(
                y_bar[c,t] >= y_bar[c,t-1]
            )
            m.addConstr(
                z_bar[c,t] >= y_bar[c,t-1]
            )

for n in C:
    for c in G_2[n]:
        for t in range(1, time_l):
            m.addConstr(
                x_bar[c,t,0] >= x_bar[c,t-1,0]
            )
            m.addConstr(
                y_bar[c,t] >= y_bar[c,t-1]
            )
            m.addConstr(
                z_bar[c,t] >= y_bar[c,t-1]
            )

for n in C:
    for c in S[n]:
        for t in range(1, time_l):
            m.addConstr(
                x_bar[c,t,0] >= x_bar[c,t-1,2]
            )
            m.addConstr(
                y_bar[c,t] >= y_bar[c,t-1]
            )
            m.addConstr(
                z_bar[c,t] >= y_bar[c,t-1]
            )

#======== Bateas ========
#---- Tiempo ----

for n in C:
    for t in T:
        for i in I_d:
            m.addConstr(
                gp.quicksum(x_hat[i,b,t,2]*T_t[t] for b in B[n]) <= T_t[t] * Lambda["i"]
            )
        
        for j in J:
            m.addConstr(
                gp.quicksum(y_hat[j,b,t]*T_t[t] for b in B[n]) <= T_t[t] * Lambda["j"]
            )

        for k in K:
            m.addConstr(
                gp.quicksum(z_hat[k,b,t]*T_t[t] for b in B[n]) <= T_t[t] * Lambda["k"]
            )

#---- Precedencia ----

for n in C:
    for t in range(1,time_l):    
        for m_g in G_2[n]:
            for b in B[n]:
                m.addConstr(
                    gp.quicksum(x_hat[i,b,t,2] for i in I_d) <= I_d_v * z_bar[m_g, t-1]
                )
                m.addConstr(
                    gp.quicksum(y_hat[j,b,t] for j in J) <= J_val * z_bar[m_g, t-1]
                )
                m.addConstr(
                    gp.quicksum(z_hat[k,b,t] for k in K) <= K_val * z_bar[m_g, t-1]
                )

#---- Progreso ----
#agregue un parametro para la amsa de las bateas

for n in C:
    for b in B[n]:
        for t in T:
            m.addConstr(
                x_bar[b, t, 2] * Mass_drill_B[b]
                <= gp.quicksum(x_hat[i, b, tau, 2] * T_t[tau] for i in I_d for tau in range(0, t+1))
            )
            m.addConstr(
                y_bar[b, t] * Mass_blast_B[b]
                <= gp.quicksum(y_hat[j, b, tau] * T_t[tau] for j in J for tau in range(0, t+1))
            )
            m.addConstr(
                z_bar[b, t] * Mass_extr_B[b]
                <= gp.quicksum(z_hat[k, b, tau] * T_t[tau] for k in K for tau in range(0, t+1))
            )

#---- Vinculo y finalizacón ----

for n in C:
    for b in B[n]:
        m.addConstr(gp.quicksum(x[b, t, 2] for t in T) == 1)
        m.addConstr(gp.quicksum(y[b, t]    for t in T) == 1)
        m.addConstr(gp.quicksum(z[b, t]    for t in T) == 1)

        for t in T:
            m.addConstr(x[b, t, 2] <= x_bar[b, t, 2])
            m.addConstr(y[b, t]    <= y_bar[b, t])
            m.addConstr(z[b, t]    <= z_bar[b, t])

#---- Secuencia de procesos ----

for n in C:
    for b in B[n]:
        for t in range(1, time_l):
            m.addConstr(
                gp.quicksum(y_hat[j, b, t] for j in J) <= J_val * x_bar[b, t-1, 2]
            )
            m.addConstr(
                gp.quicksum(z_hat[k, b, t] for k in K) <= K_val * y_bar[b, t-1]
            )

#---- Restricciones de objetivo ----

for n in C:
    for b in B[n]:
        for t in range(1, time_l):
            m.addConstr(x_bar[b, t, 2] >= x_bar[b, t-1, 2])  
            m.addConstr(y_bar[b, t]    >= y_bar[b, t-1])     
            m.addConstr(z_bar[b, t]    >= z_bar[b, t-1])     

#======== Union caseron-subcaseron-batea-galeria ========
#65
for n in C:
    for c_sub in S[n]:
        for t in range(1, time_l):  
            for m_g in list(G_1[n]) + list(G_2[n]): 
                m.addConstr(
                    gp.quicksum(y_hat[j, c_sub, t] for j in J)
                    <= len(J) * z_bar[m_g, t-1]
                )

#66
for n in C:
    for c_sub in S[n]:
        b_sub = SB_of_sub[c_sub]     
        for t in range(1, time_l): 
            m.addConstr(
                gp.quicksum(y_hat[j, c_sub, t] for j in J)
                <= len(J) * z_bar[b_sub, t-1]
            )

#67
for n in C:
    for c_sub in S[n]:
        for t in range(1, time_l):  
            for m_g in list(G_1[n]) + list(G_2[n]):
                m.addConstr(
                    gp.quicksum(z_hat[k, c_sub, t] for k in K)
                    <= len(K) * z_bar[m_g, t-1]
                )

#68
for n in C:
    for c_sub in S[n]:
        b_sub = SB_of_sub[c_sub]   
        for t in range(1, time_l):
            m.addConstr(
                gp.quicksum(z_hat[k, c_sub, t] for k in K)
                <= len(K) * z_bar[b_sub, t-1]
            )

#69
for c in C:
    Sc = list(S[c]) 
    for t in T:
        m.addConstr(
            zbarC[c, t]
            <= (1.0 / len(Sc)) * gp.quicksum(
                gp.quicksum(z[nu, tau] for tau in range(0, t+1))
                for nu in Sc
            )
        )

#70
for c in C:
    for t in T:
        m.addConstr(
            zC[c, t] <= zbarC[c, t]
        )

#71
for c in C:
    m.addConstr(
        gp.quicksum(zC[c, t] for t in T) == 1
    )

# =======================
#   FUNCIÓN OBJETIVO 
# =======================

m.setObjective(
    gp.quicksum(t * zC[c, t] for c in C for t in T),
    GRB.MINIMIZE
)

m.optimize()

print("\n=== RESULTADO ===")
print("Status:", m.Status)

if m.Status == GRB.OPTIMAL:
    print("ObjVal:", m.ObjVal)

    for c in C:
        t_end = [t for t in T if zC[c, t].X > 0.5]
        print(f"Caserón {c} termina en t =", t_end[0] if t_end else None)

elif m.Status == GRB.INFEASIBLE:
    print("Modelo INFEASIBLE. Calculando IIS...")
    m.computeIIS()
    m.write("iis.ilp")
    print("Escribí iis.ilp (abre ese archivo para ver restricciones conflictivas).")

elif m.Status == GRB.UNBOUNDED:
    print("Modelo UNBOUNDED (sin cota). Revisa objetivo/restricciones.")
else:
    print("Estado distinto (p.ej. TIME_LIMIT).")

