from tkinter import *
from tkinter import messagebox
import boto3
import os
import tkinter.font as font
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
x1=open('lab_details.txt','r').read().split()
username=x1[0]
password=x1[1]
doctor_n=''
def forgot():
    def sub_btn():
        new_pwd=password_f.get()
        new_usr=username_f.get()
        if len(new_pwd)<7 or len(new_usr)<5:
            messagebox.showerror('Error','1.Username must contain minimum 5 characters\n2.Password must contain minimum 7 characters')
            window_f.destroy()
            forgot()
        else:
            global username,password
            concat=new_usr+" "+new_pwd
            x2=open('lab_details.txt','w').write(concat)
            messagebox.showinfo('Information','Details Successfully updated')
            x2=open('lab_details.txt','r').read().split()
            username=x2[0]
            password=x2[1]
            window_f.destroy()
    window_f=Toplevel()
    window_f.configure(bg='#ff8484')
    window_f.geometry('400x350+200+2')
    window_f.resizable(0,0)
    frame1=Frame(window_f)
    username_l=Label(frame1,text='User Name : ',font=("Ariel",16),bg='#ff8484')
    username_l.pack(side='left')
    username_f=Entry(frame1,width=20,font=("Ariel",16))
    username_f.pack(side='left')
    frame1.pack()
    waste1=Frame(window_f,bg='#ff8484')
    lab_waste=Label(waste1,text=' ',bg='#ff8484',).pack(fill='x')
    waste1.pack(fill='x')
    frame2=Frame(window_f,bg='#ff8484')
    password_l=Label(frame2,text='  Password   : ',font=("Ariel",16),bg='#ff8484')
    password_l.pack(side='left')
    password_f=Entry(frame2,show="*",width=20,font=("Ariel",16))
    password_f.pack(side='left')
    frame2.pack(fill='x')
    waste2=Frame(window_f,bg='#ff8484')
    lab_waste=Label(waste2,text=' ',bg='#ff8484',).pack(fill='x')
    waste2.pack()
    frame1=Frame(window_f,bg='#ff8484')
    #label_w=Label(frame1,text='                             ',bg='#ff8484').pack(side='left')
    button=Button(frame1,text='Submit',font=("Ariel",12),command=sub_btn)
    button.pack()
    frame1.pack()
    window_f.mainloop()
def destroy():
    window.destroy()
def clear(event):
    entry.delete(0,END)
    entry.config(fg='black')
    entry.unbind('<Button-1>')
def submit(event=0):
    def count_button():
        s3=boto3.resource('s3')
        my_b=s3.Bucket('530045registration')
        p_count=0
        for i in my_b.objects.all():
            p_count=p_count+1
        p_count_l.config(text="Count of patients : {}".format(p_count))
    def text_visible(event=0):
        p_count_l.config(text='')
    def upload():
        window.file=filedialog.askopenfilename()
        print(window.file)
    def doctor_details():
        window1=Tk()
        window1.geometry('-0+80')
        window1.title("Doctor Details")
        f2=Frame(window1)
        f2.configure(background='#ff8484')
        L2=Label(f2,bg='#ff8484',text="Doctor's Details:",font=("Monaco",28))
        L2.pack(side='left')
        f2.pack(side=TOP,fill='x')
        f92=Frame(window1)
        f92.configure(bg='#ff8484')
        l14=Label(f92,text='+++++++++++++++++++++++++++++++++++++++++++++',bg='#ff8484').pack(side='left')
        f92.pack(fill='x')
        f2_1=Frame(window1)
        f2_1.configure(background='#ff8484')
        L2_1=Label(f2_1,bg='#ff8484',text="Doctor Name : {0}".format(d_name),font=("Ariel",24))
        L2_1.pack(side='left')
        f2_1.pack(side=TOP,fill='x')
        f2_2=Frame(window1,bg='#ff8484')
        l2_2=Label(f2_2,text="Department    : {0}".format(d_depart),font=("Ariel",24),bg='#ff8484')
        l2_2.pack(side='left')
        f2_2.pack(side=TOP,fill='x')
        f93=Frame(window1)
        f93.configure(bg='#ff8484')
        l15=Label(f93,text=' ',bg='#ff8484').pack(side='left')
        f93.pack(fill='x')
        window1.mainloop()
    def first_window(Event):
        window.destroy()
        mainpage()
    def getdetails(event=0):
        def make_bill():
            global emailid
            pdf1=FPDF()
            pdf1.add_page()
            pdf1.set_font('Arial',size=16)
            pdf1.cell(200,10,txt="Patient Details :",ln=1)
            pdf1.cell(200,10,txt="Patient Name : {}".format(name),ln=1)
            pdf1.cell(200,10,txt="Phone Number : {}".format(pn),ln=1)
            pdf1.cell(200,10,txt="   ",ln=1)
            pdf1.cell(200,10,txt="Medication:",ln=1)
            total=0
            index=x.index('tests')
            for i,j in zip(range(x.index('medication')+1,index),mrp):
                pdf1.cell(200,10,txt="   {0}    {1}".format(x[i],j.get()),ln=1)
                total=total+int(j.get())
            pdf1.cell(200,10,txt="Total Amount : {}".format(total))
            pdf1.output("lab_bill.pdf")
            email_user = 'harshassv.13@gmail.com'
            email_password = 'harsha@2001'
            email_send =emailid
            subject = 'Tablets Bill'
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subject

            body = 'Your Payment Bill'
            msg.attach(MIMEText(body,'plain'))

            filename='lab_bill.pdf'
            attachment  =open(filename,'rb')

            part = MIMEBase('application','octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+filename)

            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(email_user,email_password)


            server.sendmail(email_user,email_send,text)
            server.quit()

        global d_name,d_depart,p_count,emailid
        p_count=0
        bucket=entry.get()
        s3 = boto3.client('s3')
        s3.download_file(bucket, 'details.txt', 'lab.txt')
        x=open('lab.txt','r').read().split('\n')
        doctor_pn=x[2]
        d_name=x[0]
        d_depart=x[1]
        name=x[3]
        age=x[6]
        weight=x[7]
        pn=x[5]
        gender=x[4]
        emailid=x[8]
        bucket='530045lab'
        os.remove("lab.txt")
        window1.destroy()
        global window
        window=Tk()
        window.wm_attributes('-fullscreen',True)
        window.configure(background='#ff8484')
        f_back=Frame(window,bg='#ff8484')
        back_image=PhotoImage(file="Back_Arrow.png")
        back_label=Label(f_back,image=back_image,bg='#ff8484')
        back_label.pack(side='left')
        back_label.bind('<Button-1>',first_window)
        f_back.pack(fill='x')
        '''f11=Frame(window)
        f11.configure(bg='#ff8484')
        l10=Label(f11,bg='#ff8484',font=("Monaco",24),text='Some more Good Deeds to be done,for those coming up!')
        l10.pack(side='left')
        l11=Label(f11,bg='#ff8484',font=("Ariel",24),text='    {}'.format(p_count))
        l11.pack(side='left')
        f11.pack(fill='x')'''
        f3=Frame(window)
        f3.configure(background='#ff8484')
        L4=Label(f3,bg='#ff8484',text="Patient's Details:",font=("Monaco",28))
        L4.pack(side='left')
        L00=Label(f3,bg='#ff8484',text="    ")
        L00.pack(side='right')
        B4=Button(f3,text='Doctor Details',command=doctor_details,font=("Ariel",14))
        B4.pack(side='right')
        f3.pack(fill='x')
        f4=Frame(window)
        f4.configure(background='#ff8484')
        L5=Label(f4,bg='#ff8484',text="Name\t\t: {0}".format(name),font=("Ariel",24))
        L5.pack(side='left')
        f4.pack(fill='x')
        f7=Frame(window)
        f7.configure(bg='#ff8484')
        L6=Label(f7,bg='#ff8484',text="Gender\t\t:  {0}".format(gender),font=("Ariel",24))
        L6.pack(side='left')
        f7.pack(fill='x')
        f4_1=Frame(window)
        f4_1.configure(bg='#ff8484')
        pn_p=Label(f4_1,bg='#ff8484',text="Phone Number     :   {0}".format(pn),font=("Ariel",24))
        pn_p.pack(side='left')
        f4_1.pack(fill='x')
        f4_12=Frame(window)
        f4_12.configure(bg='#ff8484')
        p_a=Label(f4_12,bg='#ff8484',text="Age\t\t:  {0}".format(age),font=("Ariel",24))
        p_a.pack(side='left')
        f4_12.pack(fill='x')
        f4_2=Frame(window)
        f4_2.configure(bg='#ff8484')
        pn_w=Label(f4_2,bg='#ff8484',text="Weight\t\t:  {0}".format(weight),font=("Ariel",24))
        pn_w.pack(side='left')
        f4_2.pack(fill='x')
        f5_w=Frame(window,bg='#ff8484')
        L_w=Label(f5_w,bg='#ff8484').pack()
        f5_w.pack(fill='x')
        f5=Frame(window)
        f5.configure(background='#ff8484')
        #x=open('tests.txt','r').read().split('\n')
        L7=Label(f5,bg='#ff8484',text="Tests:",font=("Monaco",28))
        L7.pack(side='left')
        f5.pack(fill='x')
        mrp=[]
        index=x.index('tests')
        for i in range(x.index('medication')+1,index):
            if x[i]!='':
                f6=Frame(window,background='#ff8484')
                dot=Label(f6,text='o',font=("Ariel",20),bg='#ff8484').pack(side='left')
                tests1=Label(f6,text=x[i],font=("Ariel",24),bg='#ff8484').pack(side='left')
                label_w=Label(f6,text='       ',bg='#ff8484').pack(side='left')
                entry_1=Entry(f6,font=('Arial',15),width=4)
                entry_1.pack(side='left')
                mrp.append(entry_1)
                rs=Label(f6,text=' RS',font=('Arial',10),bg='#ff8484').pack(side='left')
                f6.pack(fill='x')
            #waste=Label(f6,text='',font=("Ariel",14),bg='#ff8484').pack(side='top')
        #f6.pack(fill='x')
        f9=Frame(window)
        f9.configure(bg='#ff8484')
        l12=Label(f9,text=' ',bg='#ff8484').pack(side='left')
        f9.pack(fill='x')
        f8=Frame(window)
        b2=Button(f8,text='Generate Bill',command=make_bill,font=('Arial',18))
        b2.pack()
        f8.pack()
        window.mainloop()

    if username_e.get()==username and password_e.get()==password:
        global entry,window1
        destroy()
        def mainpage():
            def exit_f():
                window1.destroy()
            global entry,window1,p_count_l
            window1=Tk()
            window1.configure(bg='#ff8484')
            frame1=Frame(window1,bg='#ff8484')
            frame2=Frame(window1,bg='#ff8484')
            l_w=Label(frame2,text=' ',bg='#ff8484').pack(fil='x')
            label=Label(frame1,text='Phone Number : ',font=("Ariel",16),bg='#ff8484')
            label.pack(side='left')
            entry=Entry(frame1,font=("Ariel",16),width=20,fg='#d3d3d3')
            entry.insert(0,'Ex: 7986410542')
            entry.bind('<Return>',getdetails)
            entry.bind('<Button-1>',clear)
            entry.pack(side='left')
            entry_w=Label(frame1,text='       ',bg='#ff8484').pack(side='left')
            button=Button(frame1,text="Get Details",font=("Ariel",15),command=getdetails)
            button.pack(side='left')
            frame2.pack(side='top',fill='x')
            frame1.pack(fill='x')
            frame3_w=Frame(window1,bg='#ff8484')
            l_w=Label(frame3_w,text='',bg='#ff8484').pack(fill='x')
            frame3_w.pack()
            frame3=Frame(window1,bg='#ff8484')
            p_count_b=Button(frame3,text="Patient Count",font=('Arial',20),command=count_button)
            p_count_b.pack()
            frame3.pack()
            frame4=Frame(window1,bg='#ff8484')
            p_count_l=Label(frame4,text='',bg='#ff8484',font=('Arial',24))
            p_count_l.bind('<Button-1>',text_visible)
            p_count_l.pack()
            frame4.pack()
            for i in range(0,4):
                frame3_w=Frame(window1,bg='#ff8484')
                l_w=Label(frame3_w,text='',bg='#ff8484').pack(fill='x')
                frame3_w.pack(side='bottom')
            frame5=Frame(window1,bg='#ff8484')
            exit=Button(frame5,text="EXIT",font=('Arial',20),command=exit_f)
            exit.pack()
            frame5.pack(side='bottom')
            window1.resizable(0,0)
            window1.wm_attributes('-fullscreen','true')
            window1.mainloop()
        mainpage()
    else:
        messagebox.showerror('Error','Entered Credentials are incorrect')
window=Tk()
window.configure(bg='#ff8484')
window.geometry('700x650+200+2')
window.resizable(0,0)
window.wm_attributes('-fullscreen','true')
frame0=Frame(window,bg='#ff8484')
l=Label(frame0,text="ADMIN PAGE",font=("Ariel",19),bg='#ff8484')
l.pack()
frame0.pack()
waste=Frame(window,bg='#ff8484')
lab_waste=Label(waste,bg='#ff8484',).pack(fill='x')
waste.pack()
frame1=Frame(window,bg='#ff8484')
username_l=Label(frame1,text='User Name : ',font=("Ariel",16),bg='#ff8484')
username_l.pack(side='left')
username_e=Entry(frame1,width=20,font=("Ariel",16))
username_e.pack(side='left')
frame1.pack()
waste1=Frame(window,bg='#ff8484')
lab_waste=Label(waste1,bg='#ff8484',).pack(fill='x')
waste1.pack()
frame2=Frame(window,bg='#ff8484')
password_l=Label(frame2,text='Password   : ',font=("Ariel",16),bg='#ff8484')
password_l.pack(side='left')
password_e=Entry(frame2,show="*",width=20,font=("Ariel",16))
password_e.bind('<Return>',submit)
password_e.pack(side='left')
frame2.pack()
waste2=Frame(window,bg='#ff8484')
lab_waste=Label(waste2,bg='#ff8484',).pack(fill='x')
waste2.pack()
frame1=Frame(window,bg='#ff8484')
#label_w=Label(frame1,text='                             ',bg='#ff8484').pack(side='left')
button=Button(frame1,text='Submit',font=("Ariel",12),command=submit)
button.pack()
lab_waste=Label(frame1,text='       ',bg='#ff8484',).pack()
button1=Button(frame1,text='Forgot Password',font=("Ariel",12),command=forgot)
button1.pack()
frame1.pack()
frame1_w=Frame(window,bg='#ff8484')
label1_w2=Label(frame1_w,text=' ',bg='#ff8484').pack()
frame1_w.pack(fill='x')
frame2=Frame(window,bg='#ff8484')
button_destroy=Button(frame2,text='close',font=("Ariel",12),command=destroy)
button_destroy.pack()
frame2.pack()
window.mainloop()
