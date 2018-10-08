import os
import sys
import radical.pilot as rp
import radical.utils as ru

if __name__ == "__main__":
    
    PILOT_CORES = 2     # the number of cores each Pilot will take
    BAG_SIZE    = 5    # the number of units
    CU_CORES    = 1     # the cores each CU will take

    report = ru.Reporter(name='radical.pilot')
    report.title('Bag of Tasks (RP version %s)' % rp.version)

    # get the resource, otherwise use localhost
    if   len(sys.argv)  > 2: report.exit('Usage:\t%s [resource]\n\n' % sys.argv[0])
    elif len(sys.argv) == 2: resource = sys.argv[1]
    else                   : resource = 'local.localhost'

    # create the session
    session = rp.Session()
    try:
        report.info('read config')
        config = ru.read_json('%s/config.json' % os.path.dirname(os.path.abspath(__file__)))
        report.ok('>>ok\n')

        report.header('submit pilots')

        # initialize the pilot description
        pmgr = rp.PilotManager(session=session)
        pd_init = {'resource'      : resource,
                   'runtime'       : 15,  # pilot runtime (min)
                   'exit_on_error' : True,
                   'project'       : config[resource]['project'],
                   'queue'         : config[resource]['queue'],
                   'access_schema' : config[resource]['schema'],
                   'cores'         : PILOT_CORES
                  }
        pdesc = rp.ComputePilotDescription(pd_init)

        pilot = pmgr.submit_pilots(pdesc)
        report.header('submit units')

        umgr = rp.UnitManager(session=session)
        umgr.add_pilots(pilot)

        report.info('create %d unit description(s)\n\t' % BAG_SIZE)

        # initialize the compute unit descriptions
        size = 1
        cuds = list()
        for i in range(0, BAG_SIZE):
            cud = rp.ComputeUnitDescription()
	    cud.executable = 'python'
	    cud.arguments = ['bubble_sort_rp.py','Input%s.txt' % (i+1),'Output%s.txt' % (i+1)]
	    cud.input_staging = ['Input/Input%s.txt' % (i+1),'bubble_sort_rp.py']
	    cud.output_staging = ['Output%s.txt' % (i+1)]
            #cud.executable 		= ['/bin/bash'] # Assign executable to the task
            #cud.arguments 		= ['-l', '-c', 'base64 /dev/urandom | head -c %s > output.txt' % size] # Assign arguments
            cud.environment     = {'CU_NO': i}
            cud.cpu_processes   = 1
            cuds.append(cud)
            report.progress()
        report.ok('>>>ok\n')

        units = umgr.submit_units(cuds)

        report.header("gather results")
        umgr.wait_units()

        # print the 
        for unit in units:
            print "* CU %s, state %s, exit code: %s, stdout: %s" \
                % (unit.uid, unit.state, unit.exit_code, unit.stdout.strip())

    # catch exceptions
    except Exception as e:
        report.error('caught Exception: %s\n' % e)
        ru.print_exception_trace()
        raise

    # catch keyboard interrupt
    except (KeyboardInterrupt, SystemExit) as e:
        ru.print_exception_trace()
        report.warn('exit requested\n')

    # close the session
    finally:
        report.header("closing session")
        session.close ()
    report.header()
