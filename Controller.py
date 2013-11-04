__author__ = 'Jacob'

#adding a comment just so it detects a change
#mark's adding a comment to test the same thing

def main():
    print 'Enter the number of the command you want to execute.'
    print '1: Turn on synchronization.'
    print '2: Turn off synchronization'
    s = raw_input('Command: ')
    if s == '1':
        sync_on()
    elif s == '2':
        sync_off()



def sync_on():
    writer = open('../a_pipe', 'w', 0)
    writer.write('t')

def sync_off():
    writer = open('../a_pipe', 'w', 0)
    writer.write('f')

main()