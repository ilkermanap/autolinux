import paramiko
from scp import SCPClient


class User:
    """
    Linux user class. Username is mandatory, either provide password 
    or the ssh key file. You can provide both, but key file will be 
    tried first during login.

    Attributes
    ----------
    username  : str
       User name
    password  : str
       Password, optional
    keyfile   : str
       Ssh private key file, optional
    client    : paramiko SSHClient
       Client object
    connected : boolean 
       State of the connection

    Methods
    -------
    key_based_connect(server)
       Establish connection to given server object with ssh 
       private key file. Sets client and connected attributes.
    
    sshclient(server)
       Establish connection to given server. First try the key file
       if it is given, then try the password. Sets the client and 
       connected attributes.

    copy_file(remote_file_name, local_file_name=None)
       Copy file from server. If local file name is not given, use 
       remote file name as local file name.

    run_command(cmd)
       Run the given command. Return stdout and stderr inside a dict.
       Keys are "stdout" and "stderr"        
    """
    def __init__(self, username=None, password=None, keyfile=None):
        """
        Constructor for User class.

        Attributes
        ----------
        username : str
           User name

        password : str
           Password for that user, optional.

        keyfile : str
           Path for ssh private key file, optional.
        """
        self.username = username
        self.password = password
        self.keyfile = keyfile
        self.client = None
        self.connected = False

    def key_based_connect(self, server):
        """
        Try establishing a connection using the ssh private key

        Attributes
        ----------
        server : Server
            Server object 

        Returns
        -------
        tuple
            Returns (state, message) tuple. State is either true or false
            It sets the objects client and connected attributes
        """
        if self.keyfile is not None:
            host = server.ipaddr
            pkey = paramiko.RSAKey.from_private_key_file(self.keyfile)
            self.client = paramiko.SSHClient()
            policy = paramiko.AutoAddPolicy()
            self.client.set_missing_host_key_policy(policy)
            self.client.connect(host, username=self.username, pkey=pkey)
            self.connected = True
            return (True, "connected")
        else:
            self.connected = False
            return (False, "problem with connecting with the provided key file")

    def sshclient(self, server):
        """
        Try establishing a connection to given server. 
        First try the ssh private key if it is given, otherwise use password.

        Attributes
        ----------
        server : Server
            Server object 

        Returns
        -------
        tuple
            Returns (state, message) tuple. State is either true or false
            It sets the objects client and connected attributes

        """
        state = False
        if self.keyfile is not None:
            state,  msg = self.key_based_connect(server)
        if state is False:
            if self.password is not None:
                self.client = paramiko.client.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(server.ipaddr, username=self.username, password=self.password)
                self.connected = True
                return (self.connected, "Connected")
            else:
                return (False, "No password provided")
        return (False, "Neither ssh private key nor password was given") 

    def copy_from_remote(self, remote_file_name, local_file_name=None):
        self.copy_file(remote_file_name, local_file_name=local_file_name)
    
    def copy_file(self, remote_file_name, local_file_name=None):
        """
        Copy a file from the server.

        Attributes
        ----------
        remote_file_name : str
           The file name to copy. 

        local_file_name : str
           Name of local file to create
        """
        if local_file_name is None:
            local_file_name = remote_file_name.split("/")[-1]

        if not self.connected:
            pass
        else:
            scp = SCPClient(self.client.get_transport())
            scp.get(remote_file_name, local_file_name)        
            
    def copy_to_remote(self, local_file_name, remote_file_name=None):
        """
        Copy a file to the server.

        Attributes
        ----------
        remote_file_name : str
           The file name to copy. 

        local_file_name : str
           Name of local file to copy
        """
        if local_file_name is None:
            local_file_name = remote_file_name.split("/")[-1]

        if not self.connected:
            pass
        else:
            scp = SCPClient(self.client.get_transport())
            scp.put(local_file_name, remote_file_name)        


    def run_command(self, cmd):
        """
        Run the given command at the server.

        Attributes
        ----------
        cmd : str

        Returns
        -------
        dict with keys "stdout" and "stderr". Each item will be a 
        list of strings
    
        Example
        -------
        server = Server("192.168.1.200")
        user = User(username="ilker", password="deneme")
        server.set_user(user)
        out = server.user.run_command("df -h")

        err = out["strerr"]
        txt = out["stdout"]

        """
        out = {}
        if self.connected:
            _stdin, _stdout,_stderr = self.client.exec_command(cmd)
            out["stdout"] = _stdout.read().decode() 
            out["stderr"] = _stderr.read().decode()
        return out


class Server:
    def __init__(self, ipaddr, user=None):
        self.ipaddr = ipaddr
        self.user = None
        if user is not None:
            self.user = user
            self.connect()

    def set_user(self, user):
        self.user = user

    def connect(self):
        self.user.sshclient(self)

    def test(self):
        self.connect()
        out = self.user.run_command("uname -a")
        try:
            if len(out["stdout"]) > 0:
                return True
            return False
        except:
            return False

"""
from linux import User, Server

u = User(username="ilker", keyfile="/home/ilker/.ssh/id_rsa")
s = Server("blog.manap.se",u)
out = s.user.run_command("df -h")
print(out["stdout"])

"""
