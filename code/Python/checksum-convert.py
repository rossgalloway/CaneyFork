import csv
from web3 import Web3

print('opening file to convert addresses...')

# Open the CSV file using a context manager
with open('input/230313-DXD-addresses.csv') as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader(csv_file)
    # Skip the header row (if there is one)
    next(csv_reader)
    # Initialize an empty list to hold the data
    data = []
    print('converting addresses...')
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # convert each address (first element in each row item) to a checksum address and replace existing address
        row[0] = Web3.toChecksumAddress(row[0])
        # Add the row to the data list
        data.append(row)
    print('addresses converted!')

# Save to new csv file. input file path here
with open('output/230313_DXD_holders_formatted.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # add the head labels
    writer.writerow(['HolderAddress', 'mainnet',
                    'arbitrum', 'gnosis chain', 'total'])
    # write the data
    writer.writerows(data)
    print('new CSV created')