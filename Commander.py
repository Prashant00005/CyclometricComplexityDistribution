#print 'hello world'
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json, requests, time, getpass


app = Flask(__name__)
api = Api(app)

class CommanderServer():
    
    def __init__(self):
    
        self.Subjects = input("How many workers do you want to create:")
        
        self.Subjects = int(self.Subjects)  #Stores the number of workers created
        self.Current_Subjects = 0  # Initializing the no. of subjects that have connected to server
        self.timer = 0.0  
       
        
        Username_Repo = input("Enter Github Username ")
        Length_Username_Repo = len(Username_Repo)
        
        if  Length_Username_Repo != 0:     #To check for null pointer
            Password_Repo = getpass.getpass("Type your Github password (input is hidden): ")
        
        Curr_RepoPage = 1  #initialize page with First page
        
        flag = True  #to check for more number of pages
         
        self.List_Commits = []  # List of all commits
        
        while flag:
            
            
        
            if Length_Username_Repo == 0:
                r = requests.get("https://api.github.com/repos/Prashant00005/Distributed_File_Systems/commits?page={}&per_page=100".format(Curr_RepoPage))  
            else:
                r = requests.get("https://api.github.com/repos/Prashant00005/Distributed_File_Systems/commits?page={}&per_page=100".format(Curr_RepoPage), auth=(Username_Repo, Password_Repo))
                
            string_json = json.loads(r.text)
            Length_string_json = len(string_json)
            
            if  Length_string_json < 2:
             
                flag = False
                print("Iteration of all pages done!!")
            
            else:
                
                for sub_json in string_json:
                    self.List_Commits.append(sub_json['sha'])  #Keep on adding to get total
                    print("Commit ID  given is Sha: {}".format(sub_json['sha']))
                    
                print("\n")
                print("\n")
                Curr_RepoPage = Curr_RepoPage + 1
        
        Length_List_Commits = len(self.List_Commits)
        self.totalCommits = Length_List_Commits
        self.Total_List_CC = []
        
        print("Total number of commits are : ".format(self.totalCommits))


if __name__ == "__main__":
    app.run(port=8084)
    Commander_Obj = CommanderServer()  #creates object of Commander Server class
    