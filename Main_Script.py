# coding: utf-8


#        bibliotecas
# -----------------------------
from py_dss_functions import *
from Boxplot import *
import time
import pickle
# -----------------------------


# Definição da classe Rede para coleta de dados
class Rede(object):
    def __init__(self, losses, vmax, vmin, overload_transformers, cenario, penetration_level):
        self.losses = losses
        self.vmax = vmax
        self.vmin = vmin
        self.overload_transformers = overload_transformers
        self.cenario = cenario
        self.penetration_level = penetration_level


# ---------------------------------------------------------------
# Definição dos arquivos a serem simulados
# ---------------------------------------------------------------

Master_dss = r"D:\Pedro\Universidade\TCC\Simulacoes\Teste_DLL\Rede_CPFL_BAR\Master.dss"  # Arquivo Master.dss
datapath = r"D:\Pedro\Universidade\TCC\Simulacoes\Teste_DLL\Rede_CPFL_BAR"               # Diretório dos resultados

# ---------------------------------------------------------------
# Definição dos parâmetros da simulacao
# ---------------------------------------------------------------

loadshape_variations = 4                                             # Número de variações de loadshapes desejado
max_iterations = 50                                                  # Seleciona o numero de iterações por cenário
random.seed(2022)                                                    # Número inicial do gerador de números aleatórios
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
                overload_transformers = get_loading(datapath, cenarios[i])
                level_list.append(Rede(losses, vmax, vmin, overload_transformers, cenarios[i], penetration_level))

        cenarios_list.append(level_list)
    Results.append(cenarios_list)
    print('Simulações do cenário "' + cenarios[i] + '" foram finalizadas')

end = time.time()                                                    # Fim da contagem de tempo
print('\n tempo de simulação = ' + str(round(((end - start)/60), 2)) + ' minutos')

# ---------------------------------------------------------------
# Análise dos dados para geração dos gráficos
# ---------------------------------------------------------------

clear_folder(r"D:\Pedro\Universidade\TCC\Simulacoes\Teste_DLL\images")

losses = []
vmax = []
vmin = []
overload_transformers = []

for i in range(len(cenarios)):
    cenario = Results[i]
    if cenarios[i] == 'base_case':
        for level in cenario:
            for simulation in level:
                losses.append(simulation.losses)
                vmax.append(simulation.vmax)
                vmin.append(simulation.vmin)
                overload_transformers.append(simulation.overload_transformers)

        print('Média das perdas no caso base = ', np.mean(losses))
        print('Média da tensão máxima no caso base = ', np.mean(vmax))
        print('Média da tensão mínima no caso base = ', np.mean(vmin))
        print('Média de transformadores sobrecarregados no caso base = ', np.mean(overload_transformers))

    else:
        level_list_losses = []
        level_list_vmax = []
        level_list_vmin = []
        level_list_overload_transformers = []

        for level in cenario:
            losses = []
            vmax = []
            vmin = []
            overload_transformers = []

            for simulation in level:
                losses.append(simulation.losses)
                vmax.append(simulation.vmax)
                vmin.append(simulation.vmin)
                overload_transformers.append(simulation.overload_transformers)

            level_list_losses.append(losses)
            level_list_vmax.append(vmax)
            level_list_vmin.append(vmin)
            level_list_overload_transformers.append(overload_transformers)

        with open("Results", "wb") as fp:                          # Salvando os vetores caso der erro na plotagem
            pickle.dump(level_list_losses, fp)
            pickle.dump(level_list_overload_transformers, fp)
            pickle.dump(level_list_vmax, fp)
            pickle.dump(level_list_vmin, fp)

        plot_boxplot(level_list_losses, cenarios[i], 'losses')
        plot_boxplot(level_list_overload_transformers, cenarios[i], 'loading')
        plot_double_boxplot(level_list_vmax, level_list_vmin, cenarios[i], 'voltage')

print('As figuras foram criadas com sucesso!')
