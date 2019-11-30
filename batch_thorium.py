from core import *
import glob

os.mkdir(sys.argv[2])

gl = os.path.join(os.getcwd(), sys.argv[1], '*.exp')
print gl
in_fnames = glob.glob(gl)
for in_fname in in_fnames:
    out_fname = os.path.join(os.getcwd(), sys.argv[2], os.path.basename(in_fname)[:-3] + 'csv')
    print out_fname
    processOne(in_fname, out_fname)

