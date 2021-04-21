from flask import Flask, request
import requests
import docker
import os


app = Flask(__name__)
client = docker.from_env()
pwd = os.environ['PWD']

# request(method, url, args)


@app.route("/")
def home():
    return {"status":"API working","message":"Check documentation to see how this works"}
    
# input: directory, port
@app.route("/docker/deploy",methods=["POST"])
def generate_docker():
    if(request.is_json):
        try:
            content = request.get_json()
            directory = content['directory']
            port = content['port']

        except:
            return {"status":"error","message":"make sure you include the following items as proper JSON: directory, port"}

        if (not port.isdigit()) and (len(port)== 4 or len(port) == 5):
                return {"status":"error","message":"internalPort expects an integer of size 4 or 5"}    
        
        folder="/files/{}".format(directory) 
        if not (os.path.exists(folder)):
            return {"status":"error","message":"directory not found"}
        elif os.listdir(folder) == []:
            return {"status":"error","message":"no files found in directory"}

        userDir = pwd+folder
        container = client.containers.run("php:7.2-apache",ports={80:port},volumes={userDir: {'bind': '/var/www/html/', 'mode': 'rw'}},detach=True)


        return {"status":"success","message":"deployed docker","id":container.id, "name":container.name}
    else:
        return {"status":"error","message":"not in JSON Format"}
    

# Input: dockerID, action
@app.route("/docker/control",methods=["POST"])
def restart_docker():
    if(request.is_json):
        try:
            content = request.get_json()
            dockerID = content['dockerID']
            action = content['action'].lower()

        except:
            return {"status":"error","message":"make sure you include the following items as proper JSON: dockerID"}

        possibleActions = ["kill", "start", "pause", "unpause"]

        if not action in possibleActions:
            return {"status":"error","message": "Available Actions are : kill, start, pause, unpause"}

        try:
            container = client.containers.get(dockerID)
        except:
            return {"status":"error","message": "unable to get the docker instance. is the dockerId correct?"}


        if action == "kill":
            try:
                container.kill()
                container.reload()
                return {"status":"success","message": "kill the docker instance", "container":container.status}
            except:
                container.reload()
                return {"status":"error","message": "unable to kill the docker instance", "container":container.status}

        elif action == "start":
            try:
                container.start()
                container.reload()
                return {"status":"success","message": "started the docker instance", "container":container.status}
            except:
                container.reload()
                return {"status":"error","message": "unable to start the docker instance. is it paused?", "container":container.status}

        elif action == "pause":
            try:
                container.pause()
                container.reload()
                return {"status":"success","message": "paused the docker instance", "container":container.status}
            except:
                container.reload()
                return {"status":"error","message": "unable to pause the docker instance. is it dead?", "container":container.status}

        elif action == "unpause":
            try:
                container.pause()
                container.reload()
                return {"status":"success","message": "unpaused the docker instance", "container":container.status}
            except:
                container.reload()
                return {"status":"error","message": "unable to unpause the docker instance. is it dead?", "container":container.status}

        
    else:
        return {"status":"error","message":"not in JSON Format"}



# Input: dockerID
@app.route("/docker/status",methods=["POST"])
def stat_docker():
    if(request.is_json):
        try:
            content = request.get_json()
            dockerID = content['dockerID']
            action = content['action'].lower()

        except:
            return {"status":"error","message":"make sure you include the following items as proper JSON: dockerID"}

        try:
            container = client.containers.get(dockerID)
        except:
            return {"status":"error","message": "unable to get the docker instance. is the dockerId correct?"}


       
        try:
            return {"status":"success", "container":container.status}
        except:
            return {"status":"error","message": "unable to retrieve status"}


        
    else:
        return {"status":"error","message":"not in JSON Format"}



if __name__ == "__main__":

    app.run(port=80)