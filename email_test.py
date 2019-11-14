from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase

import smtplib
import os 

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

if __name__=="__main__":        
    from_addr = ''
    password = ''
    to_addr = ','.join(['','xxx@bupt.edu.cn'])
    smtp_server = 'smtp.163.com'
    # 邮件对象:
    msg = MIMEMultipart()
    host_name = os.popen("hostname").read().strip('\n')
    msg['From'] = _format_addr(host_name + ' <%s>' % from_addr)
    msg['To'] = to_addr
    msg['Subject'] = Header('服务器显卡使用情况', 'utf-8').encode()

    # 邮件正文是MIMEText:
    msg.attach(MIMEText('Have a nice day', 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取文件:
with open('./gpu_usage.txt', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('text', 'plain', filename='gpu_usage.txt')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='gpu_usage.txt')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
    
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, msg['to'].split(','), msg.as_string())
    server.quit()
    
    os.system("rm ./log/gpu_usage.txt")