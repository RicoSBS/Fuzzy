import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import simplejson
from urllib.request import FancyURLopener
from datetime import datetime


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

        home_coord = "-7.7545807,110.37433493" # Home
        work_coord2 = str(self.path) # Work

        lat = ""
        lon = ""
        for i in range(0,len(work_coord2)):
            if i >= 6 and i<=16:
                lat += work_coord2[i]
            elif i >= 22 and i<= 32:
                lon += work_coord2[i]
        #print(lat)
        #print(lon)

        #work_coord = lat,lon
        #print(work_coord)

        API1 = "AIzaSyCRXi115Ca-2IO6R03VpfYZq6ufvZ9rTcs"
        url_work2home = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + lat + "," + lon + "&destinations=" + home_coord + "&mode=driving&traffic_model=best_guess&departure_time=now&language=en-EN&sensor=false&key=" + API1

        class MyOpener(FancyURLopener):
            version = 'My new User-Agent'
        myopener = MyOpener()
        result_work2home = simplejson.load(myopener.open(url_work2home))
        driving_time_seconds_work2home = result_work2home['rows'][0]['elements'][0]['duration_in_traffic']['value']
        print(datetime.now().strftime('%Y-%m-%d %H:%M') + ";" + str(driving_time_seconds_work2home) + " seconds;" + "\n")
        
        target = open("Results.csv", 'a')
        target.write( datetime.now().strftime('%Y-%m-%d %H:%M') + ";" + str(driving_time_seconds_work2home) + ";"+ "\n")
        target.close()


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def Fuzzy():
	# The universe of variables and membership functions
	ETA = ctrl.Antecedent(np.arange(-1, 21, 0.1), 'ETA')
	DeltaT = ctrl.Antecedent(np.arange(-10, 20, 0.1), 'DeltaT')
	FLC1 = ctrl.Consequent(np.arange(18, 31, 0.1), 'FLC1')

	# MF

	ETA['SangatCepat'] = fuzz.trapmf(ETA.universe, [0, 2, 6, 8])
	ETA['Cepat'] = fuzz.trimf(ETA.universe, [6, 8, 10])
	ETA['Sedang'] = fuzz.trimf(ETA.universe, [8, 10, 12])
	ETA['Lambat'] = fuzz.trimf(ETA.universe, [10, 12, 14])
	ETA['SangatLambat'] = fuzz.trapmf(ETA.universe, [12, 14, 18, 20])

	DeltaT['NM'] = fuzz.trimf(DeltaT.universe, [-9, -6, -3])
	DeltaT['NS'] = fuzz.trimf(DeltaT.universe, [-6, -3, 0])
	DeltaT['Z'] = fuzz.trimf(DeltaT.universe, [-3, 0, 3])
	DeltaT['PS'] = fuzz.trimf(DeltaT.universe, [0, 3, 6])
	DeltaT['PM'] = fuzz.trimf(DeltaT.universe, [3, 6, 9])
	DeltaT['PL'] = fuzz.trimf(DeltaT.universe, [6, 9, 12])
	DeltaT['PB'] = fuzz.trimf(DeltaT.universe, [9, 12, 15])
	DeltaT['PVB'] = fuzz.trimf(DeltaT.universe, [12, 15, 18])

	FLC1['SangatSangatDingin'] = fuzz.trimf(FLC1.universe, [18, 19, 20])
	FLC1['SangatDingin'] = fuzz.trimf(FLC1.universe, [19, 20, 21])
	FLC1['Dingin'] = fuzz.trimf(FLC1.universe, [20, 21, 22])
	FLC1['Sejuk'] = fuzz.trimf(FLC1.universe, [21, 22, 23])
	FLC1['Sedang'] = fuzz.trimf(FLC1.universe, [22, 23, 24])


	# ETA.view()
	# DeltaT.view()
	# FLC1.view()


	"""
	==================
	DECLARE THE RULES
	==================
	"""

	rule1 = ctrl.Rule(DeltaT['NM'] & ETA['SangatCepat'], FLC1['Sedang'])
	rule2 = ctrl.Rule(DeltaT['NM'] & ETA['Cepat'], FLC1['Sedang'])
	rule3 = ctrl.Rule(DeltaT['NM'] & ETA['Sedang'], FLC1['Sedang'])
	rule4 = ctrl.Rule(DeltaT['NM'] & ETA['Lambat'], FLC1['Sedang'])
	rule5 = ctrl.Rule(DeltaT['NM'] & ETA['SangatLambat'], FLC1['Sedang'])

	rule6 = ctrl.Rule(DeltaT['NS'] & ETA['SangatCepat'], FLC1['Sedang'])
	rule7 = ctrl.Rule(DeltaT['NS'] & ETA['Cepat'], FLC1['Sedang'])
	rule8 = ctrl.Rule(DeltaT['NS'] & ETA['Sedang'], FLC1['Sedang'])
	rule9 = ctrl.Rule(DeltaT['NS'] & ETA['Lambat'], FLC1['Sedang'])
	rule10 = ctrl.Rule(DeltaT['NS'] & ETA['SangatLambat'], FLC1['Sedang'])

	rule11 = ctrl.Rule(DeltaT['Z'] & ETA['SangatCepat'], FLC1['Sejuk'])
	rule12 = ctrl.Rule(DeltaT['Z'] & ETA['Cepat'], FLC1['Sejuk'])
	rule13 = ctrl.Rule(DeltaT['Z'] & ETA['Sedang'], FLC1['Sejuk'])
	rule14 = ctrl.Rule(DeltaT['Z'] & ETA['Lambat'], FLC1['Sejuk'])
	rule15 = ctrl.Rule(DeltaT['Z'] & ETA['SangatLambat'], FLC1['Sejuk'])

	rule16 = ctrl.Rule(DeltaT['PS'] & ETA['SangatCepat'], FLC1['Dingin'])
	rule17 = ctrl.Rule(DeltaT['PS'] & ETA['Cepat'], FLC1['Dingin'])
	rule18 = ctrl.Rule(DeltaT['PS'] & ETA['Sedang'], FLC1['Dingin'])
	rule19 = ctrl.Rule(DeltaT['PS'] & ETA['Lambat'], FLC1['Sejuk'])
	rule20 = ctrl.Rule(DeltaT['PS'] & ETA['SangatLambat'], FLC1['Sejuk'])

	rule21 = ctrl.Rule(DeltaT['PM'] & ETA['SangatCepat'], FLC1['SangatDingin'])
	rule22 = ctrl.Rule(DeltaT['PM'] & ETA['Cepat'], FLC1['SangatDingin'])
	rule23 = ctrl.Rule(DeltaT['PM'] & ETA['Sedang'], FLC1['SangatDingin'])
	rule24 = ctrl.Rule(DeltaT['PM'] & ETA['Lambat'], FLC1['Dingin'])
	rule25 = ctrl.Rule(DeltaT['PM'] & ETA['SangatLambat'], FLC1['Dingin'])

	rule26 = ctrl.Rule(DeltaT['PL'] & ETA['SangatCepat'], FLC1['SangatDingin'])
	rule27 = ctrl.Rule(DeltaT['PL'] & ETA['Cepat'], FLC1['SangatDingin'])
	rule28 = ctrl.Rule(DeltaT['PL'] & ETA['Sedang'], FLC1['SangatDingin'])
	rule29 = ctrl.Rule(DeltaT['PL'] & ETA['Lambat'], FLC1['SangatDingin'])
	rule30 = ctrl.Rule(DeltaT['PL'] & ETA['SangatLambat'], FLC1['SangatDingin'])

	rule31 = ctrl.Rule(DeltaT['PB'] & ETA['SangatCepat'], FLC1['SangatSangatDingin'])
	rule32 = ctrl.Rule(DeltaT['PB'] & ETA['Cepat'], FLC1['SangatDingin'])
	rule33 = ctrl.Rule(DeltaT['PB'] & ETA['Sedang'], FLC1['SangatDingin'])
	rule34 = ctrl.Rule(DeltaT['PB'] & ETA['Lambat'], FLC1['SangatDingin'])
	rule35 = ctrl.Rule(DeltaT['PB'] & ETA['SangatLambat'], FLC1['SangatDingin'])

	rule36 = ctrl.Rule(DeltaT['PVB'] & ETA['SangatCepat'], FLC1['SangatSangatDingin'])
	rule37 = ctrl.Rule(DeltaT['PVB'] & ETA['Cepat'], FLC1['SangatSangatDingin'])
	rule38 = ctrl.Rule(DeltaT['PVB'] & ETA['Sedang'], FLC1['SangatDingin'])
	rule39 = ctrl.Rule(DeltaT['PVB'] & ETA['Lambat'], FLC1['SangatDingin'])
	rule40 = ctrl.Rule(DeltaT['PVB'] & ETA['SangatLambat'], FLC1['SangatDingin'])

	FLC1_ctrl = ctrl.ControlSystem(
	    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40])


	"""
	==========
	SIMULATION
	==========
	"""
	braking = ctrl.ControlSystemSimulation(FLC1_ctrl)

	braking.input['DeltaT'] = -6
	braking.input['ETA'] = driving_time_seconds_work2home/60 #convert to mins

	braking.compute()

	# print(braking.output['FLC1'])

	FLC1.view(sim=braking)

	# plt.show()



	"""
	=======================================================================================================
	MASUK ke FLC2
	=======================================================================================================
	"""


	TFout = ctrl.Antecedent(np.arange(18, 31, 0.1), 'FLC1_Input')
	DeltaT2 = ctrl.Antecedent(np.arange(-16, 20, 0.1), 'DeltaT2')
	FLC2 = ctrl.Consequent(np.arange(17, 31, 0.1), 'FLC2')

	# MF
	TFout['SangatSangatDingin'] = fuzz.trimf(TFout.universe, [18, 19, 20])
	TFout['SangatDingin'] = fuzz.trimf(TFout.universe, [19, 20, 21])
	TFout['Dingin'] = fuzz.trimf(TFout.universe, [20, 21, 22])
	TFout['Sejuk'] = fuzz.trimf(TFout.universe, [21, 22, 23])
	TFout['Sedang'] = fuzz.trimf(TFout.universe, [22, 23, 24])

	DeltaT2['NB'] = fuzz.trimf(DeltaT2.universe, [-15, -12, -9])
	DeltaT2['NL'] = fuzz.trimf(DeltaT2.universe, [-12, -9, -6])
	DeltaT2['NM'] = fuzz.trimf(DeltaT2.universe, [-9, -6, -3])
	DeltaT2['NS'] = fuzz.trimf(DeltaT2.universe, [-6, -3, 0])
	DeltaT2['Z'] = fuzz.trimf(DeltaT2.universe, [-3, 0, 3])
	DeltaT2['PS'] = fuzz.trimf(DeltaT2.universe, [0, 3, 6])
	DeltaT2['PM'] = fuzz.trimf(DeltaT2.universe, [3, 6, 9])
	DeltaT2['PL'] = fuzz.trimf(DeltaT2.universe, [6, 9, 12])
	DeltaT2['PB'] = fuzz.trimf(DeltaT2.universe, [9, 12, 15])
	DeltaT2['PVB'] = fuzz.trimf(DeltaT2.universe, [12, 15, 18])

	FLC2['SangatSangatDingin'] = fuzz.trimf(FLC2.universe, [18, 19, 20])
	FLC2['SangatDingin'] = fuzz.trimf(FLC2.universe, [19, 20, 21])
	FLC2['Dingin'] = fuzz.trimf(FLC2.universe, [20, 21, 22])
	FLC2['Sejuk'] = fuzz.trimf(FLC2.universe, [21, 22, 23])
	FLC2['Sedang'] = fuzz.trimf(FLC2.universe, [22, 23, 24])

	TFout.view()
	DeltaT2.view()
	FLC2.view()

	"""
	==================
	DECLARE THE RULES
	==================
	"""

	rule41 = ctrl.Rule(DeltaT2['NB'] & TFout['SangatSangatDingin'], FLC2['Dingin'])
	rule42 = ctrl.Rule(DeltaT2['NB'] & TFout['SangatDingin'], FLC2['Dingin'])
	rule43 = ctrl.Rule(DeltaT2['NB'] & TFout['Dingin'], FLC2['Dingin'])
	rule44 = ctrl.Rule(DeltaT2['NB'] & TFout['Sejuk'], FLC2['Sedang'])
	rule45 = ctrl.Rule(DeltaT2['NB'] & TFout['Sedang'], FLC2['Sedang'])

	rule46 = ctrl.Rule(DeltaT2['NL'] & TFout['SangatSangatDingin'], FLC2['Dingin'])
	rule47 = ctrl.Rule(DeltaT2['NL'] & TFout['SangatDingin'], FLC2['Dingin'])
	rule48 = ctrl.Rule(DeltaT2['NL'] & TFout['Dingin'], FLC2['Sejuk'])
	rule49 = ctrl.Rule(DeltaT2['NL'] & TFout['Sejuk'], FLC2['Sedang'])
	rule50 = ctrl.Rule(DeltaT2['NL'] & TFout['Sedang'], FLC2['Sedang'])

	rule51 = ctrl.Rule(DeltaT2['NM'] & TFout['SangatSangatDingin'], FLC2['Dingin'])
	rule52 = ctrl.Rule(DeltaT2['NM'] & TFout['SangatDingin'], FLC2['Dingin'])
	rule53 = ctrl.Rule(DeltaT2['NM'] & TFout['Dingin'], FLC2['Sejuk'])
	rule54 = ctrl.Rule(DeltaT2['NM'] & TFout['Sejuk'], FLC2['Sedang'])
	rule55 = ctrl.Rule(DeltaT2['NM'] & TFout['Sedang'], FLC2['Sedang'])

	rule56 = ctrl.Rule(DeltaT2['NS'] & TFout['SangatSangatDingin'], FLC2['SangatDingin'])
	rule57 = ctrl.Rule(DeltaT2['NS'] & TFout['SangatDingin'], FLC2['Dingin'])
	rule58 = ctrl.Rule(DeltaT2['NS'] & TFout['Dingin'], FLC2['Sejuk'])
	rule59 = ctrl.Rule(DeltaT2['NS'] & TFout['Sejuk'], FLC2['Sejuk'])
	rule60 = ctrl.Rule(DeltaT2['NS'] & TFout['Sedang'], FLC2['Sedang'])

	rule61 = ctrl.Rule(DeltaT2['Z'] & TFout['SangatSangatDingin'], FLC2['SangatSangatDingin'])
	rule62 = ctrl.Rule(DeltaT2['Z'] & TFout['SangatDingin'], FLC2['SangatDingin'])
	rule63 = ctrl.Rule(DeltaT2['Z'] & TFout['Dingin'], FLC2['Dingin'])
	rule64 = ctrl.Rule(DeltaT2['Z'] & TFout['Sejuk'], FLC2['Sejuk'])
	rule65 = ctrl.Rule(DeltaT2['Z'] & TFout['Sedang'], FLC2['Sedang'])

	rule66 = ctrl.Rule(DeltaT2['PS'] & TFout['SangatSangatDingin'], FLC2['SangatDingin'])
	rule67 = ctrl.Rule(DeltaT2['PS'] & TFout['SangatDingin'], FLC2['Dingin'])
	rule68 = ctrl.Rule(DeltaT2['PS'] & TFout['Dingin'], FLC2['Sejuk'])
	rule69 = ctrl.Rule(DeltaT2['PS'] & TFout['Sejuk'], FLC2['Sedang'])
	rule70 = ctrl.Rule(DeltaT2['PS'] & TFout['Sedang'], FLC2['Sedang'])

	rule71 = ctrl.Rule(DeltaT2['PM'] & TFout['SangatSangatDingin'], FLC2['SangatSangatDingin'])
	rule72 = ctrl.Rule(DeltaT2['PM'] & TFout['SangatDingin'], FLC2['SangatDingin'])
	rule73 = ctrl.Rule(DeltaT2['PM'] & TFout['Dingin'], FLC2['SangatDingin'])
	rule74 = ctrl.Rule(DeltaT2['PM'] & TFout['Sejuk'], FLC2['Dingin'])
	rule75 = ctrl.Rule(DeltaT2['PM'] & TFout['Sedang'], FLC2['Sejuk'])

	rule76 = ctrl.Rule(DeltaT2['PL'] & TFout['SangatSangatDingin'], FLC2['SangatSangatDingin'])
	rule77 = ctrl.Rule(DeltaT2['PL'] & TFout['SangatDingin'], FLC2['SangatDingin'])
	rule78 = ctrl.Rule(DeltaT2['PL'] & TFout['Dingin'], FLC2['SangatDingin'])
	rule79 = ctrl.Rule(DeltaT2['PL'] & TFout['Sejuk'], FLC2['Dingin'])
	rule80 = ctrl.Rule(DeltaT2['PL'] & TFout['Sedang'], FLC2['Sejuk'])

	rule81 = ctrl.Rule(DeltaT2['PB'] & TFout['SangatSangatDingin'], FLC2['SangatSangatDingin'])
	rule82 = ctrl.Rule(DeltaT2['PB'] & TFout['SangatDingin'], FLC2['SangatSangatDingin'])
	rule83 = ctrl.Rule(DeltaT2['PB'] & TFout['Dingin'], FLC2['SangatDingin'])
	rule84 = ctrl.Rule(DeltaT2['PB'] & TFout['Sejuk'], FLC2['Dingin'])
	rule85 = ctrl.Rule(DeltaT2['PB'] & TFout['Sedang'], FLC2['Dingin'])

	rule86 = ctrl.Rule(DeltaT2['PVB'] & TFout['SangatSangatDingin'], FLC2['SangatSangatDingin'])
	rule87 = ctrl.Rule(DeltaT2['PVB'] & TFout['SangatDingin'], FLC2['SangatSangatDingin'])
	rule88 = ctrl.Rule(DeltaT2['PVB'] & TFout['Dingin'], FLC2['SangatSangatDingin'])
	rule89 = ctrl.Rule(DeltaT2['PVB'] & TFout['Sejuk'], FLC2['SangatDingin'])
	rule90 = ctrl.Rule(DeltaT2['PVB'] & TFout['Sedang'], FLC2['SangatDingin'])


	FLC2_ctrl = ctrl.ControlSystem(
	    [rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60, rule61, rule62, rule63, rule64, rule65, rule66, rule67, rule68, rule69, rule70, rule71, rule72, rule73, rule74, rule75, rule76, rule77, rule78, rule79, rule80, rule81, rule82, rule83, rule84, rule85, rule86, rule87, rule88, rule89, rule90])

	"""
	==========
	SIMULATION
	==========
	"""
	braking2 = ctrl.ControlSystemSimulation(FLC2_ctrl)

	braking2.input['DeltaT2'] = 9
	braking2.input['FLC1_Input'] = braking.output['FLC1']

	braking2.compute()

	print(round(braking2.output['FLC2'],0))

	FLC2.view(sim=braking2)

	plt.show()

	"=================================================================================="


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')

    try:
        httpd.serve_forever()
        Fuzzy()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()


"================================================================================="




