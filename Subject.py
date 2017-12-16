import json, requests, subprocess
#CLIENT

def run():

    Port_Commander = input("Enter port of commander")
    IP_Commander = input("Enter IP of Commander ")
    Commit_Count = 0    #Initializing commit count 0 at start

    req = requests.get("http://{}:{}/repo".format(IP_Commander,Port_Commander), json={'FetchStatus': False})
    string_json = json.loads(req.text)
    Url_Repository = string_json['repo']
    subprocess.call(["bash", "SubjectScript.sh", Url_Repository])

    req = requests.get("http://{}:{}/repo".format(IP_Commander,Port_Commander), json={'FetchStatus': True}) 

    Pending_Commit = True
    
    while Pending_Commit:
        
        req = requests.get("http://{}:{}/Cyclo".format(IP_Commander,Port_Commander))  
        string_json = json.loads(req.text)
        print(string_json)
        print("Response: {}".format(string_json['msg']))
        if string_json['msg'] == -2: 

           print("Checking")
           
        else:
           
            if string_json['msg'] == -1:
                print("All done!!")
                break
            subprocess.call(["bash", "SubjectCommit.sh", string_json['msg']])
            
            RadonOutput = subprocess.check_output(["radon", "cc", "-s", "-a" , "workerData"])
            
            radonCCOutput = RadonOutput.decode("utf-8")  
            
            print(radonCCOutput)
            
            CC_Average_Start = radonCCOutput.rfind("(")
            
            if radonCCOutput[CC_Average_Start+1:-2] == "":
                print("Error! No file needed..")
                
                req = requests.post("http://{}:{}/cyclomatic".format(IP_Commander,Port_Commander),
                                  json={'CommitSub': string_json['msg'], 'CycloComp': -1})
            else:
                CC_Average = float(radonCCOutput[CC_Average_Start+1:-2]) 
                req = requests.post("http://{}:{}/cyclomatic".format(IP_Commander,Port_Commander),
                                  json={'CommitSub': string_json['msg'], 'CycloComp': CC_Average})
            Commit_Count = Commit_Count + 1 

if __name__ == "__main__":
    run()