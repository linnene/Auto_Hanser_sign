import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendMail(mail_content,recv_address):
    sender_address = 'teadarkline@gmail.com'
    sender_pass = 'fhbj stjc jnas ztna'

    message = MIMEMultipart()  
    message['From'] = sender_address  
    message['To'] = recv_address  
    message['Subject'] = '发送主题,自己自定义'
    message.attach(MIMEText(mail_content,'plain'))
    session = smtplib.SMTP('smtp.gmail.com',)
    session.starttls()
    session.login(sender_address,sender_pass)
    text = message.as_string()
    session.sendmail(sender_address,recv_address,text)
    print("send {} successfully".format(recv_address))
    session.quit()

main_content = '''代码就是这么多
是不是很简单。
ok了家人们,记得点一个赞。
'''
sendMail(main_content,"2691234891@qq.com")
