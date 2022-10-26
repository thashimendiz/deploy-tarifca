import pywebio
from pywebio.input import input, FLOAT
from pywebio.output import put_text, put_html, put_markdown, put_table
from pydoc import describe
from tkinter.font import names
import pandas as pd
import numpy as np
from tabulate import tabulate



def tariff():


    
# import Data Files
    data2019 = pd.read_excel("data_2019.xlsx")
    data2019 = pd.DataFrame(data2019)

    data2020 =  pd.read_excel("data_2020.xlsx")
    data2020  = pd.DataFrame(data2020)

    data2021 = pd.read_excel("data_2021.xlsx")
    data2021  = pd.DataFrame(data2021)

    data2022 = pd.read_excel("data_2022.xlsx")
    data2022  = pd.DataFrame(data2022)

    frames = [data2019, data2020, data2021, data2022]
    tariff_data = pd.concat(frames)


    year = input("Input Year：", type=FLOAT)
    HSCode = input("Input HS CODE：")
    cif = input("Input CIF Value：", type=FLOAT)
    quan= input("Input Quantity：", type=FLOAT)


    fil_tariff = tariff_data[(tariff_data['YEAR'] == year) &  (tariff_data['HS'] == HSCode)] 
# print(fil_tariff)


    Surcharge =  cif *  fil_tariff.iloc[0]['CD']
# print(Surcharge)

    PALevy = cif *  fil_tariff.iloc[0]['PAL']
# print(PALevy)



    if fil_tariff.iloc[0]['GD_Code'] == 1 :   CustomDuty = cif *  fil_tariff.iloc[0]['GD']
  
    else :   CustomDuty = quan *  fil_tariff.iloc[0]['GD']
    
  

# print(CustomDuty)
 
    if fil_tariff.iloc[0]['CESS_Code'] == "1" : CESSLevy =  (cif + (cif * 0.1)) *  fil_tariff.iloc[0]['CESS']
  
    else :  CESSLevy =  quan *  tariff_data.iloc[0]['CESS']
  
  
    if fil_tariff.iloc[0]['SPL_Code'] == "1" : ExciseDuty = ((cif + (cif * 0.15)) + CustomDuty + PALevy + CESSLevy )*  fil_tariff.iloc[0]['SPL']
  
    else :   ExciseDuty = quan *  fil_tariff.iloc[0]['SPL']
  
    
    VATax = ((cif + (cif * 0.1)) + CustomDuty + PALevy + CESSLevy + ExciseDuty )*  fil_tariff.iloc[0]['VAT']
  
  
    NBTax = ((cif + (cif * 0.1)) + CustomDuty + PALevy + CESSLevy + ExciseDuty )*  fil_tariff.iloc[0]['NBT']
  
  
    SCLevy = quan *  fil_tariff.iloc[0]['SCL']
  
    Tax = CustomDuty + Surcharge + PALevy + CESSLevy + ExciseDuty + VATax + NBTax + SCLevy

    t_c = (Tax/ cif)* 100

    # list = (CustomDuty, Surcharge, PALevy, CESSLevy, ExciseDuty, VATax, NBTax, SCLevy,  Tax, T_C)

    # print(list)


   # print(tabulate([['Year', year], ['HS CODE', HSCode], ['cif value', CIF], ['Quantity', quan], ['Custom Duty', CustomDuty], ['Surcharge Tax', Surcharge],['PAL', PALevy], ['CESS Levy', CESSLevy],['Excise Duty', ExciseDuty], ['VAT', VATax], ['NBT', NBTax],['SCL', SCLevy], ['Total Tax ', Tax],['Total Tax as a % of CIF', T_C]], headers=['DESCRIPTION', 'VALUE'], tablefmt='orgtbl'))
    
   
    
    put_table([['Year', 'HS CODE', 'CIF value', 'Quantity',  'Custom Duty',  'Surcharge Tax', 'PAL', 'CESS Levy', 'Excise Duty',  'VAT',  'NBT', 'SCL',  'Total Tax ', 'Total Tax as a % of CIF'],
                [ year, HSCode, cif,  quan,  CustomDuty,  Surcharge, PALevy,  CESSLevy, ExciseDuty,  VATax,  NBTax, SCLevy,  Tax, t_c],]
            )

    # break
3
if __name__ == '__main__':
    pywebio.start_server(tariff)