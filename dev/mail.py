import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmail (receiver_address, mail_content_password, mail_content_choose='mail_content_base', sender_address="paper.noreply@gmail.com", sender_pass="papernoreplypassword") :
    """
   -RecieverAdress
   -MailContent(UserPassword)
    """
    
    mail_content ="Bonjour \nVotre uuid temporaire est : " + mail_content_password + "\nCette clée est à utiliser au même titre que votre mot de passe."
    
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address

    if mail_content_choose == 'mail_content_base' :
        message['Subject'] = "Forgot-Password-PaperLand"
        message.attach(MIMEText(mail_content, 'plain'))

    elif mail_content_choose == 'notify_update_password' :
        message['Subject'] = "Update-Password-PaperLand"
        mail_content_update = "Bonjour \nNous vous informons que votre mot de passe à bien été modifié !\nA bientôt !"
        message.attach(MIMEText(mail_content_update, 'plain'))
    
    elif mail_content_choose == 'notify_account_created' :
        message['Subject'] = "Account-Created-On-Paperland"
        mail_content_update = "Bonjour \nNous vous informons que votre compte a bien été enregistré !!!\nA bientôt !"
        message.attach(MIMEText(mail_content_update, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls()

    session.login(sender_address, sender_pass)
    text = message.as_string()

    session.sendmail(sender_address, receiver_address, text)
    session.quit()

if __name__ == "__main__":
    sendmail("maximilien.poncet19@gmail.com", "Miroredge21345678" )