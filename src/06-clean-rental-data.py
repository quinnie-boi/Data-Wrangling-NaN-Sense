


def clean_rental()
    """ """


    # Remove the 803 weird and unusable rows containg 4-5 NA Values
    df.dropna(
        subset=["Median Rent"],
        inplace=True
    )

    # Remove rows where Location Id == -99
    df = df[df["Location Id"] != -99]

    # standardise Number Of Beds column <- do not need this if ALL & ALL is the aggrogate data
    # df['Number Of Beds'] = df['Number Of Beds'].replace(to_replace=['5', '6', '7', '8', '9', '15'], value="5+")

    df['Number Of Beds'] = df['Number Of Beds'].astype('category')
    df['Dwelling Type'] = df['Dwelling Type'].astype('category')
    df.rename(columns={'Location Id': 'sa2_code'}, inplace=True)

    df = df[
        (df["Dwelling Type"] == "ALL") &
        (df["Number Of Beds"] == "ALL")
        ].copy()

    return df