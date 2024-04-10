import random
import math
import matplotlib.collections as mc
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import os

def generate_coordinates(n_cities):
    coordinates = []
    for i in range(n_cities):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        coordinates.append((x,y))

    return coordinates

# computar a distância total percorrida pelo caixeiro viajante
def get_total_distance(distances, tour):
    
    total_distance = 0

    # mudança simples para pegar as distâncias, porque agora tour é uma matriz do tour de cada caixeiro
    for tr in tour:
        for i in range(len(tr)-1):
            total_distance += distances[tr[i]][tr[i+1]]

        # tour[-1]: pega o último elemento (-2 pega o 2º último e por assim vai)
        total_distance += distances[tr[-1]][tr[0]]

    return int(total_distance)

def generate_lines(coordinates, tour):
    lines = []

    for j in range(len(tour) - 1):
        lines.append([
            coordinates[tour[j]],
            coordinates[tour[j+1]]
        ])

    lines.append([
        coordinates[tour[-1]],
        coordinates[tour[0]] # vai do ultimo ao primeiro
    ])

    return lines


def plot_tour(coordinates, tour, n_caixeiros, nomeArq, distances):

    # variável color para mudar a cor de cada caixeiro
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    # subplot == uma folha em branco para desenharmos
    fig, ax = pl.subplots()
    for i in range(n_caixeiros):
        lc = mc.LineCollection(generate_lines(coordinates, tour[i]), linewidths=2, colors=colors[i])
        ax.add_collection(lc)
    ax.autoscale() # ajusta a figura para fazer caber o desenho
    ax.margins(0.1)
    # scatter == grafo
    pl.scatter([i[0] for i in coordinates], [i[1] for i in coordinates])
    pl.title("Distância:"+str(get_total_distance(distances, tour)))
    pl.xlabel("X")
    pl.ylabel("Y")
    pl.savefig(nomeArq+".png")
    pl.close()

def heuristic_multiplos_caixeiros(distances, n_cities, n_caixeiros):

    if(n_caixeiros == 0):
        return [0]
    if(n_caixeiros == n_cities):
        return [0]
    
    remaining_cities = list(range(1, n_cities))  # Começo uma lista de cidades restantes retirando a cidade 0 pois ela será sempre a cidade inicial de todo caixeiro
    tours = [[] for _ in range(n_caixeiros)] # Inicio a variável tours como uma matriz para cada caixeiro existente

    # (len(remaining_cities)+n_caixeiros)//n_caixeiros
    # cálculo de quantas cidades cada caixeiro viajará
    # print((len(remaining_cities)+n_caixeiros)//n_caixeiros)

    cidades_kd = (len(remaining_cities)+n_caixeiros)//n_caixeiros # Variável para quantas cidades kd caixeiro vai viajar

    for i in range(n_caixeiros): # Esse for roda somente 1 vez por caixeiro
        if remaining_cities:
            tours[i].append(0)  # Começa do ponto 0
            current_city, x = nearest_neighbor(tours[i][-1], remaining_cities, distances) # Current_city =  Nearest_City
            tours[i].append(current_city)
            remaining_cities.remove(current_city)
        else:
            break

    for i in range(n_caixeiros): # Esse for roda até que, OU os caixeiros percorram todas as cidades OU os caixeiros percorram seu limite de cidades
        while remaining_cities:
            if remaining_cities and len(tours[i]) < cidades_kd:
                nearest_city, x = nearest_neighbor(tours[i][-1], remaining_cities, distances)
                tours[i].append(nearest_city)
                remaining_cities.remove(nearest_city)
            else:
                break

    while remaining_cities: # Esse for roda até que todas as cidades restantes tenham sido percorridas, caso todos os caixeiros estejam no limite ele verifica em qual tour é mais propício de se encaixar
        nearest_city, nearest_distance = nearest_neighbor(tours[i][-1], remaining_cities, distances)
        visitado = 0
        for i in range(n_caixeiros):
            n, d = nearest_neighbor(tours[i][-1], remaining_cities, distances)
            if nearest_distance > d:
                nearest_distance = d
                nearest_city = n
                visitado = i

        tours[visitado].append(nearest_city)
        remaining_cities.remove(nearest_city)

    return tours

def nearest_neighbor(city, remaining_cities, distances): # Método que procura a cidade mais próxima
    min_distance = float('inf') # Cria um número infinito para usar no cálculo da mais proxima
    nearest_city = None

    for next_city in remaining_cities: # Foreach city in remaining_cities
        if distances[city][next_city] < min_distance:
            min_distance = distances[city][next_city]
            nearest_city = next_city
    
    return nearest_city, min_distance # Retorna a cidade mais próxima e a distância mínima (usada em um momento específico)

def ler_instancia(nome):
    file = open("instances/"+nome, "r")
    coordinates = []
    n_cities = 0

    # Lê cada cidade e guarda elas na matriz de coordenadas
    for line in file:
        linha = line.split()
        n_cities += 1
        coordinates.append((int(linha[1]), int(linha[2])))
    
    # Gera a matriz de distâncias baseada na tabela de coordenadas
    distances = [[0 for _ in range(n_cities)] for _ in range(n_cities)]

    for i in range(n_cities):
        for j in range(i + 1, n_cities):
            x = coordinates[i][0] - coordinates[j][0]
            y = coordinates[i][1] - coordinates[j][1]
            distance = math.sqrt(x**2 + y**2) 
            distances[i][j] = distances[j][i] = distance

    # Verifica o nome no final do arquivo para descobrir a quantidade de caixeiros
    nomeRecortado = nome.split('-')
    n_caixeiros = int(nomeRecortado[2].replace("m",""))

    return n_cities, n_caixeiros, coordinates, distances

def ler_instancias(diretorio):
    files = os.listdir(diretorio)

    for f in files:
        n_cities, n_caixeiros, coordinates, distances = ler_instancia(f)
        tour = heuristic_multiplos_caixeiros(distances, n_cities, n_caixeiros)
        plot_tour(coordinates, tour, n_caixeiros, f, distances)

    
    
#instancia_a_ler = "mTSP-n31-m3"
diretorio = "instances/"
ler_instancias(diretorio)

#n_cities, n_caixeiros, coordinates, distances = ler_instancia(instancia_a_ler)
#tour = heuristic_multiplos_caixeiros(distances, n_cities, n_caixeiros)
#distanciaTotal = get_total_distance(tour)
#print(distanciaTotal)
#plot_tour(coordinates, tour, n_caixeiros)