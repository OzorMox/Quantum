import core.server
s = core.server.UMMOServer()
ip,port = open("servers.txt").read().split("\n")[0].split(":")
port = int(port)
s.host(ip,port,"enet_adapter")
while s.running:
    s.update()
