import subprocess

def bash_command(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')

def bash_print(str):
    bash_command('echo "{0}"'.format(str))
