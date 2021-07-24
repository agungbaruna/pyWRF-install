import os, subprocess, glob

user_computer = os.environ["HOME"]

#WPS installed location
out_lib = str(input(f"Type the directory of libraries were installed [default: {user_computer}/WRF-install]: "))

if out_lib == "" : 
    out_install = user_computer + "/WRF-install"
    out_lib = user_computer + "/WRF-install/LIBRARIES"

#Open directory
wps_dir = out_install + "/WPS"

# Warning
input(f"WPS will install in {wps_dir} directory. Continue?")

# Download WPS
if not(os.path.exists(wps_dir)):
    subprocess.run("git clone https://github.com/wrf-model/WPS", shell=True)
    subprocess.run(f"mv WPS {wps_dir}", shell=True)

os.chdir(wps_dir)

#Print instruction
print('''
After you press ENTER button, you asked to choose one
of compiler.

                                Hint: You can type "3" 
''')

str(input("Do you want continue to install WPS? [press ENTER]"))

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

# Installing WPS
subprocess.run(f"export {JASPERINC}; export {JASPERLIB}; export {NETCDF}; export {PNETCDF}; export {HDF5}; export {PHDF5}; export {PATH}; export {LD_LIBRARY_PATH}; export {LDFLAGS}; export {CPPFLAGS}; ./configure; ./compile", shell=True, cwd=wps_dir)

# Check programs
check_files = glob.glob("*.exe")

if os.path.exists(check_files[0]) and os.path.exists(check_files[1]) and os.path.exists(check_files[2]):
    print(f'''
    ------------------------------------------------

    !!!!     WPS was installed successfully     !!!!

    ------------------------------------------------
    ''')
else:
    print(f''' 
    Please check the environment/variable of LIBRARIES:
    {LD_LIBRARY_PATH}
    {NETCDF} 
    {PNETCDF} 
    {JASPERLIB} 
    ''')