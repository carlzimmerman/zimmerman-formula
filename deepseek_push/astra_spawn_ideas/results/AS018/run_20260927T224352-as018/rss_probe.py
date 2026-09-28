import resource
b0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
x = bytearray(80*1024*1024)
b1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
del x
print("ru_maxrss after 80 MB alloc:", b1)
print("delta:", b1 - b0)