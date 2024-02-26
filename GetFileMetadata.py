
import csv
import math
from datetime import date

filename = 'Data8277.csv'

def try_cast(val, type_to_cast):
    try:
        return type_to_cast(val)
    except (ValueError, TypeError):
        return None

def test_types(val):
    if (try_cast(val, int)) != None:
        return 'int'
    else: 
        if(try_cast(val, float)) != None:
            return 'decimal'
        else:
            if(try_cast(val, date.fromisoformat)) != None:
                return 'datetime'
            else:
                return 'varchar'

def set_varchar_length(val):
    return math.ceil(len(val) / 50) * 50

def set_decimal_precision(val):
    parts = val.split('.')
    precision = len(parts[0])
    scale = len(parts[1]) if len(parts) > 1 else 0
    return precision, scale

metadatadict = {}

with open(filename) as inputcsv:
    csvreader = csv.DictReader(inputcsv)
    
    fieldnames_dict = {fieldname: (None, 0, (0, 0)) for fieldname in csvreader.fieldnames}

    print(fieldnames_dict)
    
    rownum = 0

    for row in csvreader:
        for colname in csvreader.fieldnames:
            
            val = row[colname]
            valtype = test_types(val)
            existingtype, maxlength, (precision, scale) = fieldnames_dict[colname]
            print('Evaluating row:' + rownum.__str__())

            if(valtype != existingtype):
                if(existingtype == None):
                    if (valtype == 'varchar'):
                        fieldnames_dict[colname] = valtype, set_varchar_length(val), (None, None)
                    else:
                        if (valtype == 'decimal'):
                            fieldnames_dict[colname] = valtype, None, set_decimal_precision(val)
                        else: 
                            fieldnames_dict[colname] = valtype, None, (None, None)
                else:
                    fieldnames_dict[colname] = 'varchar', set_varchar_length(val), (None, None) #probably the safest option although I guess an int could be made a decimal                                   
            else:       #for varchar and decimal: if the type is the same recheck the length
                if(valtype == 'varchar'):
                    if len(val) > maxlength:
                        fieldnames_dict[colname] = valtype, set_varchar_length(val), (None, None)
                    else:
                        fieldnames_dict[colname] = valtype, maxlength, (None, None)
                if(valtype == 'decimal'):
                    precision, scale = set_decimal_precision(val)
                    if precision > fieldnames_dict[colname][2][0] or scale > fieldnames_dict[colname][2][1]:
                        fieldnames_dict[colname] = valtype, None, (precision, scale)
                    else:
                        fieldnames_dict[colname] = valtype, None, fieldnames_dict[colname][2]
        rownum += 1

for c, d in fieldnames_dict.items():
   print(c, d)

with open('metadata.csv', 'w', newline='') as metadatacsv:
    writer = csv.writer(metadatacsv)
    writer.writerow(['ColName', 'DataType', 'MaxLength', 'Precision', 'Scale'])
    for colname, (datatype, maxlength, (precision, scale)) in fieldnames_dict.items():
        writer.writerow([colname, datatype, maxlength, precision, scale])