# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 23:50:18 2026

@author: DOM1804
"""
import csv
import math

AVG_EARTH_RADIUS_MILES = 3959.0

def read_csv_zipcodes(filename='zip_codes_states.csv'):
    '''
     @requires: a filename of the valid CSV-file with zipcodes data, 
       which must exist and be readable from the same directory as the executed .py file
       'zip_codes_states.csv' is a default name.
       Order of columns in the file is determined as: zip_code, latitude, longitude, city, state, county
       
     @modifies: None
     @effects: None
     
     @raises: FileNotFoundError if the file is not found in the mentioned directory,
       ValueError: if any errors arise during processing. 

     @returns: a tuple of 2 dictionaries - 
       1. a dictionary to search data by zipcode:
           { 5-digit zipcode : { 'latitude' : float,
                                 'longitude': float, 
                                 'city' : str,
                                 'state': str,
                                 'county': str
                                },
            ...}

       2. a dictionary to search data by a 'city-state' tuple:
           {
               (city, state) : [sorted list of indices],
               ...
            }
    '''
    by_zipcode_dict = {}
    by_city_state_dict = {}
    
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)            
            next(reader) #skip the line with headers
            for row in reader:
                #skip lines having one or more empty cells
                if not row or any(cell.strip().replace('"', '') == '' for cell in row):
                    continue 
                #skip lines where zipcode validation failed
                zipcode = row[0].strip().replace('"', '')
                if not zipcode.isdigit() or len(zipcode) != 5:
                    continue
                #convert coordinates
                try:
                    latitude = float(row[1].strip().replace('"', ''))
                    longitude = float(row[2].strip().replace('"', ''))
                except (ValueError, TypeError):
                    continue #skip row if coordinates cannot be converted into floats
                city, state, county = tuple(elem.strip().replace('"', '') for elem in row[3:])
                
                by_zipcode_dict[zipcode] = {'latitude': latitude,
                                            'longitude': longitude,
                                            'city': city,
                                            'state': state,
                                            'county': county
                                            }
                key = (city, state)
                if key not in by_city_state_dict:
                    by_city_state_dict[key] = set() #to remove duplicates
                by_city_state_dict[(city, state)].add(zipcode)
                
            for key in by_city_state_dict:
                by_city_state_dict[key] = sorted(by_city_state_dict[key])
            
            if not by_zipcode_dict or not by_city_state_dict: 
                raise ValueError('No valid lines found. Please, check the format of data supplied')
                
            return  by_zipcode_dict, by_city_state_dict
        
    except FileNotFoundError:
        raise FileNotFoundError(f'The file "{filename}" is not found in the current directory')
        
    except csv.Error as e:
        raise ValueError(f'An error occured while processing csv-file: {e}')
            
def lookup_by_zipcode(by_zipcode_dict, zip_code):
    '''
     @requires: 1. a dictionary to search data by zipcode:
         { 5-digit zipcode : { 'latitude' : float,
                               'longitude': float, 
                               'city' : str,
                               'state': str,
                               'county': str
                              },
          ...}
               2. a zipcode to search
     @modifies: None
     @effects: None     
     @raises: None
     @returns: returns a dictionary of parameters 'latitude', 'longitude', 'city', 'state', 'county',
               corresponding to the zipcode or None if no matches found.
    '''
    zip_code = zip_code.strip()
    return by_zipcode_dict.get(zip_code)

def lookup_by_city_state(by_city_state_dict, city, state):
    '''
     @requires: 1. a dictionary to search data by a 'city-state' tuple:
         {
             (city, state) : [sorted list of indices],
             ...
          }
               2. a city to search
               3. a state to search
     @modifies: None
     @effects: None     
     @raises: None
     @returns: - city, state with original formatting
              - a list of indices corresponding to the city-state combination 
       or empty list if no matches found.
    '''
    city = city.strip().lower().title()
    state = state.strip().upper() 
    key = (city, state)
    return city, state, by_city_state_dict.get(key, []) 

def decimal_to_dms(decimal_degrees, is_latitude):
    '''
    @requires: 1. coordinate value in decimal degrees
               2. is_latitude (0/1) - allows to distinguish between latitude(1) and longitude(0)
    @modifies: None
    @effects: None
    @raises: None 
    @returns: a string with coordinates in DMS format - DDD∘MM'SS.SS"X
        where DDD - degrees (3 digits with leading zeros),
             MM - minutes (2 digits with leading zeros),
             SS.SS - seconds (2 decimal places),
             X - direction (N/S for latitude, E/W for longitude).        
      e.g.
      decimal_to_dms(42.6737, True)  -> '042∘40'25.32"N'
      decimal_to_dms(-73.6088, False) -> '073∘36'31.68"W'
    '''
    #Determine direction by coordinate sign
    if is_latitude:
        direction = 'N' if decimal_degrees >= 0 else 'S'
    else:
        direction = 'E' if decimal_degrees >= 0 else 'W'
    
    #Use absolute value for subsequent calcs
    abs_value = abs(decimal_degrees)
    
    #DMS calcs
    degrees = int(abs_value)
    minutes = int((abs_value - degrees) * 60)
    seconds = ((abs_value - degrees) * 60 - minutes) * 60
    
    #padding with leading zeros
    return f"{degrees:03d}∘{minutes:02d}'{seconds:.2f}\"{direction}"

def handle_loc(by_zipcode_dict, zip_code):
    '''
    @requires: 1. a dictionary to search data by zipcode:
        { 5-digit zipcode : { 'latitude' : float,
                              'longitude': float, 
                              'city' : str,
                              'state': str,
                              'county': str
                             },
         ...}
              2. a zipcode 
    @modifies: processes 'loc' command (find location by a zipcode)
    @effects: 1. calls a 'lookup_by_zipcode' function to get the info about zipcode
              2. calls a decimal_to_dms func to format the info about coordinates
              3. prints out the information about zipcode with predefined formatting
              4. if empty output is received, prints a notification of error to console 
    @raises: None 
    @returns: None
    '''
    zip_code = zip_code.strip()
    record = lookup_by_zipcode(by_zipcode_dict, zip_code)
    
    if record is None:
        print("Invalid ZIP Code: " + zip_code)
        return
    
    lat_dms = decimal_to_dms(record['latitude'], True)
    lon_dms = decimal_to_dms(record['longitude'], False)
    county_str = record['county'] + " county" if record['county'] else "unknown county"
    
    print("ZIP Code " + zip_code + " is in " + record['city'] + ", " + record['state'] + ", " + county_str + ",")
    print("coordinates: (" + lat_dms + "," + lon_dms + ")")

def handle_zip(by_city_state_dict, city, state):
    '''
    @requires: 1. a dictionary to search data by a 'city-state' tuple:
        {
            (city, state) : [sorted list of indices],
            ...
         }
              2. a city to search
              3. a state to search
    @modifies: processes 'zip' command
    @effects: 1. calls a 'lookup_by_city_state' function and prints out its output to console
              2. if empty output is received, prints a notification of error to console 
    @raises: None
    @returns: None
    '''
    city = city.strip()
    state = state.strip()
    city_orig, state_orig, zips = lookup_by_city_state(by_city_state_dict, city, state)
    
    if not zips:
        print("No ZIP Codes found for " + city + ", " + state)
    else:
        zips_str = ", ".join(zips)
        print("The following ZIP Code(s) found for " + city_orig + ", " + state_orig + ": " + zips_str)              

def haversine_distance(lat1, lon1, lat2, lon2):
    '''
    @requires: coordinates corresponding to 2 zipcode locations (floats)
    @modifies: None
    @effects: None  
    @raises: None
    @returns: distance between zipcode locations in miles
      Geodesic distance is calculated using haversine formula (https://en.wikipedia.org/wiki/Haversine_formula)
    '''
    #convert degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    #haversine formula
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2   
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return AVG_EARTH_RADIUS_MILES * c

def handle_dist(by_zipcode_dict, zip1, zip2):
    '''
    @requires: 1. a dictionary to search data by zipcode:
        { 5-digit zipcode : { 'latitude' : float,
                              'longitude': float, 
                              'city' : str,
                              'state': str,
                              'county': str
                             },
         ...}
              2. a zipcode 1
              3. a zipcode 2
    @modifies: processes 'dist' command
    @effects: 1. calls 'lookup_by_zipcode' func to obtain the coordinates of zip1 and zip2
              2. calls haversine_distance func to obtain the geodesic distance
              3. prints out the distance to console or shows a notification of error, if at least one of the zipcodes is not found   
    @raises: None
    @returns: None

    '''    
    zip1 = zip1.strip()
    zip2 = zip2.strip()
    
    record1 = lookup_by_zipcode(by_zipcode_dict, zip1)
    if record1 is None:
        print("Invalid ZIP Code: " + zip1)
        return #early exit from handle_dist, the code below will not be executed
    
    record2 = lookup_by_zipcode(by_zipcode_dict, zip2)
    if record2 is None:
        print("Invalid ZIP Code: " + zip2)
        return #early exit from handle_dist, the code below will not be executed
    
    distance = haversine_distance(
        record1['latitude'], record1['longitude'],
        record2['latitude'], record2['longitude']
    )
    
    print(f"The distance between {zip1} and {zip2} is {distance:.2f} miles")
                    
def main():
    '''
    @requires: None
    @modifies: launches a REPL-interface of the program
    @effects: 1. loads data from 'zip_codes.csv'
              2. enters a loop of command processing:
                  -'loc': location by a zipcode
                  -'zip': zipcodes by a 'city-state' combination
                  -'dist': calculation of distance between 2 zipcodes
                  -'end': program exit
    @raises: None 
    @returns: None
    '''
    #data upload
    try:
        by_zipcode_dict, by_city_state_dict = read_csv_zipcodes()
        print("Loaded " + str(len(by_zipcode_dict)) + " ZIP codes")
        print()
    except Exception as e:
        print("An error occured during file upload: " + str(e))
        return
    
    #REPL
    while True:
        try:
            command = input("Command ('loc', 'zip', 'dist', 'end') => ").strip().lower()
            print(command)
            
            if command == 'end':
                print("Done")
                break
            elif command == 'loc':
                zip_code = input("Enter a ZIP Code to lookup => ").strip()
                print(zip_code)
                handle_loc(by_zipcode_dict, zip_code)
            elif command == 'zip':
                city = input("Enter a city name to lookup => ").strip()
                print(city)
                state = input("Enter the state name to lookup => ").strip()
                print(state)
                handle_zip(by_city_state_dict, city, state)
            elif command == 'dist':
                zip1 = input("Enter the first ZIP Code => ").strip()
                print(zip1)
                zip2 = input("Enter the second ZIP Code => ").strip()
                print(zip2)
                handle_dist(by_zipcode_dict, zip1, zip2)
            else:
                print("Invalid command, ignoring")
        except (KeyboardInterrupt, EOFError):
            print("\nDone")
            break
        except Exception as e:
            print("An error occured during command execution: " + str(e))


if __name__ == "__main__":
    main()        
            
            
    



