
##########################################
##  Create Function to Check All These  ##
##  Dictionaries to Identify Delta_HPI  ##
##         Between Two Dates            ##
##########################################

## Note: Function takes Dates as Strings in format "YYYY-mm-dd"

## Purpose of function is to help estimate the current price of a property based on the sale price and sale date of the most recent sale
## Function takes the date of the most recent sale price and then calculates the difference in logs between the house price index (HPI) at the time of the last sale and the current HPI.  It then exponentiates this difference to find the factor by which to multiply the previous sale price by in order to generate the estimate of the current price.
## Lastly, the function tries a variety of methods to find the relevant HPI factors.  E.g. it first tries at the zip level, but if it can't find the right data, it tries the county-level HPI index, if it can't find that it tries CBSA, etc.
## WARNING: As is, this function returns a 0 if it fails to get enough data to perform this calculation.  You'll thus need to write in your own handling of these values (e.g. probably to throw out house sales if you fail to get an estimate like this), since a naive use of this would result in predictions of house price = 0 when insufficient data is found!

def Find_Delta_HPI_Factor(Previous_Date, Current_Date, StateFIPS, CountyFIPS, CBSA, Zip):

	Previous_Date = Previous_Date[:8] + '01' ## Standardize to first of the month.
	Current_Date = Current_Date[:8] + '01'

	## Make sure dates are legit and, e.g. the foreclosure date doesn't come before the previous sale date.
	if ((Previous_Date not in Legit_Dates) or (Current_Date not in Legit_Dates)):
		return 0
	try:
		Previous_Obj = Convert_to_DT(Previous_Date)
		Current_Obj  = Convert_to_DT(Current_Date)
		assert (Previous_Obj < Current_Obj)  ## If the previous date is not before the current date then something has gone wrong with the data.
	except Exception:
		return 0

	try:
		Previous_HPI_log = Zillow_Zip_Prices[(Zip, Previous_Date)]
		Current_HPI_log  = Zillow_Zip_Prices[(Zip, Current_Date)]
		Factor = exp(Current_HPI_log - Previous_HPI_log)
		return Factor
	except Exception:
		pass

	try:	
		Previous_HPI_log = Zillow_County_Prices[(StateFIPS, CountyFIPS, Previous_Date)]
		Current_HPI_log  = Zillow_Zip_Prices[(StateFIPS, CountyFIPS, Current_Date)]
		Factor = exp(Current_HPI_log - Previous_HPI_log)
		return Factor
	except Exception:
		pass

	try:
		Previous_HPI_log = Zillow_County_Prices[(StateFIPS, CountyFIPS, Previous_Date)]
		Current_HPI_log  = Zillow_Zip_Prices[(StateFIPS, CountyFIPS, Current_Date)]
		Factor = exp(Current_HPI_log - Previous_HPI_log)
		return Factor
	except Exception:
		pass

	try:	
		Previous_HPI_log = Zillow_CBSA_Prices[(CBSA, Previous_Date)]
		Current_HPI_log  = Zillow_CBSA_Prices[(CBSA, Current_Date)]
		Factor = exp(Current_HPI_log - Previous_HPI_log)
		return Factor
	except Exception:
		pass

	if Zip in Legit_Zips:  ## then if it wasn't found previously, it is probably in a very non-metro MSA.  But, if it is a non-legit Zip, then this is a less reasonable assumption, and the best guess is probably to use state prices.
		try:
			Previous_HPI_log = FHA_State_Prices[(StateFIPS, Previous_Date)]
			Current_HPI_log  = FHA_State_Prices[(StateFIPS, Current_Date)]
			Factor = exp(Current_HPI_log - Previous_HPI_log)
			return Factor		 
		except Exception:
			pass
	## there are one or two states that the FHA doesn't have non-metro prices for.  In these cases, just use Zillow state prices.  Likewise, if the prices haven't been found by anything previous, then try the Zillow state prices.  Thus, in either condition, the operation to use at this point is the same.

	try:
		Previous_HPI_log = Zillow_State_Prices[(StateFIPS, Previous_Date)]
		Current_HPI_log = Zillow_State_Prices[(StateFIPS, Current_Date)]
		Factor = exp(Current_HPI_log - Previous_HPI_log)
		return Factor	
	except Exception:
		pass

	return 0 ## If everything else has failed ...
