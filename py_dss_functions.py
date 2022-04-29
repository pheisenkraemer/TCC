# coding: utf-8

#        bibliotecas
# -----------------------------
import py_dss_interface
import pandas as pd
import os
import shutil
import scipy.stats as stats
import random
import numpy as np
# -----------------------------


# Definições da classe DSS
dss = py_dss_interface.DSSDLL()


# ---------------------------------------------------------------
# Definições das funções para serem utilizadas nas simulações
# ---------------------------------------------------------------


# Função para compilar o OpenDSS
def compile_dss(dss_file, datapath, casename):
    dss.dss_clear_all()
    dss.text("compile {}".format(dss_file))
    dss.text("Set datapath={}".format(datapath))
    dss.text("Set casename={}".format(casename))
    dss.text("Set Mode=yearly ControlMode=Time time=(0,0) Number=288 stepsize=5m")
    dss.text("Set demandinterval=true DIVerbose=true")
    dss.text("Set overloadreport=true voltexcept=true")
    dss.text("Set normvminpu=0.92 normvmaxpu=1.05")


# Função para rodar simulações
def solve_dss():
    dss.solution_solve_all()
    dss.text("closedi")


def get_loads_total_power():
    total_power = 0
    dss.loads_first()

    for i in range(dss.loads_count()):
        load_kw = dss.loads_read_kw()
        total_power = total_power + load_kw

    return total_power


# Função para coletar dados de tensão da simulação
def get_voltages(datapath, casename):
    voltage_csv = r"\{}\DI_yr_0\DI_VoltExceptions_1.CSV".format(casename)
    folder = datapath + voltage_csv
    df = pd.read_csv(folder, engine='python')

    vmax = df[' "Max Voltage"'].max()
    vmin = df[' "Min Voltage"'].min()

    return vmax, vmin


# Função para coletar dados de carregamento da simulação
def get_loading(datapath, casename):
    overload_csv = r"\{}\DI_yr_0\DI_Overloads_1.CSV".format(casename)
    folder = datapath + overload_csv
    df = pd.read_csv(folder, engine='python')

    # lines_violated = 0
    transformers_violated = 0

    elements = list(pd.unique(df[' "Element"']))
    for element in elements:
        # if element.find("Line") != -1:
        #    lines_violated = lines_violated + 1
        if element.find("Transformer") != -1:
            transformers_violated = transformers_violated + 1

    # overload_lines = (lines_violated/dss.lines_count())*100
    overload_transformers = (transformers_violated/dss.transformers_count())*100

    return overload_transformers


# Função para coletar dados de perdas da simulação
def get_losses(datapath, casename):
    losses_csv = r"\{}\DI_yr_0\SystemMeter_1.CSV".format(casename)
    folder = datapath + losses_csv
    df = pd.read_csv(folder, engine='python')

    energia_kwh = df[' kWh'].max()
    perdas_kwh = df[' "Losses kWh"'].max()
    perdaspercentuais = (perdas_kwh/energia_kwh)*100

    return perdaspercentuais


# Função para gerar estação de recarga monofásica convencional
def create_monophasic_station(name, bus, kv):
    dss.text("New line.mono_{} phases=1 bus1={} bus2=mono_sec_{} switch=yes".format(name, bus, bus))

    dss.text("makebuslist")
    dss.text("setkVBase bus=mono_sec_{} kVLL={}".format(bus, kv))

    dss.text(
        "New Load.station_mono_{} bus1=mono_sec_{} phases=1 conn=wye model=1 kv=0.127 kw=7.4 pf=0.98"
        " yearly=Flat_Curve".format(name, bus))


# Função para gerar estação de recarga trifásica convencional
def create_triphasic_station(name, bus, kv):
    phase_kv = kv * np.sqrt(3)

    dss.text("New line.tri_{} phases=3 bus1={} bus2=tri_sec_{} switch=yes".format(name, bus, bus))
    dss.text("New transformer.tri_{} phases=3 windings=2 buses=(tri_sec_{}, tri_ter_{}) conns=(wye, wye) "
             "kVs=({},0.38) xhl=3.78 %R=1.82 kVAs=(45.0, 45.0)".format(name, bus, bus, phase_kv))

    dss.text("makebuslist")
    dss.text("setkVBase bus=tri_sec_{} kVLL={}".format(bus, phase_kv))
    dss.text("setkVBase bus=tri_ter_{} kVLL=0.38".format(bus))

    dss.text("New Load.station_tri_{} bus1=tri_ter_{} phases=3 conn=wye model=1 kv=0.38 kw=22.0 pf=0.98"
             " yearly=Flat_Curve".format(name, bus))


# Função para gerar estação de recarga trifásica com PV e banco de baterias
def create_renewable_station(name, bus, kv):
    phase_kv = kv * np.sqrt(3)

    dss.text("New line.renewable_{} phases=3 bus1={} bus2=tri_sec_{} switch=yes".format(name, bus, bus))
    dss.text("New transformer.renewable_{} phases=3 windings=2 buses=(tri_sec_{}, tri_ter_{}) conns=(wye, wye) " 
             "kVs=({},0.38) xhl=3.78 %R=1.82 kVAs=(45.0, 45.0)".format(name, bus, bus, phase_kv))

    dss.text("makebuslist")
    dss.text("setkVBase bus=tri_sec_{} kVLL={}".format(bus, phase_kv))
    dss.text("setkVBase bus=tri_ter_{} kVLL=0.38".format(bus))

    dss.text(
        "New Load.station_renewable_{} bus1=tri_ter_{} phases=3 conn=wye model=1 kv=0.38 kw=22.0 pf=0.98"
        " yearly=Station_Curve_PV_Bank".format(name, bus))


# função para gerar variações nas curvas de carga dos consumidores
def cdf(media):

    sigma = 0.1
    mediamais4dp = media+4*sigma
    mediamenos4dp = media-4*sigma
    qtdpts = 100
    incremento = (mediamais4dp - mediamenos4dp) / qtdpts
    eixo_x = list()  # Eixo X da função

    for i in range(100):
        if mediamenos4dp > 0:
            eixo_x.append(mediamenos4dp)
        mediamenos4dp = mediamenos4dp + incremento

    f_x = stats.norm.pdf(eixo_x, media, sigma)  # função de densidade de probabilidade

    eixo_y = list()  # Eixo Y da função

    fda = f_x[0]  # função de distribuição acumulada
    for i in range(len(f_x) - 1):
        if eixo_x[i] > 0:
            eixo_y.append(fda)
        fda = fda + f_x[i + 1]

    sorteio = random.uniform(0, eixo_y[len(eixo_y) - 1])

    j = 0
    for i in range(len(eixo_y)):
        if eixo_y[i] < sorteio < eixo_y[i + 1]:
            dif1 = sorteio - eixo_y[i]
            dif2 = eixo_y[i + 1] - sorteio
            if dif1 > dif2:
                j = i + 1
            else:
                j = i

    return eixo_x[j]


# Função para criar novas variações das curvas de carga dos consumidores
def create_loadshapes(datapath, variations):
    archive = r"\new_loadshapes.dss"
    folder = datapath + archive

    with open("new_loadshapes.dss") as f:          # Verifica se o arquivo já esxiste e se contem todas as variações
        firstline = f.readlines()[0].rstrip()
        description = "!Curve_Variations = {}".format(variations)

    if os.path.exists(folder) and description in firstline:
        pass
    else:
        arquivo = open("new_loadshapes.dss", "w")  # cria um dss na pasta onde está o código
        arquivo.truncate(0)

        df_1 = pd.read_csv(r"D:\Pedro\Universidade\TCC\Simulacoes\Teste_DLL\Curva_Flat.csv")
        df_2 = pd.read_csv(r"D:\Pedro\Universidade\TCC\Simulacoes\Teste_DLL\Curva_Estacao_PV.csv")
        df_3 = pd.read_csv(r"D:\Pedro\Universidade\TCC\Simulacoes\Teste_DLL\Curva_Estacao_PV_Banco.csv")
        loadshape_flat = str(list(df_1['Curva']))[1:-1]
        loadshape_pv = str(list(df_2['Curva']))[1:-1]
        loadshape_bat = str(list(df_3['Curva']))[1:-1]
        hora = str(list(df_1['Hora']))[1:-1]

        arquivo.write(str("!Curve_Variations = {} {}".format(variations, "\n\n")))
        arquivo.write(str("New LoadShape.Flat_Curve Npts=96 Hour=({}) Mult=({}) {}".format(hora, loadshape_flat, "\n\n")))
        arquivo.write(str("New LoadShape.Station_Curve_PV Npts=96 Hour=({}) Mult=({}) {}".format(hora, loadshape_pv, "\n\n")))
        arquivo.write(str("New LoadShape.Station_Curve_PV_Bank Npts=96 Hour=({}) Mult=({}) {}".format(hora, loadshape_bat, "\n\n")))

        new_loadshape = list()
        dss.loadshapes_first()

        for p in range(dss.loadshapes_count()):
            k = 0
            while k < variations:
                k = k + 1
                loadshape_name = dss.loadshapes_read_name()
                p_curve = dss.loadshapes_read_p_mult()
                h_curve = dss.loadshapes_read_time_array()

                if "default" not in loadshape_name:
                    for i in range(len(p_curve)):
                        new_loadshape.append(cdf(p_curve[i]))
                    arquivo.write(str("New LoadShape.{}_{} Npts=288 mult=({}) hour=({}) {}"
                                      .format(str(loadshape_name), str(k), str(new_loadshape)[1:-1], str(h_curve)[1:-1], "\n\n")))

                new_loadshape = []

            dss.loadshapes_next()

        arquivo.close()


# Função para sotear novas curvas de carga para os consumidores
def sample_loadshapes(numcurv):
    dss.text("Redirect new_loadshapes.dss")
    dss.loads_first()
    for i in range(dss.loads_count()):
        sorteio = random.randint(1, numcurv)
        nome = dss.loads_read_name()
        loadshape = dss.loads_read_daily()
        if "station" not in nome:
            dss.text("Load." + nome + ".yearly=" + loadshape + "_" + str(sorteio))
        dss.loads_next()


# Função para elecionar lista de barras de média tensão trifásicas
def make_3phase_buslist():
    buses = dss.circuit_all_bus_names()
    my_buses = list()
    my_bus_voltage_dict = dict()

    for bus in buses:
        dss.circuit_set_active_bus(bus)
        if bus == "sourcebus":
            pass
        elif dss.bus_kv_base() >= 1.0 and len(dss.bus_nodes()) == 3:
            my_buses.append(bus)
            my_bus_voltage_dict[bus] = dss.bus_kv_base()

    return my_buses, my_bus_voltage_dict


# Função para selecionar lista de barras de baixa tensão
def make_1phase_buslist():
    buses = dss.circuit_all_bus_names()
    my_buses = list()
    my_bus_voltage_dict = dict()

    for bus in buses:
        dss.circuit_set_active_bus(bus)
        if bus == "sourcebus":
            pass
        elif dss.bus_kv_base() <= 1.0:
            my_buses.append(bus)
            my_bus_voltage_dict[bus] = dss.bus_kv_base()

    return my_buses, my_bus_voltage_dict


# Função para sortear a barra das estações de acordo com o cenário
def sample_stations(cenario, penetration_level):
    bus_list_3phase, my_bus_voltage_dict_3phase = make_3phase_buslist()  # Cria lista de barras trifásicas para sorteio
    bus_list_1phase, my_bus_voltage_dict_1phase = make_1phase_buslist()  # Cria lista de barras monofásicas para sorteio
    buses_mono = len(bus_list_1phase)
    buses_tri = len(bus_list_3phase)
    # total_power = get_loads_total_power()

    if cenario == 'base_case':
        pass

    elif cenario == 'monophasic_station':
        kv = my_bus_voltage_dict_1phase
        for i in range(int(round(buses_mono * penetration_level))):
            bus = random.sample(bus_list_1phase, 1)
            create_monophasic_station(str(i), bus[0], kv[bus[0]])
            dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus[0], 'red', 8, 15))

    elif cenario == 'triphasic_station':
        kv = my_bus_voltage_dict_3phase
        for i in range(int(round(buses_tri * (penetration_level/20)))):
            bus = random.sample(bus_list_3phase, 1)
            create_triphasic_station(str(i), bus[0], kv[bus[0]])
            dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus[0], 'red', 8, 15))

    elif cenario == 'renewable_station':
        kv = my_bus_voltage_dict_3phase
        for i in range(int(round(buses_tri * (penetration_level/20)))):
            bus = random.sample(bus_list_3phase, 1)
            create_renewable_station(str(i), bus[0], kv[bus[0]])
            dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus[0], 'red', 8, 15))

    else:
        kv_mono = my_bus_voltage_dict_1phase
        kv_tri = my_bus_voltage_dict_3phase
        for i in range(int((round(buses_mono * penetration_level * 0.6)))):
            bus = random.sample(bus_list_1phase, 1)
            create_monophasic_station(str(i), bus[0], kv_mono[bus[0]])
            dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus[0], 'red', 8, 15))
        for i in range(int(round(buses_tri * penetration_level * 0.015))):
            bus = random.sample(bus_list_3phase, 1)
            create_triphasic_station(str(i), bus[0], kv_tri[bus[0]])
            dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus[0], 'red', 8, 15))
        for i in range(int(round(buses_tri * penetration_level * 0.0005))):
            bus = random.sample(bus_list_3phase, 1)
            create_renewable_station(str(i), bus[0], kv_tri[bus[0]])
            dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus[0], 'red', 8, 15))

    dss.text("Interpolate")


# ---------------------------------------------------------------
# Definições de funções de escopo global
# ---------------------------------------------------------------


# Função para limpar do diretório os dados das simulações antigas
def clear_folder(folder):
    dir = "{}".format(folder)
    files = os.listdir(dir)
    for filename in files:
        if filename.endswith('.dss') or filename.endswith('.Txt') or filename.endswith('.dbl') or filename.endswith('.DSV'):
            pass
        elif filename.endswith('.csv') or filename.endswith('.CSV') or filename.endswith('.pdf'):
            os.unlink(dir + "/" + filename)
        else:
            shutil.rmtree(dir + "/" + filename)


# Função para verificar se o algoritmo troca corretamente a loadshapes das cargas na simulação
def check_loads():
    dss.loads_first()

    pmult = 'vazio'

    for i in range(400):
        dss.loads_next()

    loadshape = dss.loads_read_yearly()
    if len(loadshape) == 0:
        pass
    else:
        dss.loadshapes_write_name(loadshape)
        pmult = dss.loadshapes_read_p_mult()

    print(pmult)
    print('Loadshape = ', loadshape)


# Função para verificar se o sorteio das estações está ocorrendo corretamente
def check_station():
    dss.loads_first()

    for i in range(dss.loads_count()):
        nome = dss.loads_read_name()
        if 'station' in nome:
            loadshape = dss.loads_read_yearly()
            bar_ev = dss.dssproperties_read_value(str(dss.cktelement_all_property_names().index('bus1')+1))
            print('Nome = ', nome)
            print('Barra = ', bar_ev)
            print('Loadshape = ', loadshape)
        dss.loads_next()
