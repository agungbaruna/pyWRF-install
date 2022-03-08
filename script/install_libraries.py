import os, tarfile, subprocess, time, sys

print(''' 
--------------------------------------------------------
WRF model use many supporting packages, such as jasper, 
libpng, hdf5, pnetcdf, and netcdf. These libraries are 
HIGHLY RECOMMENDED to install in your machine.
--------------------------------------------------------
''')
str(input("press ENTER to continue or CTRL+C to stop !"))

user_computer = os.environ["HOME"]

out_dir = str(input(f'''
The installation directory will be located at {user_computer}, named WRF-install.
Press ENTER to continue or CTRL+C to stop !
'''))

if out_dir == "": out_dir = user_computer

#Start time
strt = time.localtime(); strt = time.strftime("%Y-%m-%d %H:%M %z", strt)

# Make folder installation
cur_dir     = os.getcwd()
out_install = out_dir + "/WRF-install"

# Check folder name
if not(os.path.exists(out_install)):
    os.makedirs(out_install)
else:
    # If WRF-install dir exist, change WRF-install name 
    subprocess.run(f"mv -r {user_computer}/WRF-install {user_computer}/WRF-install-backup", shell=True) 

# Extract each Libraries file
out_lib = out_install + "/LIBRARIES"
lib_dir = cur_dir + "/libraries"

os.chdir(lib_dir) #Open library folder

with open("requirements.txt","r") as tar_files:
    library_files = [line.rstrip() for line in tar_files]

for lib_folder in library_files:
    if not(os.path.exists(lib_folder)):
        tar = tarfile.open(lib_folder + ".tar.gz", "r:gz")
        tar.extractall()
        tar.close()

# Assign Environment Variable
LD_LIBRARY_PATH = f"LD_LIBRARY_PATH={out_lib}/lib:$LD_LIBRARY_PATH"
CPPFLAGS = f"CPPFLAGS=-I/{out_lib}/include"
LDFLAGS  = f'LDFLAGS="-L/{out_lib}/lib -L/usr/lib/x86_64-linux-gnu"' 
CC       = f"CC=/usr/bin/mpicc"
PATH     = f"PATH={out_lib}/bin:$PATH"
FC       = f"FC=/usr/bin/mpif90"

# LIBRARIES INSTALLATION
# Create folder 
os.makedirs(out_lib)

# 1. PNG
subprocess.run(f"{LDFLAGS} {CPPFLAGS} {LD_LIBRARY_PATH} ./configure --prefix={out_lib}; make; make install", cwd=library_files[0] + "/", shell=True)

# 2. Jasper
subprocess.run(f"{LDFLAGS} {CPPFLAGS} {LD_LIBRARY_PATH} ./configure --prefix={out_lib}; make; make install", cwd=library_files[1] + "/", shell=True)

use_hdf5 = "Yes"

if use_hdf5 == "No" or use_hdf5 == "no" or use_hdf5 == "n":
    netcdf_option = "--disable-netcdf-4"
    # Netcdf-C
    subprocess.run(f"./configure --prefix={out_lib} --disable-dap {netcdf_option}; make; make install", cwd=library_files[4] + "/", shell=True)

    # # Netcdf-Fortran
    subprocess.run(f"./configure --prefix={out_lib}; make; make install", cwd=library_files[5] + "/", shell=True)

elif use_hdf5 == "" or use_hdf5 == "Yes" or use_hdf5 == "Y" or use_hdf5 == "yes":
    # HDF5
    subprocess.run(f"{CC} {CPPFLAGS} {LDFLAGS} ./configure --prefix={out_lib} --enable-hl --enable-fortran --enable-parallel --with-default-api-version=v18; make; make install", cwd=library_files[2] + "/", shell=True)

    # Checking HDF5 libraries
    hdf5_files = f"{out_lib}/bin/h5dump"
    if not(os.path.exists(hdf5_files)):
        print(f"Please check HDF5 installation in {out_lib}/bin")
        sys.exit()
    else:
        #Pnetcdf
        subprocess.run(f"{CPPFLAGS} {LDFLAGS} {LD_LIBRARY_PATH} ./configure --prefix={out_lib} --with-mpi=/usr/bin --enable-fortran --enable-shared; make; make install", cwd=library_files[3] + "/", shell=True)
        
        # Netcdf-C
        subprocess.run(f"{CC} {CPPFLAGS} {LDFLAGS} {LD_LIBRARY_PATH} ./configure --prefix={out_lib} --enable-dap --enable-parallel-tests --enable-pnetcdf --disable-dap; make; make install", cwd=library_files[4] + "/", shell=True)

        # Netcdf-Fortran
        subprocess.run(f"{CC} {FC} {CPPFLAGS} {LDFLAGS} {LD_LIBRARY_PATH} ./configure --prefix={out_lib}; make; make install", cwd=library_files[5] + "/", shell=True) 

# Checking libraries
check_files = [f"{out_lib}/bin/nc-config", f"{out_lib}/bin/nf-config", f"{out_lib}/bin/pnetcdf-config", f"{out_lib}/bin/h5dump"] 

#Stop time
stp = time.localtime(); stp = time.strftime("%Y-%m-%d %H:%M %z", stp)

if os.path.exists(check_files[0]) and os.path.exists(check_files[1]) and os.path.exists(check_files[2]) and os.path.exists(check_files[3]):

    print(f''' \033[32m
    ------------------------------------------------

    !!!!  Packages were installed successfully  !!!

    ------------------------------------------------

    These library were installed in {out_lib} directory

    These libraries were started installed in {strt}
    and ended in {stp}
    ''')

else:
    print(f'''  \033[31m
    Please check the installation LIBRARIES:
    ''')
    sys.exit()

#Back to current directory
os.chdir(cur_dir)