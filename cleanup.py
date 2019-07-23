#listing  files  in Python
import os,time,sys
date=time.strftime("%m%d%Y")
logfile="logfile_"+date+".txt"
sys.stdout=open(logfile,"w")
sys.stderr=open(logfile,"w")

def cleanup():
    path=[]
    days=0
    count_file=0
    count_folders=0
    details_list=[]
    fo=open("details.txt","r")
    lines=fo.readlines()
    for line in lines:
        details_list.append(line.strip('\r\n'))

    path=details_list.pop(0)
    days=details_list.pop(0)

    time_in_secs=time.time()-(int(days)*3600)
    for root,dirs,files in os.walk(path,topdown=False):
        for file in files:
            full_path=os.path.join(root,file)
            stat=os.stat(full_path)
            if stat.st_mtime<=time_in_secs:
                try:
                    os.remove(full_path)
                    print("Removed file:",full_path)
                    count_file+=1
                except OSError as e:
                    print("Error Message:",e)

        for folder in dirs:
            full_path_d=os.path.join(root,folder)
            try:
                #print("Removed folder:",folder)
                os.rmdir(full_path_d)
                print("Removed Folder:",full_path_d)
                count_folders+=1
            except OSError as e:
                print("Error Message:",e)

    print("Files removed from path",path,":",count_file)
    print("Folders removed from path",path,":",count_folders)


def Email_Notification():
    import email, smtplib, ssl, sys

    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    COMMASPACE = ', '

    subject = "Cleanup Activity - Automation"
    body = """Hi Team,

    Please find attached cleanup logs.

    Regards,
    Arun"""
    sender_email = "arunnakade@gmail.com"
    receiver_email = ['arunnakade@gmail.com']
    password = "Arun@1992"

    for To in receiver_email:
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = COMMASPACE.join(receiver_email)
        message["Subject"] = subject
        # message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = logfile  # In same directory as script

        # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
            print("Congo!!!Email sent")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


if __name__=="__main__":
   cleanup()
   Email_Notification()