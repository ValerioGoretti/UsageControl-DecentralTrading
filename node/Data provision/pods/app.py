from ast import Subscript
from cgitb import text
from re import A
#import resource
from threading import Thread
import tkinter as tk      
from tkinter import filedialog

from tkinter import E, EW, LEFT, W, font as tkfont
from webbrowser import get  
import DTpod_service
import os
import shutil
from DTaddresses import *
import json
from DTpod_service import StoppableHTTPServer, DTpod_service
from DTobligation_oracle import DTobligation_oracle
from DTindexing_oracle import DTindexing_oracle
from tkinter import filedialog as fd
from tkinter import messagebox

"""
The class is the controller entity of the graphical user interface for the pod management.
Contains the logic for controlling windows and view transitions.
The views of the application are implemented through the TKinter python library and modelled as tk.Frame subclasses.
""" 
class App(tk.Tk):
    """
    Class initializer.
    Sets up the main window settings
    """ 
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.pod_path=""
        self.title_font = tkfont.Font(size=15)
        width= self.winfo_screenwidth()               
        height= self.winfo_screenheight()               
        self.geometry("%dx%d" % (width, height))
        self.resizable(False,False)
        self.domain_dict={1:"Social",2:"Finance",3:"Medical",None:"None"}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in [WelcomePage]:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("WelcomePage")
    """
    Transition function.
    """     
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


"""
Class implementing the welcome page of the application.
Allows users to open a local pod or to create a new one.
""" 
class WelcomePage(tk.Frame):  
    """
    Sets up the main graphical elements of the view.
    """ 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent=parent
        label = tk.Label(self, text="Welcome to DTPodManager", font=controller.title_font).grid(column=1,row=0)
        podsRegistration=tk.LabelFrame(self, text="Register a new Pod",labelanchor='n',padx=10,pady=10)
        tk.Label(podsRegistration, text="Domain name of the Pod: ").grid(column=0,row=0)
        e1 = tk.Entry(podsRegistration)
        e1.grid(column=1,row=0)
        self.social=tk.IntVar()
        self.finance=tk.IntVar()
        self.medical=tk.IntVar()
        tk.Label(podsRegistration, text="Pod type: ").grid(column=0,row=1)
        frame_checkbutton=tk.Frame(podsRegistration)
        c1 = tk.Checkbutton(frame_checkbutton, text='Social',variable=self.social, onvalue=1, offvalue=0).grid(column=0,row=0,sticky=W)
        c2 = tk.Checkbutton(frame_checkbutton, text='Finance',variable=self.finance, onvalue=1, offvalue=0).grid(column=1,row=0,sticky=W)
        c3 = tk.Checkbutton(frame_checkbutton, text='Medical',variable=self.medical, onvalue=1, offvalue=0).grid(column=2,row=0,sticky=W)
        frame_checkbutton.grid(column=1,row=1)
        tk.Label(podsRegistration, text="Owner public key: ").grid(column=0,row=2)
        public_key_owner = tk.Entry(podsRegistration)
        public_key_owner.grid(column=1,row=2)
        tk.Label(podsRegistration, text="Owner private key: ").grid(column=0,row=3)
        private_key_owner = tk.Entry(podsRegistration)
        private_key_owner.grid(column=1,row=3)
        button2 = tk.Button(podsRegistration, text="submit", command = lambda:self.submit_validation(public_key_owner.get(),private_key_owner.get(),e1.get())).grid(column=2,row=4)
        podsRegistration.grid(column=1,row=1)
        open_pod=tk.Button(self, text="Open pod from filesystem", command = lambda:self.show_pod_page()).grid(column=1,row=2)
    """
    Starts the pod initialization procedure.
    """         
    def register_pod(self,public_key,private_key,pod_reference,pod_type):
        pod_location = filedialog.askdirectory()
        pod_location=pod_location+"/"+pod_reference
        indexing_oracle=DTindexing_oracle(DTINDEXING,private_key)
        id,public_key_pod,private_key_pod,obligation_address=indexing_oracle.register_Pod(bytes(pod_reference, 'utf-8'),pod_type,public_key,private_key)
        self.generate_config_files(pod_location,id,public_key_pod,public_key,private_key_pod,obligation_address)
    """
    Sets up the DTobligation.json and DTconfig.json files.
    """ 
    def generate_config_files(self,pod_location,id,address,owner,private_key,obligations_address):
        os.makedirs(os.path.dirname(pod_location+"/"+"DTconfig.json"), exist_ok=True)
        with open(pod_location+"/"+"DTconfig.json", 'w') as f:
            config={"id": id, "address": address, "resources": [], "owner": owner, "private_key": private_key}
            json.dump(config, f, indent=2)
        with open(pod_location+"/"+"DTobligations.json", 'w') as f2:
            obligations={"default": {},"address":obligations_address}
            json.dump(obligations, f2, indent=2)

    """
    Validation of the pod's initialization fields.
    """ 
    def submit_validation(self,public_key_owner,private_key_owner,pod_reference):
        
        if self.social.get()==self.medical.get()==self.finance.get()==0:
            messagebox.showerror('Error', 'Please choose an alternative')
            return False
        dictio={str(self.social):1,str(self.medical):3,str(self.finance):2}
        n_set=0
        result=-1
        for d in [self.social,self.medical,self.finance]:
            if d.get()==1:
                n_set+=1
                result=dictio[str(d)]
        if n_set>1:
            messagebox.showerror('Error', 'Please choose only one alternative')
        else:  
            self.register_pod(public_key_owner,private_key_owner,pod_reference,result)    

    """
    Transition function to the Pod's view.
    """ 
    def show_pod_page(self,pod_path="C:\\Users\\david\\Desktop\\DTPod"):

        pod_location = filedialog.askdirectory()
        self.controller.pod_path=pod_location
        pod_frame = PodManagement(parent=self.parent, controller=self.controller)
        pod_frame.grid(column=0,row=0,sticky="nsew")
        pod_frame.tkraise()

class ResourceManagement(tk.Frame):
        def __init__(self, parent, controller,resource_information):
            tk.Frame.__init__(self, parent,padx=10,pady=20)
            self.controller = controller
            self.parent=parent
            self.resource_info=resource_information
            self.resource_id=resource_information['id']
            self.initialize_layout()


        def initialize_layout(self):
            for widget in self.winfo_children():
                widget.destroy()
            label = tk.Label(self, text="Resource Page", font=self.controller.title_font)
            label.grid(column=1,row=0)
            button1 = tk.Button(self, text="Back to the Pod Page",
                                command=lambda: self.back_to_pod()).grid(column=0,row=1)
            
            button2 = tk.Button(self, text="Open the resource",
                                command=lambda: self.controller.show_frame("PodManagement")).grid(column=1,row=1)
            button2 = tk.Button(self, text="Open the resource",command=lambda: self.controller.show_frame("PodManagement")).grid(column=2,row=1)
            information_frame=tk.LabelFrame(self, text="Resources's Information",labelanchor='n',padx=10,pady=10)
            tk.Label(information_frame, text=("Resource Id: "+str(self.resource_info['id']))).grid(column=0,row=0,sticky=W)
            tk.Label(information_frame, text="Resource Location: "+self.resource_info['location']).grid(column=0,row=1,sticky=W)
            tk.Label(information_frame, text="Has specific obligation rules: "+str(self.resource_info['hasSpecificObligations'])).grid(column=0,row=2,sticky=W)
            information_frame.grid(column=1,row=2)
            Resource_infromation=tk.LabelFrame(self, text="Resource Obligation",labelanchor='n',padx=10,pady=10)
            if self.resource_info['hasSpecificObligations']:
                self.specific_obligations=self.read_resource_obligations()
            

            obligations_frame=tk.LabelFrame(self, text="Resource Pod Obligations",labelanchor='n',padx=10,pady=10)
            #label_ob = tk.Label(self, text="Default Pod obligations",font=self.controller.title_font).grid(column=1,row=3)
            tk.Label(obligations_frame, text="Access Counter Obligation: "+str(self.read_specific_obligations('access_counter'))).grid(column=0,row=0,sticky=W)
            tk.Label(obligations_frame, text="Set").grid(column=1,row=0)
            entry_access = tk.Entry(obligations_frame)
            entry_access.grid(column=2,row=0,sticky=W)
            submit_access=tk.Button(obligations_frame, text="Submit", command=lambda:self.send_access_counter_obligation(self.resource_id,int(entry_access.get()))).grid(column=3,row=0)
            remove_access=tk.Button(obligations_frame, text="Remove obligation",command=lambda:self.remove_access_counter_obligation()).grid(column=4,row=0)


        # tk.Frame(se,background="#000000").grid(row=4,column=1)
            tk.Label(obligations_frame, text="Temporal Obligation: "+str(self.read_specific_obligations('temporal'))).grid(column=0,row=1,sticky=W)
            tk.Label(obligations_frame, text="Set").grid(column=1,row=1)
            entry_temporal = tk.Entry(obligations_frame)
            entry_temporal.grid(column=2,row=1,sticky=W)
            submit_temporal=tk.Button(obligations_frame, text="Submit", command=lambda:self.send_temporal_obligation(self.resource_id,int(entry_temporal.get()))).grid(column=3,row=1)
            remove_access=tk.Button(obligations_frame, text="Remove obligation",command=lambda:self.remove_temporal_obligation()).grid(column=4,row=1)

            tk.Label(obligations_frame, text="Domain Obligation: "+(self.controller.domain_dict[self.read_specific_obligations('domain')])).grid(column=0,row=2,sticky=W)
            domain_frame=tk.Frame(obligations_frame)
            self.social = tk.IntVar()
            self.finance=tk.IntVar()
            self.medical=tk.IntVar() 
            c1 = tk.Checkbutton(domain_frame, text='Social',variable=self.social, onvalue=1, offvalue=0).grid(column=0,row=0,sticky=W)
            c2 = tk.Checkbutton(domain_frame, text='Finance',variable=self.finance, onvalue=1, offvalue=0).grid(column=1,row=0,sticky=W)
            c3 = tk.Checkbutton(domain_frame, text='Medical',variable=self.medical, onvalue=1, offvalue=0).grid(column=2,row=0,sticky=W)

            domain_frame.grid(column=1,row=2)
            submit_Domain=tk.Button(obligations_frame, text="Submit",command=lambda: self.submit_domain_button()).grid(column=3,row=2)
            tk.Button(obligations_frame, text="Remove obligation",command=lambda:self.remove_domain_obligation(self.resource_id)).grid(column=4,row=2)


            
            tk.Label(obligations_frame, text="Country Obligation: "+str(self.read_specific_obligations('country'))).grid(column=0,row=3,sticky=W)
            tk.Label(obligations_frame, text="Set").grid(column=1,row=3)
            entry_Country = tk.Entry(obligations_frame)
            entry_Country.grid(column=2,row=3,sticky=W)
            submit_Context=tk.Button(obligations_frame, text="Submit",command=lambda: self.send_country_obligation(self.resource_id,int(entry_Country.get()))).grid(column=3,row=3)
            tk.Button(obligations_frame, text="Remove obligation",command=lambda: self.remove_country_obligation(self.resource_id)).grid(column=4,row=3)
            obligations_frame.grid(column=1,row=3)
            
            

        def read_obligations(self):
            f = open(self.controller.pod_path+"\\DTobligations.json",mode='r')
            obligations=json.load(f)

            return obligations
        def read_resource_obligations(self):
            try:
                f = open(self.controller.pod_path+"\\DTobligations.json",mode='r')
                obligations=json.load(f)
                return obligations[str(self.resource_info['id'])]
            except Exception:
                return None
        def read_specific_obligations(self,obligation_name):
            try:
                return self.specific_obligations[obligation_name]
            except:
                return None
        def send_access_counter_obligation(self,id,access_counter):
            self.controller.obligations_oracle.set_access_counter_obligation(id,access_counter)
            self.write_obligation("access_counter",access_counter)
           # self.initialise_layout()
        def send_temporal_obligation(self,id,temporal_obligation):
            self.controller.obligations_oracle.set_temporal_obligation(id,temporal_obligation)
            self.write_obligation("temporal",temporal_obligation)
        def submit_domain_button(self):
            if self.social.get()==self.medical.get()==self.finance.get()==0:
                messagebox.showerror('Error', 'Please choose an alternative')
                return False
            dictio={str(self.social):1,str(self.medical):3,str(self.finance):2}
            n_set=0
            result=-1
            for d in [self.social,self.medical,self.finance]:
                if d.get()==1:
                    n_set+=1
                    result=dictio[str(d)]
            if n_set>1:
                messagebox.showerror('Error', 'Please choose only one alternative')
            else:
                self.controller.obligations_oracle.set_domain_obligation(self.resource_id,result)
                self.send_domain_obligation(self.resource_id,result)


                



        def write_obligation(self,obligation,value):
            file=self.read_obligations()
            resource_obligations=self.read_resource_obligations()
            if resource_obligations==None:
                resource_obligations={}
            resource_obligations[obligation]=value
            file[str(self.resource_info['id'])]=resource_obligations
            with open(self.controller.pod_path+"\\DTobligations.json", "w") as outfile:
                json.dump(file,outfile)
            return True
        def remove_obligation(self,obligation):
            file=self.read_obligations()
            resource_obligations=file[str(self.resource_id)]
            resource_obligations.pop(obligation)
            file[str(self.resource_info['id'])]=resource_obligations
            with open(self.controller.pod_path+"\\DTobligations.json", "w") as outfile:
                json.dump(file,outfile)
            return True             
        def remove_access_counter_obligation(self):
            self.controller.obligations_oracle.deactivate_access_counter_obligation(self.resource_id)
            self.remove_obligation("access_counter")
        def remove_temporal_obligation(self):
            self.controller.obligations_oracle.deactivate_temporal_obligation(self.resource_id)
            self.remove_obligation("temporal")

        def send_country_obligation(self,id,country):
            self.controller.obligations_oracle.set_country_obligation(id,country)
            self.write_obligation("country",country)
            #self.initialise_layout()
        
        def send_domain_obligation(self,id,domain):
            self.controller.obligations_oracle.set_domain_obligation(id,domain)
            self.write_obligation("domain",domain)
        def remove_country_obligation(self,id):
            self.controller.obligations_oracle.deactivate_country_obligation(id)
            self.remove_obligation("country")
        def remove_domain_obligation(self,id):
            self.controller.obligations_oracle.deactivate_domain_obligation(id)
            self.remove_obligation("domain")

        def back_to_pod(self):
            pod_frame = PodManagement(parent=self.parent, controller=self.controller)
            pod_frame.grid(column=0,row=0,sticky="nsew")
            pod_frame.tkraise()







"""
Class implementing the view to control a specific pod.
Allows users add/remove resources, starts the pod web service and control pod's information.
""" 
class PodManagement(tk.Frame):
    """
    Sets up the main graphical elements of the window.
    """ 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,padx=10,pady=20)
        self.parent=parent
        self.controller = controller
        validation_result=self.validate_path(self.controller.pod_path)
        if(validation_result):
            def handler(*args):
                DTpod_service(self.controller.pod_pk,*args)
            self.pod=StoppableHTTPServer(('localhost',9999),handler,self.controller.pod_path)
            self.controller.push_in_indexing=DTindexing_oracle(DTINDEXING,self.controller.pod_pk)
            self.initialise_layout()
        else:
            label = tk.Label(self, text="Pod Management",font=controller.title_font)
            address = tk.Label(self, text="The given path does not contain a DTPod").grid(0,0)
    """
    Sets up the pod management view
    """     
    def initialise_layout(self):
        for widget in self.winfo_children():
            widget.destroy()
        obligations=self.read_obligations()
        self.controller.obligations=obligations
        self.controller.obligations_oracle=DTobligation_oracle(self.controller.obligations['address'],self.controller.pod_pk)
        label = tk.Label(self, text="Pod Management ",font=self.controller.title_font)
        label.grid(column=1,row=0)
        information_frame=tk.LabelFrame(self, text="Pod's Information",labelanchor='n',padx=10,pady=10)
        tk.Label(information_frame, text="Address: "+self.controller.pod_address).grid(column=0,row=0,sticky=W)
        pod_path= tk.Label(information_frame, text="Pod path: "+self.controller.pod_path).grid(column=0,row=1,sticky=W)
        pod_owner= tk.Label(information_frame, text="Pod owner: "+self.controller.pod_owner,).grid(column=0,row=2,sticky=W)
        information_frame.grid(column=1,row=1)
        button = tk.Button(self, text="Start the pod",
                            command=lambda: self.start_server())
        button2=tk.Button(self, text="Stop the pod",
                            command=lambda: self.stop_server())
        button3=tk.Button(self, text="Add resource",
                            command=lambda: self.register_resource('0xcE0cb7B19c77De88dcD6c20E2d69cf1e57F6F1fB',self.controller.pod_id,0))


        button.grid(column=0,row=2)
        button2.grid(column=1,row=2)
        button3.grid(column=2,row=2)
        obligations_frame=tk.LabelFrame(self, text="Default Pod Obligation",labelanchor='n',padx=10,pady=10)
        tk.Label(obligations_frame, text="Default Access Counter: "+str(self.get_default_obligation_value('access_counter'))).grid(column=0,row=0,sticky=W)
        tk.Label(obligations_frame, text="Set").grid(column=1,row=0)
        entry_access = tk.Entry(obligations_frame)
        entry_access.grid(column=2,row=0,sticky=W)
        submit_access=tk.Button(obligations_frame, text="Submit", command=lambda: self.send_default_access_counter_obligation(int(entry_access.get()))).grid(column=3,row=0)
        remove_access=tk.Button(obligations_frame, text="Remove obligation" ,command=lambda: self.remove_default_access_counter_obligation()).grid(column=4,row=0)

        tk.Label(obligations_frame, text="Default Temporal Obligation: "+str(self.get_default_obligation_value('temporal'))).grid(column=0,row=1,sticky=W)
        tk.Label(obligations_frame, text="Set").grid(column=1,row=1)
        entry_temporal = tk.Entry(obligations_frame)
        entry_temporal.grid(column=2,row=1,sticky=W)
        submit_temporal=tk.Button(obligations_frame, text="Submit",command=lambda: self.send_default_temporal_obligation(int(entry_temporal.get()))).grid(column=3,row=1)
        remove_access=tk.Button(obligations_frame, text="Remove obligation" ,command=lambda: self.remove_default_temporal_obligation()).grid(column=4,row=1)

        tk.Label(obligations_frame, text="Domain Obligation: "+self.controller.domain_dict[self.get_default_obligation_value('domain')]).grid(column=0,row=2,sticky=W)
        domain_frame=tk.Frame(obligations_frame)
        self.social = tk.IntVar()
        self.finance=tk.IntVar()
        self.medical=tk.IntVar() 
        c1 = tk.Checkbutton(domain_frame, text='Social',variable=self.social, onvalue=1, offvalue=0).grid(column=0,row=0,sticky=W)
        c2 = tk.Checkbutton(domain_frame, text='Finance',variable=self.finance, onvalue=1, offvalue=0).grid(column=1,row=0,sticky=W)
        c3 = tk.Checkbutton(domain_frame, text='Medical',variable=self.medical, onvalue=1, offvalue=0).grid(column=2,row=0,sticky=W)
        domain_frame.grid(column=1,row=2)
        submit_Domain=tk.Button(obligations_frame, text="Submit",command=lambda: self.submit_domain_button()).grid(column=3,row=2)
        tk.Button(obligations_frame, text="Remove obligation",command=lambda: self.remove_default_domain_obligation()).grid(column=4,row=2)

        tk.Label(obligations_frame, text="Country Obligation: "+str(self.get_default_obligation_value('country'))).grid(column=0,row=3,sticky=W)
        tk.Label(obligations_frame, text="Set").grid(column=1,row=3)
        entry_Country = tk.Entry(obligations_frame)
        entry_Country.grid(column=2,row=3,sticky=W)
        submit_Context=tk.Button(obligations_frame, text="Submit",command=lambda: self.send_default_country_obligation(int(entry_Country.get()))).grid(column=3,row=3)
        tk.Button(obligations_frame, text="Remove obligation",command=lambda:self.remove_default_country_obligation()).grid(column=4,row=3)
        
        
        obligations_frame.grid(column=1,row=3)
        initialisesd_reources=tk.LabelFrame(self, text="Initialised Resources",labelanchor='n',font=self.controller.title_font,padx=10,pady=10)
        res=self.get_initialised_resources()
        row_counter=0
        for r in res:
            location=r['location']
            id=r['id']
            print(id,self.hasSpecificRules(id))
            tk.Label(initialisesd_reources, text=location+"  id:"+str(id)).grid(column=0,row=row_counter)
            
            tk.Button(initialisesd_reources, text="Remove resource",
                        command=lambda parameter=id: self.remove_resource(parameter)).grid(column=1,row=row_counter)
            tk.Button(initialisesd_reources, text="See resource",
                        command=lambda parameter=r: self.show_resource_page(parameter)).grid(column=2,row=row_counter)
            row_counter=row_counter+1
        initialisesd_reources.grid(column=1,row=4)
    """
    Starts the recording of a new default domain rule for the pod.
    """       
    def submit_domain_button(self):
        if self.social.get()==self.medical.get()==self.finance.get()==0:
            messagebox.showerror('Error', 'Please choose an alternative')
            return False
        dictio={str(self.social):1,str(self.medical):3,str(self.finance):2}
        n_set=0
        result=-1
        for d in [self.social,self.medical,self.finance]:
            if d.get()==1:
                n_set+=1
                result=dictio[str(d)]
        if n_set>1:
            messagebox.showerror('Error', 'Please choose only one alternative')
        else:
            self.send_default_domain_obligation(result)
    """
    Starts the HTTP web service for the resources delivery.
    """ 
    def start_server(self):
        thread = Thread(None, self.pod.serve_forever)
        thread.start()
    """
    Starts the HTTP web service for the pod.
    """ 
    def get_initialised_resources(self):
        f = open(self.controller.pod_path+"\\DTconfig.json")
        config=json.load(f)
        return config['resources']
    """
    Stops the HTTP web service for the pod.
    """         
    def stop_server(self):
        self.pod.force_stop()
        def handler(*args):
            DTpod_service(self.controller.pod_pk,*args)
        self.pod=StoppableHTTPServer(('localhost',9999),handler,self.controller.pod_path)
    """
    Initializes the procedure to deactivate a pod's resource.
    """ 
    def remove_resource(self,resId):
        self.controller.push_in_indexing.deactivate_resource(resId);
        f = open(self.controller.pod_path+"\\DTconfig.json")
        config=json.load(f)
        resources=config['resources']
        new_resources=[]
        location=None
        for res in resources:
            if res['id']!=resId:
                new_resources.append(res)
            else:
                location=res['location']
        config['resources']=new_resources
        with open(self.controller.pod_path+"\\DTconfig.json", "w") as outfile:
            json.dump(config,outfile)
        path_to_remove=self.controller.pod_path+location
        path_to_remove=path_to_remove.replace("/","\\")
        os.remove(path_to_remove)
        self.initialise_layout()

    """
    Verifies the validity of the DTconfig.json file
    """     
    def validate_path(self,path):
        config_exist=os.path.exists(path+"\\DTconfig.json")
        if config_exist:
            f = open(path+"\\DTconfig.json")
            config=json.load(f)
            self.controller.pod_address=config["address"]
            self.controller.pod_owner=config["owner"]
            self.controller.pod_pk=config["private_key"]
            self.controller.pod_id=config["id"]
            f.close()
        return config_exist

    """
    Retrieves the default obligation rules related to the pod.
    """ 
    def get_default_obligation_value(self,obligation_name):
        try:
            return self.controller.obligations['default'][obligation_name]
        except:
            return None
    """
    Add a resource in the DTconfig.json file
    """ 
    def add_resource_to_config(self,path,id_resource,location):
        config_exist=os.path.exists(path+"\\DTconfig.json")
        if config_exist:
            f = open(path+"\\DTconfig.json",mode='r')
            config=json.load(f)
            print(config['resources'])
            new_resource={'id':id_resource,'location':location}
            config['resources'].append(new_resource)
            with open(path+"\\DTconfig.json", "w") as outfile:
            
                json.dump(config,outfile)
            return True
        return False


    """
    Initialize a new resource in the pod.
    """
    def register_resource(self,reference,podId,subscription):
        path=fd.askopenfilename(title='Select a resource to initialize')
        destination=fd.askdirectory(title='Select a location internal to the pod location',initialdir=self.controller.pod_path)
        print(destination)
        if destination.startswith(self.controller.pod_path.replace("\\","/")) and path!='' and destination!='':
            path_list= path.split("/")
            filename=path_list[len(path_list)-1]
            new_path=destination+"/"+filename
            print(new_path)
            reference_to_register=new_path.replace(self.controller.pod_path.replace("\\","/"),"")
            print(reference_to_register)
            shutil.copyfile(path, new_path)
            byte=bytes(reference_to_register, 'utf-8')
            idResource=self.controller.push_in_indexing.add_resource(byte,podId,subscription)
            self.add_resource_to_config(self.controller.pod_path,idResource,reference_to_register)
            self.initialise_layout()
        else:
             messagebox.showerror('Error', 'Please select a path inside your DTPod location: '+self.controller.pod_path)
    

    """
    Starts the recording of a new default temporal obligation rule.
    """   
    def send_default_temporal_obligation(self,temporal_obligation):
        self.controller.obligations_oracle.set_default_temporal_obligation(temporal_obligation)
        self.write_default_obligations("temporal",temporal_obligation)
        self.initialise_layout()
    """
    Starts the recording of a new default access counter obligation rule.
    """ 
    def send_default_access_counter_obligation(self,access_counter):
        self.controller.obligations_oracle.set_default_access_counter_obligation(access_counter)
        self.write_default_obligations("access_counter",access_counter)
        self.initialise_layout()
    """
    Starts the recording of a new default country obligation rule.
    """ 
    def send_default_country_obligation(self,country):
        self.controller.obligations_oracle.set_default_country_obligation(country)
        self.write_default_obligations("country",country)
        self.initialise_layout()
    """
    Starts the recording of a new default domain obligation rule.
    """ 
    def send_default_domain_obligation(self,domain):
                
        self.controller.obligations_oracle.set_default_domain_obligation(domain)
        self.write_default_obligations("domain",domain)
        self.initialise_layout()


    """
    Records a new rule in the local DTobligation.json file
    """ 
    def write_default_obligations(self,obligation_name,value):
        obligations=self.read_obligations()
        obligations['default'][obligation_name]=value
        with open(self.controller.pod_path+"\\DTobligations.json", "w") as outfile:
            json.dump(obligations,outfile)
        return True
    """
    Starts the deactivation of a default access counter obligation rule.
    """  
    def remove_default_access_counter_obligation(self):
        self.controller.obligations_oracle.deactivate_default_access_counter_obligation()
        print(self.cancel_default_obligation_json("access_counter"))
        self.initialise_layout()
    """
    Starts the deactivation of a default access counter obligation rule.
    """      
    def remove_default_temporal_obligation(self):
        self.controller.obligations_oracle.deactivate_default_temporal_obligation()
        print(self.cancel_default_obligation_json("temporal"))
        self.initialise_layout()
    """
    Starts the deactivation of a default domain obligation rule.
    """
    def remove_default_domain_obligation(self):
        self.controller.obligations_oracle.deactivate_default_domain_obligation()
        print(self.cancel_default_obligation_json("domain"))
        self.initialise_layout()
    """
    Starts the deactivation of a default country obligation rule.
    """
    def remove_default_country_obligation(self):
        self.controller.obligations_oracle.deactivate_default_country_obligation()
        print(self.cancel_default_obligation_json("country"))
        self.initialise_layout()
    """
    Remove an obligation rule from the local DTobligations.json file
    """
    def cancel_default_obligation_json(self,obligation_name):
        obligations=self.read_obligations()
        if obligations!=None:
            obligations['default'].pop(obligation_name)
            with open(self.controller.pod_path+"\\DTobligations.json", "w") as outfile:
                json.dump(obligations,outfile)
            return True 
        return False
    """
    Remove an obligation rule from the local DTobligations.json file
    """    
    def read_config_file(self):
        try:
            f = open(self.controller.pod_path+"\\DTconfig.json",mode='r')
            config=json.load(f)
            return config
        except OSError:
            return None
    """
    Read obligation rules from the DTobligations.json file.
    """ 
    def read_obligations(self):
        try:
            f = open(self.controller.pod_path+"\\DTobligations.json",mode='r')
            obligations=json.load(f)
            return obligations
        except OSError:
            return None

    def synchronize_resources(self):
        bc_resources=self.controller.push_in_indexing.get_resource_information(self.controller.pod_id)
        config_file=self.read_config_file()
        if config_file!=None:
            print(config_file)
            print(bc_resources)

    """
    Verifies from the local DTobligation.json file if a resource has dedicated obligation rules.
    """     
    def hasSpecificRules(self,id):
        obligations=self.read_obligations()
        return str(id) in obligations.keys()

    """
    Transition to a resource control page
    """     
    def show_resource_page(self,resource_information):
        resource_information['hasSpecificObligations']=self.hasSpecificRules(resource_information['id'])
        resource_frame = ResourceManagement(parent=self.parent, controller=self.controller,resource_information=resource_information)
        resource_frame.grid(column=0,row=0,sticky="nsew")
        resource_frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()