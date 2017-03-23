import platform

system = platform.system().lower()

if system in ["linux", "linux2"]:
   print("linux")
elif system == "darwin":
   print("MAC OS X")
elif system == "win32":
   print("Windows")
else:
   print("Unknown OS")
print("VERSION %s" % (platform.release()))
