# AutoLinux

The purpose of these classes are to help people with limited knowledge of linux.

With the help of these classes, we can create a list of actions for specific purposes.

    from linux import User, Server

    u = User(username="ilker", keyfile="/home/ilker/.ssh/id_rsa")
    s = Server("blog.manap.se",u)
    out = s.user.run_command("df -h")
    print(out["stdout"])



