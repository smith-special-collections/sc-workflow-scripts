from asnake.aspace import ASpace
import argparse
import logging
import csv
import pprint


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("CSVFILE", default="DEFAULT", help="Path to CSV file for parsing.")
    cliArguments = argparser.parse_args()

    aspace = ASpace()


    with open(cliArguments.CSVFILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['resource_uri'])
            record = aspace.client.get(row['resource_uri']).json()
            #print(record)
            agent = row['agent_uri']
            role = row['role']
            new_agent = {'is_primary': False, 'role': role, 'terms': [], 'ref': agent}
            print(new_agent)
            record['linked_agents'].append(new_agent)
            print("This is the new record: ")
            print(record)

            try:
                post = aspace.client.post(row['resource_uri'],json=record).json()
                print('Successful update for {}'.format(post['uri']))
            except:
                print('Failed update for {}'.format(row['resource_uri']))
