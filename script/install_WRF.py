import os, subprocess, tarfile, time, glob

#Current directory
cur_dir     = os.getcwd()

#Open directory
wrf_wps_dir = cur_dir + "/wrf"
os.chdir(wrf_wps_dir)

#Print instruction
print('''
After you press enter button, you asked to choose one
of compilers to compile WRF and nesting method.

                      Hint: You can type "34" and "1" 
''')

print(str(input("Do you want continue to install WRF? [press enter]")))

#WRF path
wrf_path = wrf_wps_dir + "/WRF"
old_path = wrf_wps_dir + "/WRF-4.2.2"
out_install = cur_dir + "/out"

#Start time
strt = time.localtime(); strt = time.strftime("%Y-%m-%d %H:%M %z", strt)

#Extract WRF files
wrf = tarfile.open(old_path + ".tar.gz","r:gz")
wrf.extractall()
wrf.close()

#Rename WRF files
subprocess.run(f"mv {old_path} {wrf_path}", shell=True)

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

# Installing WRF
os.chdir(wrf_path)
subprocess.run(f"export {JASPERINC} {JASPERLIB} {NETCDF} {PNETCDF} {HDF5} {PHDF5} {PATH} {LD_LIBRARY_PATH} {LDFLAGS}; ./configure; ./compile em_real -j 4", shell=True, cwd=wrf_path)

# Finish
#Stop time
stp = time.localtime(); stp = time.strftime("%Y-%m-%d %H:%M %z", stp)

#Check programs
os.chdir(wrf_path + "/main")
check_files = glob.glob("*.exe")

if os.path.exists(check_files[0]) and os.path.exists(check_files[1]) and os.path.exists(check_files[2]) and os.path.exists(check_files[3]):
    print(f'''
    ------------------------------------------------

    !!!!     WRF was installed successfully     !!!!

    ------------------------------------------------

    WRF was started installed in {strt}
    and ended in {stp}
    ''')
else:
    print(f''' 
    Please check the environment/variable of LIBRARIES:
    {NETCDF} 
    {PNETCDF} 
    {HDF5} 
    {PHDF5} 
    ''')