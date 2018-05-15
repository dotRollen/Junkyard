import argparse

parser = argparse.ArgumentParser(description='Automate BMC mac binding, get hardware and software inventory')
parser.add_argument('noderange', type=str, nargs='+',
                    help='groups or node range IE: node1,node2,node3 | rack1')
parser.add_argument('-g', '--getinv', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='get hardware and software inventory for Dell R630 and R730xd')
parser.add_argument('-b', '--bmcbind', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='get hardware and software inventory for Dell R630 and R730xd')

args = parser.parse_args()
print args.accumulate(args.noderange)