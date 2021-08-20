from paramiko import SSHClient, AutoAddPolicy


class SSH:
    def __init__(self, hostname, username, password, port):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        print("Conectando ao servidor ssh...")
        self.ssh.connect(hostname=hostname,
                         username=username, password=password, port=port)

    def exec_cmd(self, cmd: str):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        stdin.close()

        if stderr.channel.recv_exit_status() != 0:
            return f'{stderr.read().decode("utf8")}'
        else:
            return f'{stdout.read().decode("utf8")}'
