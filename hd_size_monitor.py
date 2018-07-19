#!/usr/bin/env python
#-*- encoding:UTF-8 -*-

"""
App para verificar Espaço em disco e enviar email 
informando o percentual de uso, para evitar crash do servidor.
"""
import os, socket
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from sendemail import enviaEmail  #modulo personalizado com funcao para enviar o email

#Diretório alvo
dir = '/'

# Verifica o percentual em disco disponivel  
strg = "%"
def verifEspaco(dir):
	disk = os.statvfs(dir)
	totalBytes = float(disk.f_bsize * disk.f_blocks)
	totalGB = totalBytes/1024/1024/1024 
	totalUso = float(disk.f_bsize*(disk.f_blocks-disk.f_bfree))
	usoGB = totalUso/1024/1024/1024
	percreal = (usoGB/totalGB)*100
	hd_uso = percreal + 4 # +4% de espaco reservado do sistema em media
	return hd_uso

perc = verifEspaco(dir)

#Verificando IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))
ip = s.getsockname()[0]
s.close()

#Hostname da maquina
servidor = socket.gethostname()

#dados de envio de email
subject = "*** Espaco em disco insuficiente ***"
fromwho = 'exemplo@servidorde_email.com.br'
tosend = 'user@servidor_de_email.com.br'
#tosend = 'hinfo@gmx.com' #ambiente de teste

# Parametros para verificar se deve enviar email
if int(perc) >= 90:
	mensagem = """
Atenção!
Servidor %s, %s
Está com %.f%s do disco em uso.
Espaço insuficiente em disco!!!
Delete alguns arquivos desnecessários!
"""% (servidor, ip, perc,strg)
	status = "vermelho"

elif int(perc) > 80:
	mensagem = """
Atenção!
Servidor %s, %s
Está com %.f%s do disco em uso.
Espaço em disco está ficando pequeno. 
Delete alguns arquivos desnecessários!
"""	% (servidor, ip, perc,strg)
	status = "amarelo"
else:
	mensagem = """
Servidor: %s %s
Está com %.f%s do disco em uso.
Espaço em disco está OK!
""" % (servidor, ip, perc,strg)
	status = "verde"

#Se o Espaço estiver reduzido envia o email
if status == "vermelho": 
	msg = MIMEText(mensagem,"plain", "utf-8")
	msg["Subject"] = subject
	msg['From'] = fromwho
	msg['To'] = tosend
	enviaEmail(msg,fromwho,tosend)


#.:.
	
