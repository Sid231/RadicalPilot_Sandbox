import sys
import pprint
import radical.utils as ru
import radical.pilot as rp
import radical.analytics as ra

if __name__ == '__main__':    # get the source folder to analyze
    if len(sys.argv) < 2:
        print "\n\tusage: %s <dir|tarball>\n" % sys.argv[0]
        sys.exit(1)    
    src = sys.argv[1]    
    if len(sys.argv) == 2: 
        stype = 'radical.pilot'
    else: 
        stype = sys.argv[2]    
    session = ra.Session(src, stype)    # print the PMGR_ACTIVE and FINAL timestamp for each pilot
    pilots = session.filter(etype='pilot', inplace=False)
    durations = pilots.duration([rp.PMGR_ACTIVE, rp.FINAL])
    pprint.pprint(durations)    sys.exit(0)
