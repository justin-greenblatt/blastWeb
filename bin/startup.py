from subprocess import Popen, PIPE
import os
from settings import dConfig as homelessConfig

#configure home Directorie
homelessConfig["common"]["HOME_DIR"] = os.environ.get("HOME")
dConfigOut = open(os.path.join(configsPath, "directories.ini"), 'w')
homelessConfig.write(dConfigOut)
dConfigOut.close()

from settings import sConfig, dConfig, pConfig

def runCommand(command):
    p = Popen(command, stdout = PIPE, stdin = PIPE)
    print(" ".join(command))
    p.wait()
    print("finished")
    return p.communicate()

for p in sConfig["apt"].values():
    runCommand(["sudo", "apt", "install", p, "-y"])
for q in sConfig["pip"].values():
    runCommand(["sudo", "pip3", "install", q, "--no-input"])

#formatDisk
formatDiskCommand = ["sudo", "mkfs.ext4", "-m", "0", "-E", "lazy_itable_init=0,lazy_journal_init=0,discard", "/dev/sdb"]
runCommand(formatDiskCommand)

print("-----formatedDisk-----")

def createDir(dirName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)

createDir(dConfig["common"]["data_path"])
mountDiskCommand = ["sudo", "mount", "-o", "discard,defaults", "/dev/sdb", dConfig["common"]["data_path"]]
runCommand(mountDiskCommand)

print("-----mounted disk-----")

for d in dConfig["resources"].values():
    createDir(d)
    print("---created directorie : "+d)
