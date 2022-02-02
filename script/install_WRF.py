import os, subprocess, glob

user_computer = os.environ["HOME"]

#WRF installed location
out_lib = str(input(f"Type the directory of libraries were installed [default: {user_computer}/WRF-install]: "))

if out_lib == "" : 
    out_install = user_computer + "/WRF-install"
    out_lib = user_computer + "/WRF-install/LIBRARIES"

#Open directory
wrf_dir = out_install + "/WRF"

# Warning
input(f"WRF will install in {wrf_dir} directory. Continue?")

# Download WRF model
if not(os.path.exists(wrf_dir)):
    subprocess.run("git clone https://github.com/wrf-model/WRF", shell=True)
    subprocess.run(f"mv WRF {wrf_dir}", shell=True)

os.chdir(wrf_dir)

#Print instruction
print('''
After you press ENTER button, you asked to choose one
of compilers to compile WRF and nesting method.

                      Hint: You can type "34" and "1" 
''')

str(input("Do you want continue to install WRF? [press ENTER]"))

# Assign Environment Variable
LDFLAGS  = f'LDFLAGS="-L{out_lib}/lib -L/usr/lib/x86_64-linux-gnu"'
CPPFLAGS = f"CPPFLAGS=-I{out_lib}/include"
LD_LIBRARY_PATH = f"LD_LIBRARY_PATH={out_lib}/lib:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
CC        = f"CC=/usr/bin/mpicc"
FC        = f"FC=/usr/bin/mpif90"
PATH      = f"PATH={out_lib}/bin:$PATH"
JASPERLIB = f"JASPERLIB={out_lib}/lib"
JASPERINC = f"JASPERINC={out_lib}/include"
NETCDF    = f"NETCDF={out_lib}"
PNETCDF   = f"PNETCDF={out_lib}"
HDF5      = f"HDF5={out_lib}"
PHDF5     = f"PHDF5={out_lib}"

# Installing WRF
subprocess.run(f"export {JASPERINC}; export {FC}; export {JASPERLIB}; export {NETCDF}; export {PNETCDF}; export {HDF5}; export {PHDF5}; export {PATH}; export {LD_LIBRARY_PATH}; export {LDFLAGS}; ./configure; ./compile em_real -j 4", shell=True, cwd=wrf_dir)

# Finish
# Check programs
check_files = glob.glob(wrf_dir + "/main/*.exe")

if os.path.exists(check_files[0]) and os.path.exists(check_files[1]) and os.path.exists(check_files[2]) and os.path.exists(check_files[3]):
    print(f''' \033[32m
    ------------------------------------------------

    !!!!     WRF was installed successfully     !!!!

    ------------------------------------------------
    ''')
else:
    print(f'''  \033[31m
    Please check the environment/variable of LIBRARIES:
    {NETCDF},
    {PNETCDF}, 
    {HDF5}, or 
    {PHDF5} 
    ''')