
## This script generates the dictionaries matching dates and locations to log values of the house price index (HPI).  These dictionaries are then used by the Find_Delta_HPI_Factor() function.

########################################
## Get List of all "Legit" Zip Codes  ##
########################################

# Here, "Legit" is defined as appearing in a crosswalk file


LegitZip_FileName = "/Users/Ohlrogge/Dropbox/School_Data/Demographic/Geographic Divisions - Names, FIPS Codes, Matching, Etc./Crosswalk Files/All_Legit_ZipCodes.txt"

with open(LegitZip_FileName, 'r') as f:
	Legit_Zips = {line.rstrip('\n') for line in f.readlines()}


######################################
##  Get List of all "Legit" Dates   ##
##  i.e. covered by Zillow and      ##
##  plausible given CoreLogic data  ##
######################################

LegitDates_FileName = "/Users/Ohlrogge/Dropbox/School_Data/Demographic/House Prices/ZillowPriceData/My Modified Zillow Datasets/Coverage_Dates.txt"

with open(LegitDates_FileName, 'r') as f:
	Legit_Dates = {line.rstrip('\n') for line in f.readlines()}

#############################
##  Create Dictionary for  ##
##    Zillow Zip HPI       ##
#############################

Zillow_Dir = "/Users/Ohlrogge/Dropbox/School_Data/Demographic/House Prices/ZillowPriceData/My Modified Zillow Datasets/"

print 'Reading in Zillow Zip Prices'
Zillow_Zip_FileName = "Zip_Zhvi_SingleFamilyResidence_Delta_Log_24.txt"
(a, b, c, CN_ZillowZip) = Get_CN(Zillow_Dir, Print = False, Condition = Zillow_Zip_FileName)

Zillow_Zip_Prices = {}
with open(Zillow_Dir + Zillow_Zip_FileName, 'r') as f:
	for idx, line in enumerate(f):
		if idx == 0: continue
		LineList = line.rstrip('\n').split('\t')

		HPI_log = try_float(LineList[CN_ZillowZip['Zhvi_log']])
		if HPI_log == 0: continue

		Zip = LineList[CN_ZillowZip['Zip']]
		Date = LineList[CN_ZillowZip['Date']]

		Zillow_Zip_Prices[(Zip, Date)] = HPI_log

print 'Created Zillow_Zip_Prices:  Zillow Zip Prices Found = %d' %len(Zillow_Zip_Prices)

################################
##  Create Dictionary for     ##
##    Zillow County HPI       ##
################################

print 'Reading in Zillow County Prices'
Zillow_County_FileName = "County_Zhvi_SingleFamilyResidence_Delta_Log_24.txt"
(a, b, c, CN_ZillowCounty) = Get_CN(Zillow_Dir, Print = False, Condition = Zillow_County_FileName)

Zillow_County_Prices = {}
with open(Zillow_Dir + Zillow_County_FileName, 'r') as f:
	for idx, line in enumerate(f):
		if idx == 0: continue
		LineList = line.rstrip('\n').split('\t')

		HPI_log = try_float(LineList[CN_ZillowCounty['Zhvi_log']])
		if HPI_log == 0: continue

		StateFIPS = LineList[CN_ZillowCounty['StateFIPS']]
		CountyFIPS = LineList[CN_ZillowCounty['CountyFIPS']]
		Date = LineList[CN_ZillowCounty['Date']]

		Zillow_County_Prices[(StateFIPS, CountyFIPS, Date)] = HPI_log

print 'Created Zillow_County_Prices:  Zillow County Prices Found = %d' %len(Zillow_County_Prices)



##############################
##  Create Dictionary for   ##
##    Zillow CBSA HPI       ##
##############################


print 'Reading in Zillow CBSA Prices'
Zillow_CBSA_FileName = "CBSA_Zhvi_SingleFamilyResidence_Delta_Log_24.txt"
(a, b, c, CN_ZillowCBSA) = Get_CN(Zillow_Dir, Print = False, Condition = Zillow_CBSA_FileName)

Zillow_CBSA_Prices = {}
with open(Zillow_Dir + Zillow_CBSA_FileName, 'r') as f:
	for idx, line in enumerate(f):
		if idx == 0: continue
		LineList = line.rstrip('\n').split('\t')

		HPI_log = try_float(LineList[CN_ZillowCBSA['Zhvi_log']])
		if HPI_log == 0: continue

		CBSA = LineList[CN_ZillowCBSA['CBSA']]
		Date = LineList[CN_ZillowCBSA['Date']]

		Zillow_CBSA_Prices[(CBSA, Date)] = HPI_log

print 'Zillow CBSA Prices Found = %d' %len(Zillow_CBSA_Prices)



###############################
##  Create Dictionary for    ##
##    Zillow State HPI       ##
###############################

print 'Reading in Zillow State Prices'
Zillow_State_FileName = "State_Zhvi_SingleFamilyResidence_Delta_Log_24.txt"
(a, b, c, CN_ZillowState) = Get_CN(Zillow_Dir, Print = False, Condition = Zillow_State_FileName)

Zillow_State_Prices = {}
with open(Zillow_Dir + Zillow_State_FileName, 'r') as f:
	for idx, line in enumerate(f):
		if idx == 0: continue
		LineList = line.rstrip('\n').split('\t')

		HPI_log = try_float(LineList[CN_ZillowState['Zhvi_log']])
		if HPI_log == 0: continue

		StateFIPS = LineList[CN_ZillowState['StateFIPS']]
		Date = LineList[CN_ZillowState['Date']]

		Zillow_State_Prices[(StateFIPS, Date)] = HPI_log

print 'Created Zillow_State_Prices: Zillow State Prices Found = %d' %len(Zillow_State_Prices)



###############################
##   Create Dictionary for   ##
##  FHA State Non-Metro HPI  ##
###############################

print 'Reading in FHA Non-Metro State Prices'

FHA_Dir = "/Users/Ohlrogge/Dropbox/School_Data/Demographic/House Prices/FHA House Prices/"
FHA_FileName = "FHA_nonMSA_House_Prices_With_Lags_All_Months.txt"

(a, b, c, CN_FHA) = Get_CN(FHA_Dir, Print = False, Condition = FHA_FileName)

FHA_State_Prices = {}
with open(FHA_Dir + FHA_FileName, 'r') as f:
	for idx, line in enumerate(f):
		if idx == 0: continue
		LineList = line.rstrip('\n').split('\t')

		HPI_log = try_float(LineList[CN_FHA['Index_log']])
		if HPI_log == 0: continue

		StateFIPS = LineList[CN_FHA['StateFIPS']]
		Date = LineList[CN_FHA['Date']]

		FHA_State_Prices[(StateFIPS, Date)] = HPI_log

print 'Created FHA_State_Prices: FHA State Prices Found = %d' %len(FHA_State_Prices)

