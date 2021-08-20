""" Script para variar os octetos de um endereço IP """
"""     import subprocess
    subprocess.Popen("ssh {user}@{host} {cmd}".format(user=user, host=host, cmd='ls -l'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
"""

try:
    from os import sep
    from os import getenv
    from dotenv import load_dotenv, find_dotenv
    from datetime import datetime, time
    import connect_ssh
    import sys
    import csv
    import subprocess
    subprocess.call("pip install -r requirements.txt")
except:
    subprocess.call(["pip install paramiko==2.7.2",
                    "pip install virtualenv==20.6.0"])


load_dotenv(find_dotenv())
host = getenv('HOST')
usr = getenv('USER')
password = getenv('PASSWORD')
port = getenv('PORT')


RESET_OCTET = 0
THIRD_OCTET_RANGE = 2
SECOND_OCTET_RANGE = 18
ip_address = [172, 17, 0, 1]


change_first_octet_address, change_second_octet_address = False, True
AUX_SECOND_OCTET_ADDRESS = ip_address[1]
AUX_THIRD_OCTET_ADDRESS = ip_address[2]


def escrevecsv(list_of_ip: str, path: str, header: str):
    with open(path, 'w', encoding='utf-8', newline='') as file:
        csv_file = csv.writer(file, quoting=csv.QUOTE_ALL, )
        file.write(header+'\n')
        csv_file.writerows(list_of_ip)
        ''' flag = file.write(''.join(lista))
        if flag == 0:
            return 'arquivo {} gravado com sucesso'.format(path)
        else:
            return 'erro na gravvação' '''


if len(sys.argv) > 1:
    ip_range_arg = sys.argv[1].strip()
    print("Argumentos passados: ", str(sys.argv[1:]))
    ip_address = [int(x) for x in (ip_range_arg.split('.'))]


def change_octet_address(ip_address_, index, range_octect):
    ips_changed = []
    ips_changed.append('.'.join(map(str, ip_address_)))

    #print(f'IP: {ip_address}')
    if(ip_address_[index] < range_octect):
        for x in range(ip_address_[index], range_octect):
            ip_address_[index] = ip_address_[index] + 1
            string_ip = '.'.join(map(str, ip_address_))
            ips_changed.append(string_ip)

        ''' If para caso quiser intercalar  alteração dos octetos '''
        if index == 1:
            #change_second_octet_address = True
            change_first_octet_address = False

        if index == 2:
            #change_first_octet_address = True
            change_second_octet_address = False
            ip_address_[index-1] = ip_address_[index-1] + 1
            if(ip_address_[index-1] <= SECOND_OCTET_RANGE):
                ip_address_[index] = RESET_OCTET
    return ips_changed


''' Instanciar a conexão ssh '''
ssh = connect_ssh.SSH(host, usr, password, port)


def exec_command(ssh_client: ssh, command: str):
    result = ssh_client.exec_cmd(command)
    if result:
        return result
    else:
        return "executado com sucesso"


all_ips_address_generated = []
#all_ips_address_generated.append('.'.join(map(str, ip_address)))

''' Etapa de geração de IP's '''
while(ip_address[1] <= SECOND_OCTET_RANGE):
    # if ip_address[1] == 16:
    # break
    if AUX_SECOND_OCTET_ADDRESS == SECOND_OCTET_RANGE and AUX_THIRD_OCTET_ADDRESS == THIRD_OCTET_RANGE:
        break
    if ip_address[2] < THIRD_OCTET_RANGE and change_second_octet_address:
        all_ips_address_generated = all_ips_address_generated + \
            change_octet_address(ip_address, 2, THIRD_OCTET_RANGE)

print(*all_ips_address_generated, sep="\n")

''' Colocar o retorno de cada execução na lista '''
list_with_return_command = [exec_command(ssh,
                                         f'config user ldap; edit Pictor; set source-{x}; next; end')
                            for x in all_ips_address_generated]

print(*list_with_return_command)

'''
with open('file.txt', 'a+', encoding='utf-8') as file:
    current_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    file.write('ip;data;execução '+'\n')
    [file.writelines(str(ip+';'+res + '\n'))
     for ip, res in zip(all_ips_address_generated, list_with_return_command)]
 '''
