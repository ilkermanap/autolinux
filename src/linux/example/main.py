from linux import User, Server

u = User(username="ilker", keyfile="/home/ilker/.ssh/id_rsa")
s = Server("blog.manap.se",u)
out = s.user.run_command("df -h")
print(out["stdout"])

