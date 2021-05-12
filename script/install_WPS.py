import os, subprocess, tarfile, glob

#Current directory
cur_dir     = os.getcwd()

#Open directory
wrf_wps_dir = cur_dir + "/wrf"
os.chdir(wrf_wps_dir)

#Print instruction
print('''
After you press enter button, you asked to choose one
of compilers to compile WPS.

                                Hint: You can type "3" 
''')

print(str(input("Do you want continue to install WPS? [press enter]")))

#WRF path
wps_path = wrf_wps_dir + "/WPS"
old_path = wrf_wps_dir + "/WPS-4.2"
out_install = cur_dir + "/out"

#Extract WPS files
wps = tarfile.open(old_path + ".tar.gz","r:gz")
wps.extractall()
wps.close()

#Rename WPS files
subprocess.run(f"mv {old_path} {wps_path}", shell=True)

# Assign Environment Variable
LDFLAGS  = f"LDFLAGS=-L/{out_install}/lib"
CPPFLAGS = f"CPPFLAGS=-I/{out_install}/include"
LD_LIBRARY_PATH = f"LD_LIBRARY_PATH={out_install}/lib:$LD_LIBRARY_PATH"
CC        = f"CC={out_install}/bin/mpicc"
PATH      = f"PATH={out_install}/bin:$PATH"
JASPERLIB = f"JASPERLIB={out_install}/lib"
JASPERINC = f"JASPERINC={out_install}/include"
NETCDF    = f"NETCDF={out_install}"
PNETCDF   = f"PNETCDF={out_install}"
HDF5      = f"HDF5={out_install}"
PHDF5     = f"PHDF5={out_install}"

#Installing WPS
os.chdir(wps_path)
subprocess.run(f"export {JASPERINC} {JASPERLIB} {NETCDF} {PNETCDF} {HDF5} {PHDF5} {PATH} {LD_LIBRARY_PATH} {LDFLAGS} {CPPFLAGS}; ./configure; ./compile", shell=True, cwd=wps_path)

#Check programs
os.chdir(wps_path)
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
    {HDF5} 
    {PHDF5} 
    ''')