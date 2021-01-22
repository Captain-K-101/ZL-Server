# zumpla-lumpa-server


### Problem Statement:  
Easy way to deploy multiple user's code(webserver language) under the same domain but containerized to their own directory.  
  
  
### Existing Issues:
We need to create seperate users(diff for linux and windows) in the system for making sure that they upload files to their own system(if there is no login based gui). Even with this their web code is gonna run as www-data and a simple php exploit to escape out of their base directory would give them a control over other users. Hard to install customised language for user.  
  
  
### Existing Soln and their Drawback:
Complex UI.  
`ui is like a joke. if you need to explain it, its not good`  
  
  
### Idea(as of now):
Use a simple file upload system with a login system(already got one) and spin up dockers for each users(dockers are heavy and i was told something called nomad can limit memory of each user)  
  
    
### Tech Stack:
- Django
- Try gcloud storage api
- Cloud mongo
- Rest
- Dockers(use ubuntu vannila -> generate nomad script -> enjoy dynamic scaling)
