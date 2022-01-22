import numpy as np
import xlsxwriter as xls
import pandas as pd

M = np.array([[7.6, 6, 6, 3299], # Punkty w A0
                  [8.1, 6, 4, 4399], # Punkty w A0
                  [6.2, 8, 4, 2700], # Punkty w A0
                  [27, 8, 4, 4549], # Punkty w A1 - nieosiągalne
                  [14.4, 16, 17, 4049], # Punkty w A2 - QWO, # Punkty w A1 - nieosiągalne
                  [14.8, 8, 12, 8199], # Punkty w A1 - nieosiągalne
                  [14.8, 8, 9.5, 9699],# Punkty w A1 - nieosiągalne
                  [14, 8, 11, 5399], # Punkty w A1 - nieosiągalne
                  [27, 16, 6, 7299], # Punkty w A1 - nieosiągalne
                  [18.4, 8, 14, 5099,], # Punkty w A1 - nieosiągalne
                  [18.4, 32, 10, 7699], # Punkty w A2 - QWO
                  [28.2, 16, 10, 5099], # Punkty w A1 - nieosiągalne
                  [16.8, 16, 14, 5099], # Punkty w A1 - nieosiągalne
                  [14.8, 8, 15, 5699], # Punkty w A1 - nieosiągalne
                  [30.6, 16, 20, 10499], # Punkty w A3
                  [14.4, 16, 4, 4399], # Punkty w A1 - nieosiągalne
                  [15.6, 16, 13, 8299],
                  [14.4, 8, 15, 7099], # Punkty w A1 - nieosiągalne
                  [15.6, 16, 12, 8099], 
                  [18.4, 8, 11, 5699], # Punkty w A1 - nieosiągalne
                  [16.8, 8, 12, 3999], # Punkty w A1 - nieosiągalne
                  [15.6, 8, 10, 3599], # Punkty w A1 - nieosiągalne
                  [16.8, 16, 8, 5599],
                  [15.6, 16, 10, 5999],
                  [18.8, 32, 14, 8999]]) # Punkty w A3

# workbook = xls.Workbook('Decyzje.xlsx')
# worksheet = workbook.add_worksheet()
# row=0
# col=0

# for kryt1, kryt2, kryt3, kryt4 in (M):
#     worksheet.write(row, col, kryt1)
#     worksheet.write(row, col+1, kryt2)
#     worksheet.write(row, col+2, kryt3)
#     worksheet.write(row, col+3, kryt4)
#     row += 1
# workbook.close()
pd.DataFrame(M).to_csv("Decyzje.csv", index=None)


