import os, tarfile, subprocess, time

print(''' 
--------------------------------------------------------
WRF model use many supporting libraries, such as jasper, 
libpng, zlib, hdf5, pnetcdf, and netcdf. These libraries  
are HIGHLY RECOMMENDED installed them in your machine.
--------------------------------------------------------
''')
str(input("Do you want continue?"))


#Start time
strt = time.localtime(); strt = time.strftime("%Y-%m-%d %H:%M %z", strt)

# Make folder installation
cur_dir     = os.getcwd()
out_install = cur_dir + "/out"
os.makedirs(out_install) 

# Extract each Libraries file
lib_dir = cur_dir + "/libraries"
os.chdir(lib_dir) #Open directory
with open("requirements.txt","r") as tar_files:
    library_files = [line.rstrip() for line in tar_files]

for lib_files in library_files:
    tar = tarfile.open(lib_files, "r:gz")
    tar.extractall()
    tar.close()

# Assign Environment Variable
CPPFLAGS = f"CPPFLAGS=-I/{out_install}/include"
LDFLAGS  = f"LDFLAGS=-L/{out_install}/lib"
LD_LIBRARY_PATH = f"LD_LIBRARY_PATH={out_install}/lib:$LD_LIBRARY_PATH"
CC = f"CC={out_install}/bin/mpicc"
PATH = f"PATH={out_install}/bin:$PATH"

# LIBRARIES INSTALLATION
# 1. ZLIB
subprocess.run(f"./configure --prefix={out_install}; make check install", cwd=library_files[0][:-7] + "/", shell=True)

# 2. PNG
subprocess.run(f"{LDFLAGS} {CPPFLAGS} ./configure --prefix={out_install} --with-zlib-prefix={out_install}; make check install", cwd=library_files[1][:-7] + "/", shell=True)

# 3. Jasper
subprocess.run(f"{LDFLAGS} {CPPFLAGS} ./configure --prefix={out_install}; make check install", cwd=library_files[2][:-7] + "/", shell=True)

use_hdf5 = "Yes"

if use_hdf5 == "No" or use_hdf5 == "no" or use_hdf5 == "n":
    netcdf_option = "--disable-netcdf-4"
    # Netcdf-C
    subprocess.run(f"./configure --prefix={out_install} --disable-dap {netcdf_option}; make; make install", cwd=library_files[6][:-7] + "/", shell=True)

    # # Netcdf-Fortran
    subprocess.run(f"./configure --prefix={out_install} --disable-dap; make; make install", cwd=library_files[7][:-7] + "/", shell=True)
elif use_hdf5 == "" or use_hdf5 == "Yes" or use_hdf5 == "Y" or use_hdf5 == "yes":
    #MPICH
    subprocess.run(f"./configure --prefix={out_install} --with-device=ch3; make; make install", cwd=library_files[3][:-7] + "/", shell=True)
    subprocess.run(f"export {PATH}", shell=True)
    
    # HDF5
    subprocess.run(f"{CC} {CPPFLAGS} {LDFLAGS} ./configure --prefix={out_install} --with-zlib={out_install} --enable-hl --enable-fortran --enable-parallel; make; make install", cwd=library_files[4][:-7] + "/", shell=True)
    
    # Checking HDF5 libraries
    hdf5_files = f"{out_install}/bin/h5dump"
    if not(os.path.exists(hdf5_files)):
        print(f"Please check HDF5 installation in {out_install}/bin")

    else:
        # Netcdf-C
        subprocess.run(f"{CC} {CPPFLAGS} {LDFLAGS} ./configure --prefix={out_install} --disable-dap --enable-shared --enable-parallel-tests --enable-pnetcdf --enable-hdf5; make check install", cwd=library_files[6][:-7] + "/", shell=True)

        # Netcdf-Fortran
        subprocess.run(f"{CC} {CPPFLAGS} {LDFLAGS} ./configure --prefix={out_install} --enable-parallel-tests; make; make install", cwd=library_files[7][:-7] + "/", shell=True)

        #Pnetcdf
        subprocess.run(f"{CPPFLAGS} {LDFLAGS} ./configure --prefix={out_install} --with-mpi={out_install} --enable-fortran --enable-shared; make; make install", cwd=library_files[5][:-7] + "/", shell=True) 

# Checking libraries
subprocess.run(f"{PATH}", shell=True)

check_files = [f"{out_install}/bin/nc-config", f"{out_install}/bin/nf-config", f"{out_install}/bin/pnetcdf-config", f"{out_install}/bin/h5dump"] 

#Stop time
stp = time.localtime(); stp = time.strftime("%Y-%m-%d %H:%M %z", stp)

if os.path.exists(check_files[0]) and os.path.exists(check_files[1]) and os.path.exists(check_files[2]) and os.path.exists(check_files[3]):

    print(f'''
    ------------------------------------------------

    !!!!  Libraries were installed successfully  !!!

    ------------------------------------------------

    These library were installed in {out_install} directory

    These libraries were started installed in {strt}
    and ended in {stp}

    You can continue to install WRF and WPS by typing 
    on bash terminal:

    (WRF) 
    python script/install_WRF.py

    (WPS)
    python script/install_WPS.py 
    ''')

else:
    print(f''' 
    Please check the installation LIBRARIES:
    ''')

#Back to current directory
os.chdir(cur_dir)