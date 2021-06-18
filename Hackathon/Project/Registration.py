from tkinter import *
import boto3
import botocore
from botocore.client import Config
from tkinter import messagebox
from fpdf import FPDF
from time import sleep
from datetime import date,datetime
import os
import smtplib
import imghdr
from email.message import EmailMessage
global nc
acces_key='AKIAI43MM4QUVYVDT5WA'
access_s_key='llOZ980qQMzZnicwsInsAEhtasL1Vg1iI/OKG5BC'
label_c=0
close=0
c=0
today=date.today()
try:
    global total_c
    x=open('registration.txt','r').read().split('\n')
    print(x)
    total_c=int(x[1])
    t_date=x[0]
    print(type(t_date),type(today.day))
    if int(t_date)!=today.day:
        total_c=0
except:
    x=open('registration.txt','w').write(str(today.day)+'\n0')
    total_c=0
def destroy():
    window.destroy()
    global total_c
    print(total_c)
    x=open('registration.txt','w').write(str(today.day)+'\n{}'.format(str(total_c)))
def remove(event):
    entry.delete(0,'end')
    entry.config(fg='black')
    if type(label_c)!=type(2):
        label_c.config(text='')
def remove_1(event):
    entry_1.delete(0,'end')
    entry_1.config(fg='black')
    if type(label_c)!=type(2):
        label_c.config(text='')
def register():
    def xyz():
        global s3,bucket,label_c,close,c,total_c
        EMAIL_ADDRESS = 'harshassv.13@gmail.com'
        EMAIL_PASSWORD = 'harsha@2001'
        now = datetime.now()
        msg = EmailMessage()
        msg['Subject'] = 'Registration Bill From Apollo Hospital'
        msg['From'] = 'harshassv.13@gmail.com'
        msg['To'] = '{}'.format(entry_1.get())
        msg.set_content('Bill Of your payment')
        html='''<html>
         <head>
         <title>BILL</title>'''+'''

        <style>
        body
        {
        border:10px solid #188778;
        }
        h1
        {
        font-size:24px
        }
        img{
        vertical-align:middle;
        }
        </style>'''+'''
        </head>
        <body style="width:600;height:400">
        <form>
        <h1 style="text-align:right; font-family:Aktiv Grotesk; background-color: #FDB931;  color: #188778"> APOLLO HOSPITAL
         <img src="G:\Smart_india_hackatho\apollo.PNG" width="60" height="60" align:"top-lef"></h1>

        <label for="Firstname"><b>Date:</b></label>
        <label for="Firstname">{}</label>
        <br>
        <label for="Firstname"><b>Time:</b></label>
        <label for="Firstname">{}</label>
        <br><br><br><br><br>
        <br>
        <label for="Firstname"><b>Patient Name:</b></label>
        <label for="Firstname">{}</label>
        <br><br>
        <label for="Firstname"><b>Doctor's Name:</b></label>
        <label for="Firstname">Hema Shree Kilari</label>
        <br><br>
        <label for="Firstname"><b>Department:</b></label>
        <label for="Firstname">General Medicine</label>
        <br><br>
        <label for="Firstname"><b>Amount:</b></label>
        <label for="Firstname">1000</label>Rs
        </form>
        </body>
        </html>'''.format(str(date.today().day)+'/'+str(date.today().month)+'/'+str(date.today().year),now.strftime("%H:%M:%S"),entry.get())
        msg.add_alternative(html, subtype='html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        bucket='530045registration'
        s3=boto3.resource('s3')
        pdf=FPDF()
        pdf.add_page()
        pdf.output('{}.pdf'.format(entry.get()))
        var=open('{}.pdf'.format(entry.get()),'rb')
        s3=boto3.resource('s3',aws_access_key_id=acces_key,
                          aws_secret_access_key=access_s_key,
                          config=Config(signature_version='s3v4')
                          )
        s3.Bucket(bucket).put_object(Key='{}.pdf'.format(entry.get()),Body=var).Acl().put(ACL='public-read')
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket=entry.get(),CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
        bucket=s3.Bucket(entry.get())
        bucket.Acl().put(ACL='public-read')
        bucket='530045registration'
        s3=boto3.resource('s3')
        my_b=s3.Bucket('530045registration')
        c=0
        for obj in my_b.objects.all():
            c=c+1
        frame_c=Frame(window,bg='#ff8484')
        label_c=Label(frame_c,text='Registration Is Successfull\nThere are {} Patients before you'.format(c-1),font=('Arial',24),bg='#ff8484')
        label_c.pack()
        frame_c.pack()
        close=1
        total_c=total_c+1
    xyz()
def pc():
    bucket='530045registration'
    s3=boto3.resource('s3')
    my_b=s3.Bucket('530045registration')
    c=0
    for obj in my_b.objects.all():
        c=c+1
    bl_cd_l.config(text='    {} Patients'.format(str(total_c-c)))
def rp():
    bucket='530045registration'
    s3=boto3.resource('s3')
    my_b=s3.Bucket('530045registration')
    c=0
    for obj in my_b.objects.all():
        c=c+1
    bl_rc_l.config(text='{} Patients'.format(c))
def tpft():
     global total_c
     bl_c_l.config(text='            \t{} Patients'.format(total_c))
def clear_tp(event=0):
     bl_c_l.config(text='                           ')
def clear_rp(event=0):
     bl_rc_l.config(text='')
def clear_pc(event=0):
     bl_cd_l.config(text='')
def syncdata():
    global total_c
    s3 = boto3.client('s3')
    s3.download_file('530045admin', 'graphdata.txt', 'Total_registrations.txt')
    today = datetime.today().month
    x=open('Total_registrations.txt','r').read().split('\n')
    try:
        x[today-1]=str(int(x[today-1])+total_c)
    except:
        x.append(str(total_c))
    x='\n'.join(x)
    open('Total_registrations.txt','w').write(x)
    acces_key='AKIAI43MM4QUVYVDT5WA'
    access_s_key='llOZ980qQMzZnicwsInsAEhtasL1Vg1iI/OKG5BC'
    bucket='530045admin'
    s3 = boto3.resource('s3')
    s3.Object('530045admin', 'graphdata.txt').delete()
    var=open('Total_registrations.txt','rb')
    s3=boto3.resource('s3',aws_access_key_id=acces_key,
                      aws_secret_access_key=access_s_key,
                      config=Config(signature_version='s3v4')
                      )
    s3.Bucket(bucket).put_object(Key='graphdata.txt',Body=var).Acl().put(ACL='public-read')
window=Tk()
window.configure(bg='#ff8484')
window.geometry('700x650+200+2')
window.resizable(0,0)
window.wm_attributes('-fullscreen','true')
window.title('Registration')
f1=Frame(window)
f2=Frame(window,bg='#ff8484')
f1.configure(background='#ff8484')
sync=Button(f1,text="Sync Data",font=('Arial',14),borderwidth=4,command=syncdata)
sync.pack(side='right')
b1_c=Button(f1,text='Total Count of Patients For Today',font=('Arial',14),borderwidth=4,command=tpft)
b1_c.pack(side='left')
bl_c_l=Label(f2,text='\t          ',bg='#ff8484',font=('Arial',16))
bl_c_l.bind('<Button-1>',clear_tp)
bl_c_l.pack(side='left')
wl_4=Label(f1,text="  ",bg='#ff8484').pack(side='left')
l_w=Label(f2,text='\t\t\t          ',bg='#ff8484').pack(side='left')
b1_rc=Button(f1,text='Remaining Patients',font=('Arial',14),borderwidth=4,command=rp)
b1_rc.pack(side='left')
bl_rc_l=Label(f2,text='',bg='#ff8484',font=('Arial',16))
bl_rc_l.bind('<Button-1>',clear_rp)
bl_rc_l.pack(side='left')
wl_4=Label(f1,text="  ",bg='#ff8484').pack(side='left')
b1_cd=Button(f1,text='No.of Patients Consulted Doctor',font=('Arial',14),borderwidth=4,command=pc)
b1_cd.pack(side='left')
bl_cd_l=Label(f1,text='',bg='#ff8484',font=('Arial',16))
bl_cd_l.bind('<Button-1>',clear_pc)
bl_cd_l.pack(side='left')
f1.pack(side='top',fill='x')
f2.pack(fill='x')
frame=Frame(window,bg='#ff8484')
label=Label(frame,text='Phone Number : ',bg='#ff8484',font=("Ariel",17))
label.pack(side='left')
entry=Entry(frame,width=20,fg='#d3d3d3',font=("Ariel",16))
entry.insert(0,'Ex: 9876543214')
entry.pack(side='left')
entry.bind('<Button-1>',remove)
frame.pack()
frame1=Frame(window,bg='#ff8484')
label=Label(frame1,text='Email-id            : ',bg='#ff8484',font=("Ariel",17))
label.pack(side='left')
entry_1=Entry(frame1,width=20,fg='#d3d3d3',font=("Ariel",16))
entry_1.insert(0,'Ex: harsha@gmail.com')
entry_1.pack(side='left')
entry_1.bind('<Button-1>',remove_1)
frame1.pack()
frame_w=Frame(window,bg='#ff8484')
label_w2=Label(frame_w,text=' ',bg='#ff8484').pack()
frame_w.pack(fill='x')
frame1=Frame(window,bg='#ff8484')
button=Button(frame1,text='Register',font=("Ariel",12),command=register)
button.pack(side='left')
frame1.pack()
frame1_w=Frame(window,bg='#ff8484')
label1_w2=Label(frame1_w,text=' ',bg='#ff8484').pack()
frame1_w.pack(fill='x')
frame2=Frame(window,bg='#ff8484')
button_destroy=Button(frame2,text='close',font=("Ariel",12),command=destroy)
button_destroy.pack()
frame2.pack()
window.mainloop()
