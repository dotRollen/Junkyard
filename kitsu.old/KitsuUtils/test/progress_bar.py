import sys


def progress(count, total, prefix='', suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('%s: [%s] %s%s ... %s\r' % (prefix, bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben

# 
# Sample Usage
# 

from time import sleep

# A List of Items
items = list(range(0, 57))
l = len(items)

# Initial call to print 0% progress
progress(1, l, 'Hi Ed')
for i, item in enumerate(items):
    # Do stuff...
    sleep(0.1)
    # Update Progress Bar
    progress(count=i+1, total=l, prefix='Sending Bios', suffix='[{}/{}]'.format(i+1, l))
print ''