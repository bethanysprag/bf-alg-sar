import os
import sys
import numpy as np
import json
import bf_Sar2Shoreline
from bf.beachfront.vectorize import trace_it

try:
    import gdal
    import osr
except:
    from osgeo import gdal, osr

def main(img_path, out_path, kernelSize=10, scaleFactor=0.1, cleanup=1):
    #run bf-Sar2Shoreline --> returns binary mask
    name = bf_Sar2Shoreline.xO_names(out_path)
    binary_mask ='%s/%s_binary.tif' % (name['directory'],
                                  name['basename'])
    print binary_mask
    status = bf_Sar2Shoreline.WaterExtractionSAR(img_path,
                                                 out_path=binary_mask,
                                                 kernelSize=kernelSize,
                                                 scaleFactor=scaleFactor)
    #run vectorizing code from bf-py --> returns vector
    coastline = trace_it(binary_mask)
    if cleanup == 1:
        os.remove(binary_mask)
    # write to file
    with open(out_path, 'w') as out_path:
        json.dump(coastline, out_path)

def usage():
    print("""
          Usage:
          bf-algo-sar -i in_raster -o out_raster
          -k kernel_Size (optional, default=10)
          -s ScaleFactor (optional, default=0.1)"""
          )
    sys.exit(1)


if __name__ == '__main__':

    img_path = None
    out_path = None
    kernelSize = 10
    sf = 0.1
    cleanup = 0

    for i in range(len(sys.argv)-1):
        arg = sys.argv[i]
        if arg == '-i':
            img_path = sys.argv[i+1]
        elif arg == '-o':
            out_path = sys.argv[i+1]
        elif arg == '-k':
            kernelSize = int(sys.argv[i+1])
        elif arg == '-s':
            sf = float(sys.argv[i+1])
        elif arg == '-c':
            cleanup == int(sys.argv[i+1])

    if img_path is None:
        usage()
    if out_path is None:
        usage()

    main(img_path, out_path, kernelSize=kernelSize, scaleFactor=sf, cleanup=cleanup)
    sys.exit(0)
