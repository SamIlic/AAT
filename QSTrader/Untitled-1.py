# Function 1
# Insert getMaximumLand(stateName1, stateName2, stateName3) function here
# Step1: Retrieve area values for all 3 states using getArea function and assign it to variables.
# Step2: Use max() function to calculate the max value and store it as a variable
# Step3: Return the max value that you calculated.
# Note: You shouldn't use print in this function.
def getMaximumLand(stateName1, stateName2, stateName3):
    # 1) Retrieve area values for all 3 states using getArea function and assign it to variables.
    area_state1 = getArea(stateName1)
    area_state2 = getArea(stateName2)
    area_state3 = getArea(stateName3)
    # 2) Use max() function to calculate the max value and store it as a variable
    max_State_Area = max(area_state1,area_state2,area_state3)



###########################################################################
###########################################################################
###########################################################################
###########################################################################





