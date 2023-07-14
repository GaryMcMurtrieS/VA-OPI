"""Script that pulls historic data to display on screen"""

# import pandas as pd
# from archappl.client import ArchiverDataClient
from org.csstudio.opibuilder.scriptUtil import PVUtil

# client = ArchiverDataClient()
# client.url = 'http://127.0.0.1:17665'

# pvs_x = ['VA:LS1_CB01:BPM_D1251:X_RD', 'VA:LS1_CB01:BPM_D1271:X_RD']
# pvs_y = ['VA:LS1_CB01:BPM_D1251:Y_RD', 'VA:LS1_CB01:BPM_D1271:Y_RD']

# TIMESTAMP = '2023-06-05T13:04:08.000000-04:00'

# data_x = client.get_data_at_time(pvs_x, TIMESTAMP)
# data_y = client.get_data_at_time(pvs_y, TIMESTAMP)

# data_x.update(data_y)
# # dataframe = pd.DataFrame.from_dict(data_x).T
# # dataframe.to_csv('data_from_archiver.csv')

pvs[1].setValue(PVUtil.getDouble(pvs[1]) + 1)