""" File that converts PV list to more functional CSV file """

import pandas as pd


def convert_to_csv(txt_file, csv_file):
    """Converts raw txt file containing PVs to a CSV file """
    pvs = pd.read_csv(txt_file, header=None)

    pvs = pvs[0].str.split(':', expand=True)

    # Splitting only columns 2 and 3 on underscores, as the final column with variable identifiers
    # contains underscores but should not be split
    df1 = pvs[1].str.split('_', expand=True)
    df2 = pvs[2].str.split('_', expand=True)
    pvs = pd.concat([pvs[0], df1, df2, pvs.loc[:, 3:]], axis=1)

    pvs.dropna()

    pvs.columns = [
        "System Identifier", "Location", "Managing Device", "Device Type", "Position",
        "Variable Identifier"
    ]

    pvs.to_csv(csv_file, index=False)


if __name__ == "__main__":
    convert_to_csv("VA_pvlist.txt", "va_pvs.csv")
