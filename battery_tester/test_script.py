from battery_test_jig import CHARGERS, BatteryTestJig

BTJ = BatteryTestJig(CHARGERS)

BTJ.setup_one_charger(3, False, False) #Succeeds


#Next session, finish testing everything to make sure your imports are correct.
#Then make a script that will charge a battery and take readings over time, test it for 5 min
#fill the CSV file, then go on from there.


