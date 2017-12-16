#print 'hello world'
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json, requests, time, getpass


app = Flask(__name__)
api = Api(app)


class FindCyclomaticComp(Resource):     #To find commits and find cyclomatic aomplexities
    def __init__(self):  
        #Initializing global object of Commander class
        global Commander_Obj 
        self.server = Commander_Obj
        
        super(FindCyclomaticComp, self).__init__() 
        self.ProcessRequest = reqparse.RequestParser()

       
        self.ProcessRequest.add_argument('CommitSub', type=str, location = 'json')  
        self.ProcessRequest.add_argument('CycloComp', type=float, location='json')

    def get(self):      #If Request is Get
        Length_List_Commits = len(self.server.List_Commits)
        if self.server.Current_Subjects < self.server.Subjects:
            time.sleep(0.1)
            return {'msg': -2}
        
        if Length_List_Commits == 0: 
            return {'msg': -1}
        
        tempVal = self.server.List_Commits[0]
        del self.server.List_Commits[0] 
        print("Resp: {}".format(tempVal))
        return {'msg':tempVal}


    def post(self):     #If Request is Post
        
        args = self.ProcessRequest.parse_args() 
        Length_Total_List_CC = len(self.server.Total_List_CC)
        print("CommitSub got is {}".format(args['CommitSub']))
        print("CycloComp got is {}".format(args['CycloComp']))

        self.server.Total_List_CC.append({'CS':args['CommitSub'], 'CC':args['CycloComp']})
       
        print(self.server.Total_List_CC)
        print(self.server.List_Commits)
        
        if Length_Total_List_CC == self.server.totalCommits: 
            LastTime = time.time() - self.server.startTime
            
            print("End in {} seconds".format(LastTime))
            print(len(self.server.Total_List_CC))
            
            Average_CC = 0
        
            for a in self.server.Total_List_CC:
            
                if a['CC'] > 0:
                    Average_CC = Average_CC + a['CC']
                else:
                    print("Commit {} has no computable files".format(a['CS']))
            
            Average_CC = Average_CC / Length_Total_List_CC
            
            print("The Final Cyclomatic Complexity of the given repository is: {}".format(Average_CC))
        
        return {'success':True}


api.add_resource(FindCyclomaticComp, "/Cyclo", endpoint="Cyclo")



class FetchRepo(Resource):      #To get the Repository Information for subjects
   
    def __init__(self):  
        #Initializing global object of Commander class
        global Commander_Obj 
        self.server = Commander_Obj
        
        super(FetchRepo, self).__init__()
        
        self.ProcessRequest = reqparse.RequestParser()

        # Setting Parameters for JSON 
        self.ProcessRequest.add_argument('FetchStatus', type=int, location = 'json') 
        self.ProcessRequest.add_argument('FindCyclo', type=float, location='json')

    def get(self):
        args = self.ProcessRequest.parse_args()
        if args['FetchStatus'] == False:  #Check repository is not pulled yet 
           
            return {'repo': "https://github.com/Prashant00005/Distributed_File_Systems"}
        
        if args['FetchStatus'] == True:
            self.server.Current_Subjects = self.server.Current_Subjects + 1
            if self.server.Current_Subjects == self.server.Subjects:
                #Starting Timer
                self.server.timer = time.time() 
            print("Number of Subject : {}".format(self.server.Current_Subjects))


api.add_resource(FetchRepo, "/repo", endpoint="repo")


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
    