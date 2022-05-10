# coding: utf-8


#        bibliotecas
# -----------------------------
from py_dss_functions import *
from Boxplot import *
import time
# import pickle
# -----------------------------


# Definição da classe Rede para coleta de dados
class Rede(object):
    def __init__(self, losses, vmax, vmin, overload_transformers, overload_mean, cenario, penetration_level):
        self.losses = losses
        self.vmax = vmax
        self.vmin = vmin
        self.overload_transformers = overload_transformers
        self.overload_mean = overload_mean
        self.cenario = cenario
        self.penetration_level = penetration_level


# ---------------------------------------------------------------
# Definição dos arquivos a serem simulados
# ---------------------------------------------------------------

Master_dss = r"D:\pedro\Rede_CPFL_BAR\Master.dss"  # Arquivo Master.dss
datapath = r"D:\pedro\Rede_CPFL_BAR"               # Diretório dos resultados

# ---------------------------------------------------------------
# Definição dos parâmetros da simulacao
# ---------------------------------------------------------------

loadshape_variations = 30                                            # Número de variações de loadshapes desejado
max_iterations = 300                                                 # Seleciona o numero de iterações por cenário
random.seed(10)                                                      # Número inicial do gerador de números aleatórios
np.random.seed(10)                                                   # Número inicial do gerador de números aleatórios
cenarios = ['base_case', 'monophasic_station', 'triphasic_station',  # Cenários de sorteios para o MMC
            'renewable_station', 'stations_mix']

# ---------------------------------------------------------------
# Início do processo de simulação
# ---------------------------------------------------------------

start = time.time()                                                  # Início da contagem de tempo
clear_folder(datapath)                                               # Limpa o diretorio
compile_dss(Master_dss, datapath, 'base_case')                       # Compila o sistema
create_loadshapes(datapath, loadshape_variations)                    # Cria arquivo com variações das curvas de carga
Results = []                                                         # Vetor para coleta de resultados

for i in range(len(cenarios)):
    cenarios_list = []
    for penetration_level in np.arange(0, 1.2, 0.2):
        level_list = []
        if cenarios[i] == 'base_case' and penetration_level > 0:
            break
        elif cenarios[i] != 'base_case' and penetration_level == 0:
            continue
        else:
            for simulation in range(max_iterations):
                compile_dss(Master_dss, datapath, cenarios[i])
                sample_loadshapes(loadshape_variations)
                sample_stations(cenarios[i], penetration_level)
                solve_dss()
                losses = get_losses(datapath, cenarios[i])
                vmax, vmin = get_voltages(datapath, cenarios[i])
                overload_transformers, overload_mean = get_loading(datapath, cenarios[i])
                level_list.append(Rede(losses, vmax, vmin, overload_transformers, overload_mean, cenarios[i], penetration_level))

        cenarios_list.append(level_list)
    Results.append(cenarios_list)
    print('Simulações do cenário "' + cenarios[i] + '" foram finalizadas')

end = time.time()                                                    # Fim da contagem de tempo
print('\n tempo de simulação = ' + str(round(((end - start)/60), 2)) + ' minutos')

# ---------------------------------------------------------------
# Análise dos dados para geração dos gráficos
# ---------------------------------------------------------------

clear_folder(r"D:\pedro\images")

losses = []
vmax = []
vmin = []
overload_transformers = []
overload_means = []


for i in range(len(cenarios)):
    cenario = Results[i]
    if cenarios[i] == 'base_case':
        for level in cenario:
            for simulation in level:
                losses.append(simulation.losses)
                vmax.append(simulation.vmax)
                vmin.append(simulation.vmin)
                overload_transformers.append(simulation.overload_transformers)
                overload_means.append(simulation.overload_mean)

        print('Média das perdas no caso base = ', np.mean(losses))
        print('Média da tensão máxima no caso base = ', np.mean(vmax))
        print('Média da tensão mínima no caso base = ', np.mean(vmin))
        print('Média de transformadores sobrecarregados no caso base = ', round(int(np.mean(overload_transformers))))
        print('Média de carregamento dos transformadores sobrecarregados no caso base = ', round(int(np.mean(overload_means))))

    else:
        level_list_losses = []
        level_list_vmax = []
        level_list_vmin = []
        level_list_overload_transformers = []
        level_list_overload_means = []

        for level in cenario:
            losses = []
            vmax = []
            vmin = []
            overload_transformers = []
            overload_means = []

            for simulation in level:
                losses.append(simulation.losses)
                vmax.append(simulation.vmax)
                vmin.append(simulation.vmin)
                overload_transformers.append(simulation.overload_transformers)
                overload_means.append(simulation.overload_mean)

            level_list_losses.append(losses)
            level_list_vmax.append(vmax)
            level_list_vmin.append(vmin)
            level_list_overload_transformers.append(overload_transformers)
            level_list_overload_means.append(overload_means)

        t = 0
        print('Média de Transformadores sobrecarregados no cenário ' + cenarios[i] + ':')
        for transformer in level_list_overload_transformers:
            print('No nível de penetração ' + str(t) + ': ', round(int(np.mean(transformer))))
            t = t + 1

        plot_boxplot(level_list_losses, cenarios[i], 'losses')
        plot_boxplot(level_list_overload_means, cenarios[i], 'loading')
        plot_double_boxplot(level_list_vmax, level_list_vmin, cenarios[i], 'voltage')

print('As figuras foram criadas com sucesso!')
