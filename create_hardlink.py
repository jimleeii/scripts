import os

# Open a file
path = "/var/www/html/foo.txt"
fd = os.open( path, os.O_RDWR|os.O_CREAT )

# Close opened file
os.close( fd )

# Now create another copy of the above file.
dst = "/tmp/foo.txt"
os.link( path, dst)

print("Created hard link successfully!!")