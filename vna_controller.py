############################################### INFO ###########################################################################

"""
Nom du fichier : vna_controlleur.py
Auteur : COLLIN Florian
Github : https://github.com/FlorianCollin
Mail : flocol1302@gmail.com
Date de création : Juin 2023

Ce fichier "vna_controlleur.py" contient des classes qui vous permettent de contrôler un analyseur de réseau vectoriel (VNA) à partir de votre script Python. Vous pouvez l'ajouter à votre dossier de projet pour obtenir un accès facile aux fonctionnalités de contrôle du VNA.

La classe RFConfiguration vous permet de définir la configuration des paramètres RF tels que la fréquence centrale, la plage de fréquences, la puissance, le nombre de points, le facteur de moyennage et la bande passante IF.

La classe VNAController gère la communication avec le VNA en utilisant la bibliothèque pyvisa pour établir une connexion via le protocole TCP/IP. Elle offre des méthodes pour configurer les paramètres RF, effectuer des mesures, récupérer les données, et plus encore
"""

############################################### DEPENDANCE ######################################################################

import pyvisa
import numpy as np
# import pour les exemples de code à la fin
import matplotlib.pyplot as plt

############################################# CLASSES DE CONFIGURATIONS #########################################################

# Les classes RFConfiguration et RFConfigurationSS permettent de regrouper les variables de configuration de notre VNA (Vector Network Analyzer).
# Nous utilisons ces classes avec les méthodes set_RFConfig() ou set_RFConfigSS() de la classe VNAController. Ainsi, toute la configuration est modifiée dans le VNA.

############################################### RF CONFIGURATION (central & span) ###############################################

class RFConfiguration:
    def __init__(self, central_frequency=8e6, frequency_span=1e6, power=-10, num_points=1000, averaging_factor=0, if_band=1000, smoothing = 0):
        self.central_frequency = central_frequency
        self.frequency_span = frequency_span
        self.power = power
        self.num_points = num_points
        self.averaging_factor = averaging_factor
        self.if_band = if_band
        self.smoothing = smoothing


############################################### RF CONFIGURATION (start & stop) ##################################################

class RFConfigurationSS:
    def __init__(self, start_frequency=8e6, stop_frequency=1e6, power=-10, num_points=1000, averaging_factor=0, if_band=1000, smoothing = 0):
        self.start_frequency = start_frequency
        self.stop_frequency = stop_frequency
        self.power = power # TODO: Implementer power
        self.num_points = num_points
        self.averaging_factor = averaging_factor
        self.if_band = if_band
        self.smoothing = smoothing

############################################### VNA CONTROLLER ###################################################################


class VNAController:
    """
    Classe VNAController :
    Cette classe représente un contrôleur pour un analyseur de réseau vectoriel (VNA - Vector Network Analyzer) PLANAR TR1300/1.
    Elle permet de configurer et de contrôler les paramètres du VNA, tels que les fréquences centrales, les plages de fréquences, le nombre de points, la largeur de bande, et d'autres paramètres essentiels.
    De plus, elle offre des méthodes pour récupérer les données mesurées par le VNA, effectuer des opérations de déclenchement, réaliser des moyennes, appliquer des filtres de lissage, et gérer le format de transfert des données.
    Cette classe facilite l'automatisation des mesures et permet une intégration aisée avec d'autres systèmes ou logiciels.
    
    ATTENTION:
    - Assurez-vous d'avoir le logiciel TRVNA (https://coppermountaintech.com/download-free-vna-software/) ainsi que le module pyvisa (pip install pyvisa) installés.
    - Assurez-vous d'avoir lancé TRVNA et activé la connexion réseau (System -> Misc Setup -> Network Setup -> TCP SOCKET ON).
    - Si le numéro du port est différent de 5025, veuillez fournir l'argument address='TCPIP0::localhost::{votre numéro de port}::SOCKET' lors de l'instanciation de la classe.

    Pour tout problème, veuillez vous référer à la documentation technique du VNA et de TRVNA (https://coppermountaintech.com/help/).
    """

    def __init__(self, address='TCPIP0::localhost::5025::SOCKET'):
        rm = pyvisa.ResourceManager()
        try:
            self.vna = rm.open_resource(address)
        except pyvisa.errors.VisaIOError as e:
            print(f"Erreur lors de l'ouverture de la ressource : {e}")
            exit(1)

        self.vna.read_termination = '\n'
        self.vna.write_termination = '\n'
        self.vna.timeout = 10000000 # Définit le délai d'attente. Si le {temps de mesure} est supérieur à {timeout}, alors il y aura une interruption du programme.
        print("VNAController INIT")

    ########## METHODES ##########

    # FREQ CENT
    def set_central_frequency(self, center_freq):
        command = f":SENSe:FREQuency:CENTer {center_freq}"
        self.vna.write(command)

    def get_central_frequency(self):
        command = ":SENSe:FREQuency:CENTer?"
        out = self.vna.query(command)
        print("CENTER :", out)
        return out
    
    def central_frequency(self, center_freq):
        self.set_central_frequency(center_freq)
        out = self.get_central_frequency()
        return out

    # FREQ SPAN
    def set_frequency_span(self, frequency_span):
        command = f"SENSe:FREQuency:SPAN {frequency_span}"
        self.vna.write(command)

    def get_frequency_span(self):
        command = ":SENSe:FREQuency:SPAN?"
        out = self.vna.query(command)
        print("SPAN :", out)
        return out
    
    def frequency_span(self, frequency_span):
        self.set_frequency_span(frequency_span)
        out = self.get_frequency_span()
        return out
    
    # START FREQ
    def set_start_frequency(self, start_frequency):
        command = f"SENSe:FREQuency:STARt {start_frequency}"
        self.vna.write(command)

    # STOP FREQ
    def set_stop_frequency(self, stop_frequency):
        command = f"SENSe:FREQuency:STOP {stop_frequency}"
        self.vna.write(command)
    
    # NB POINT
    def set_num_points(self, number):
        command = f"SENSe:SWEep:POINts {number}"
        self.vna.write(command)

    def get_num_points(self):
        command = "SENSe:SWEep:POINts?"
        out = self.vna.query(command)
        print("POINTS :", out)
        return out
    def num_points(self, number):
        self.set_num_points(number)
        out = self.get_num_points()
        return out

    # CORR_STATE
    def set_corr_state(self, state):
        command = f"SYSTem:CORRection:STATe {state}"
        self.vna.write(command)

    def get_corr_state(self):
        command = "SYSTem:CORRection:STATe?"
        out = self.vna.query(command)
        print("CORR_STATE :", out)
        return out
    def corr_state(self, state):
        self.set_corr_state(state)
        out = self.get_corr_state()
        return out

    # IFBDW
    def set_if_band(self, value):
        command = f"SENSe:BANDwidth {value}"
        self.vna.write((command))
    def get_if_band(self):
        command = "SENSe:BANDwidth?"
        out = self.vna.query(command)
        print("IF BAND", out)
        return out
    
    def if_band(self, value):
        self.set_if_band(value)
        out = self.get_if_band()
        return out

    # AVG
    def set_averaging(self, avg_factor):
        self.vna.write("SENSe:AVERage:STATe 1")
        command = f":SENSe:AVERage:COUNt {avg_factor}"
        print("AVG state :", self.vna.query("SENSe:AVERage:STATe?"))
        print("AVG factor :", self.vna.query("SENSe:AVERage:COUNt?"))
        self.vna.write(command)
    
    def reset_averaging(self):
        command = "SENSe:AVERage:CLEar"
        self.write(command)

    # AUTO SCALE
    def auto_scale(self):
        self.vna.write("DISPlay:WINDow:TRACe:Y:AUTO")

    # TRIGGER
    def set_trigger_to_hold(self):
        self.vna.write("TRIGger:WAIT HOLD")

    # GET FREQUENCY 
    def get_frequency(self):
        F = self.vna.query("SENSe:FREQuency:DATA?")
        Ff = []
        Fdata = F.split(",")
        for data in Fdata:
            Ff.append(float(data))
        return np.array(Ff)
    
    def get_frequency_real32(self): # MODE REAL32
        values = self.vna.query_binary_values("SENSe:FREQuency:DATA?", datatype='d', is_big_endian=True)
        filtered_values = [value for value in values if value != 0.0]
        return np.array(filtered_values)

    # GET DATA
    def get_data(self):
        Y = self.vna.query("CALCulate:DATA:FDATa?")
        data_list = Y.split(",")
        Yf = []
        for data in data_list:
            if data != "+0.000000000E+00":
                Yf.append(float(data))
        return np.array(Yf)
    
    def get_complex_data(self):
        Y = self.vna.query("CALCulate:DATA:FDATa?")
        data_list = Y.split(",")
        Yf = []
        for k in range(0, len(data_list), 2):
                Yf.append(complex(float(data_list[k]), float(data_list[k+1])))
        return np.array(Yf, dtype=complex)

    def get_Z11(self):
        self.set_format("SMITh")
        self.set_trigger_soure("BUS")
        self.set_trigger_single()
        self.opc()
        S11 = self.get_complex_data()
        Z11 = []
        for s11 in S11:
            z11 = (1 + s11) / (1 - s11)
            Z11.append(z11)
        return Z11

    def get_data_real32(self): # MODE REAL32
        values = self.vna.query_binary_values("CALCulate:DATA:FDATa?", datatype='d', is_big_endian=True)
        return np.array(values)
    
    ###### SET VNA CONFIG ######

    def set_RFConfig(self, config: RFConfiguration):
        self.set_central_frequency(config.central_frequency)
        self.set_frequency_span(config.frequency_span)
        self.set_num_points(config.num_points)
        self.set_if_band(config.if_band)
        if (config.smoothing != 0):
            self.set_smoothing(state=1, value=config.smoothing)
        else:
            self.set_smoothing(state=0)

    def set_RFConfigSS(self, config: RFConfigurationSS):
        self.set_start_frequency(config.start_frequency)
        self.set_stop_frequency(config.stop_frequency)
        self.set_num_points(config.num_points)
        self.set_if_band(config.if_band)
        if (config.smoothing != 0):
            self.set_smoothing(state=1, value=config.smoothing)
        else:
            self.set_smoothing(state=0)

    # SET TRIGGER

    def set_trigger_soure(self, option="BUS", print_option = False):
        """
        INTernal Internal
        EXTernal External (hardware trigger input; except TR1300/1 model)
        BUS Bus (program)
        """
        command = f"TRIGger:SOURce {option}"
        self.vna.write(command)
        out = self.vna.query("TRIGger:SOURce?")
        if (print_option):
            print("trigger source :", out)
        return out

    def set_trigger_soure_internal(self, print_option = False):
        option = "INTernal"
        command = f"TRIGger:SOURce {option}"
        self.vna.write(command)
        out = self.vna.query("TRIGger:SOURce?")
        if (print_option):
            print("trigger source :", out)
        return out

    def set_continous_trigger(self, mode, print_option = False):
        command = f"INITiate:CONTinuous {mode}"
        self.vna.write(command)
        out = self.vna.query("INITiate:CONTinuous?")
        if (print_option):
            print("continuous Trigger", out)
        return out
    
    def get_trigger_status(self):
        """
        HOLD Stop
        MEAS Measurement Cycle
        WAIT Waiting for trigger
        """
        out = self.vna.query("TRIGger:STATus?")
        print("trigger status :", out)
        return out
    
    def set_trigger_single(self):
        # Generates a trigger signal and initiates a sweep
        command = "TRIGger:SINGle"
        self.vna.write(command)

    def opc(self):
        command = "*OPC?"
        out = self.vna.query(command)
        return out
    
    def acquisition(self):
        self.set_trigger_soure("BUS")
        self.set_trigger_single()
        self.opc()
        Y = self.get_data()
        return Y
    
    def acquisition_real32(self): # MODE REAL32
        self.set_trigger_soure("BUS")
        self.set_trigger_single()
        self.opc()
        Y = self.get_data_real32()
        return Y
    
    def acquisition_complexe(self):
        #self.set_format("SMITh")
        self.set_trigger_soure("BUS")
        self.set_trigger_single()
        self.opc()
        S11 = self.get_complex_data()
        return S11
    
    # SMOOTHING
    def set_smoothing(self, state = 1, value = 2):
        command1 = f"CALCulate:SMOothing {state}"
        self.vna.write(command1)
        if (state == 1):
            command2 = f"CALCulate:SMOothing:APERture {value}"
            self.vna.write(command2)

    # SET TRANSFERT FORMAT 
    def set_transfer_format(self, format = "REAL32"):
        """
        Une fois le format passé en real32, il faut faire attention à utiliser les méthodes qui ont "*_real32()" dans leur nom, sinon il y aura une erreur.
        De plus, je n'ai pas constaté d'écart significatif qui me ferait dire qu'il faut privilégier ce transfert par rapport à l'ASCII.
        """
        command = f"FORMat:DATA {format}"
        self.vna.write(command)

    def set_invisible_mode(self, mode):
        #Send “SYST:HIDE” to turn on Invisible Mode and send “SYST:SHOW” to turn it off.
        if (mode == 1):
            self.vna.write("SYST:HIDE")
        else:
            self.vna.write("SYST:SHOW")

    def set_format(self, format="MLOGarithmic"): # Fonctionne
        """
        MLOGarithmic Logarithmic magnitude
        PHASe Phase
        GDELay Group delay time
        SLINear Smith chart format (Lin)
        SLOGarithmic Smith chart format (Log)
        SCOMplex Smith chart format (Real/Imag)
        SMITh Smith chart format (R + jX)
        SADMittance Smith chart format (G + jB)
        PLINear Polar format (Lin)
        PLOGarithmic Polar format (Log)
        POLar Polar format (Real/Imag)
        MLINear Linear magnitude
        SWR Voltage standing wave ratio
        REAL Real part
        IMAGinary Imaginary part
        UPHase Expanded phase
        """
        command = f"CALCulate:FORMat {format}"
        self.vna.write(command)
        out = self.vna.query("CALCulate:FORMat?")
        print("Format :", out)
        return out


    
    


