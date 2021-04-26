import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

<<<<<<< HEAD
def sendmail (receiver_address, mail_content_password, sender_address="paper.noreply@gmail.com", sender_pass="papernoreplypassword") :
=======
def sendmail (receiver_address, mail_content_password, mail_content_choose='mail_content_base', sender_address="paper.noreply@gmail.com", sender_pass="papernoreplypassword") :
>>>>>>> parent of f6efd6b (Merge pull request #7 from Baratinus/admin)
    """
   -RecieverAdress
   -MailContent(UserPassword)
    """
    
    mail_content ="Bonjour \nVotre uuid temporaire est : " + mail_content_password + "\nCette clée est à utiliser au même titre que votre mot de passe."
    
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "Forgot-Password-PaperLand" 
    message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls()

    session.login(sender_address, sender_pass)
    text = message.as_string()

    session.sendmail(sender_address, receiver_address, text)
    session.quit()

if __name__ == "__main__":
    sendmail("maximilien.poncet19@gmail.com", "Miroredge21345678" )