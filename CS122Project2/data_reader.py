import pandas as pd
import csvkit
import csv
import math

#range = '''10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 10012, 10013, 10014, 10015, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10041, 10044, 10045, 10048, 10055, 10065, 10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10128, 10152, 10153, 10154, 10162, 10165, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282, 10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 11001, 11003, 11004, 11005, 11040, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211, 11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 11231, 11232, 11233, 11234, 11235, 11236, 11237, 11238, 11239, 11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694, 11697'''
#zip_list = range.split(', ')
# valid_list = []
# for z in zip_list:
#     valid_list.append(int(z))
# print valid_list
# print (valid_list.__contains__(11219))
valid_zip_range = '10001 to 11697'

# used following link to get valid zip codes in NYC.
# link : https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm
# created NY_ZIP_CODES list from the above link
NY_ZIP_CODES = [10453, 10457, 10460,10458, 10467, 10468,10451, 10452, 10456,10454, 10455, 10459, 10474,10463, 10471,10466, 10469, 10470, 10475,10461, 10462,10464, 10465, 10472, 10473,11212, 11213, 11216, 11233, 11238,11209, 11214, 11228,11204, 11218, 11219, 11230,11234, 11236, 11239,11223, 11224, 11229, 11235,11201, 11205, 11215, 11217, 11231,11203, 11210, 11225, 11226,11207, 11208,11211, 11222,11220, 11232,11206, 11221, 11237,10026, 10027, 10030, 10037, 10039,10001, 10011, 10018, 10019, 10020, 10036,10029, 10035,10010, 10016, 10017, 10022,10012, 10013, 10014,10004, 10005, 10006, 10007, 10038, 10280,10002, 10003, 10009,10021, 10028, 10044, 10065, 10075, 10128,10023, 10024, 10025,10031, 10032, 10033, 10034, 10040,11361, 11362, 11363, 11364,11354, 11355, 11356, 11357, 11358, 11359, 11360,11365, 11366, 11367,11412, 11423, 11432, 11433, 11434, 11435, 11436,11101, 11102, 11103, 11104, 11105, 11106,11374, 11375, 11379, 11385,11691, 11692, 11693, 11694, 11695, 11697,11004, 11005, 11411, 11413, 11422, 11426, 11427, 11428, 11429,11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421,11368, 11369, 11370, 11372, 11373, 11377, 11378,10302, 10303, 10310,10306, 10307, 10308, 10309, 10312,10301, 10304, 10305,10314]

# read txt file into dataframe
df = pd.read_csv('data.txt', encoding='latin-1')

# drop null zipcodes and drop duplicates
df = df.dropna(subset=['ZIPCODE'])
df.drop_duplicates(inplace=True)


# drop rows where zipcode is not NY_ZIP_CODES
# created df['VALID'] additional column and then dropped rows where df['VALID'] value is 'not valid'
def func(row):
    if math.isnan(row):
        print "THIS IS NAN"
    else:
        code = int(row)
        #print zipcode
        #if (code >= 10001) and (code <= 11697):
        if code in NY_ZIP_CODES:
            return 'valid'
            #print 'valid'
        else:
            return 'not valid'

df['VALID'] = df['ZIPCODE'].apply(func)
not_valid_rows = df[df['VALID'] == 'not valid']
df = df.drop(not_valid_rows.index, axis=0)


# group by camis and keep the rows with latest inspection date.
camis_group=df.groupby(['CAMIS'])
l = []

for group, gd in camis_group:
    x = gd.sort_values(["INSPDATE"], ascending=False)
    #x = group.sort('INSPDATE')
    l.append(x.iloc[0])
    # if (gd['INSPDATE']).max():
    #     date = (gd['INSPDATE']).max()

# create dataframe from list l. list l is all the CAMIS's with latest inspection date
final_df = pd.DataFrame(data=l)

r = ('zipcode', 'mean score', 'number of restaurants')
#take final_df and group by zipcode
# if group from groupby result is greater than 100, create a tuple with values from r
required_tuple = []
zip_group=final_df.groupby(['ZIPCODE'])

for group, zg in zip_group:
    tup = ()
    zipcode = group
    number_of_restaurants = zg.size
    mean_score = zg['SCORE'].mean()
    #print number_of_restaurants
    if  number_of_restaurants > 100:
        tup = (zipcode,mean_score,number_of_restaurants)
        required_tuple.append(tup)

# sorting tuples
required_tuple.sort(key=lambda tup: tup[1])

for t in required_tuple:
    print (t)

# creating csv file from the required_tuple list to do the map plot on carto website
with open('tup_shakti.csv','wb') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['ZIPCODE','AVG', 'NUMBER OF RESTAURANTS', 'COUNTRY'])
    for row in required_tuple:
        r = row + ('US',)
        csv_out.writerow(r)




