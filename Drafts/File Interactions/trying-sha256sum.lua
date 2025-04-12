name = io.read()
a,b,c = os.execute("echo " .. name .. " | sha256sum -")
print("a=", a,"b=", b, "c=", c)
