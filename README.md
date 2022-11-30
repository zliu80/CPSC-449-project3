# CPSC-449-project2

    Add your name here

    Team Members:

    Zhiqiang Liu 
    Sam Le
    Kirti Chaudjary
    Shridhar Bhardwaj


# Initialize the database

cd CPSC449project2/

Under the project directory, type:

./bin/init.sh

If the permission is denied. try:

sh ./bin/init.sh

# Split into two services.

user.py is for User Service, database userdb file in var/primary/mount/

game.py is for Game Service, database gamedb file in var/primary/mount/

# Instructions

Before you start, you should note that our Auth service is running on localhost:5000, Game service is running on localhost:5100. After setup, the Nginx server will not let you to visit the Game service unless you pass the Auth.

1. Set up the nginx server

        cd /etc/nginx/sites-enabled
    
        sudo vim tutorial

2. Updating the tutorial file, see tutorial-user-authentification, this file is under the root.

Notice here the PORT number for service are hardcoded in nginx config
```
user service: 5000
game service: 5100, 5101, 5103, the port number incrementation is 1 each time which is the way foreman works

upstream backend {
        server localhost:5100; // We only do 3 here
        server localhost:5101;
        server localhost:5102;
}
```

*** Copy pasting this for nginx could potentially cause strange issue where nginx will not working properly such as throwing 500 server error even when nginx starts up ok. Restarting might not help. 

What we recommend you do is go back to the default nginx, restart to make sure it works. Then copy paste block by block starting at the most basic nginx config, restart and make sure it works. Then restart nginx and copy another block and so on. Sometimes, when copying over material the result may contain strange invisible white spaces character that you may not notice which might result in those issues.

```       
        upstream backend {
                server localhost:5100;
                server localhost:5101;
                server localhost:5102;
        }
        server{
                listen 80;
                listen [::]:80;
                server_name tuffix-vm;

                location / {
                        auth_request /auth;
                        auth_request_set $auth_cookie $upstream_http_set_cookie;
                        auth_request_set $auth_status $upstream_status;
                        proxy_pass http://backend;
                }

                location = /auth {
                        internal;
                        proxy_pass http://localhost:5000;
                        proxy_pass_request_body off;
                        proxy_set_header Content-Length "";
                        proxy_set_header X-Original-URI $request_uri;
                        proxy_set_header X-Original-Remote-Addr $remote_addr;
                        proxy_set_header X-Original-Host $host;
                }

                location ~ ^/(register)$ {
                        proxy_pass http://localhost:5000;
                        proxy_set_header X-Original-URI $request_uri;
                        proxy_set_header X-Original-Remote-Addr $remote_addr;
                        proxy_set_header X-Original-Host $host;
                }
        }
```
3. After updating tutorial, restart nginx

        sudo service nginx restart
    
4. Start User (port: 5000) and Game (port: 5100, 5101, 5102) Service.

        foreman start --formation user=1,game=3 --port 5000 
    
visit http://tuffix-vm, you will see the authentification dialog if you have not logged in.

<img width="1223" alt="image" src="https://user-images.githubusercontent.com/98377452/200998703-dbe7bab7-2e57-4200-8a45-55154ff4e5c7.png">

# User API

There are only two API. 1). auth 2). register

In order to visit the game service, you must pass the authentification (all game API require auth).

However, you will be able to register without authentification.

GET: http://tuffix-vm/register?username=yourusername&password=yourpassword
POST using httpie: http --form POST http://tuffix-vm/register username="username1" password="password"

# Game API

See http://tuffix-vm/docs

Note: 

1. The User API won't be in this docs.

2. The username is not required to pass in to the game service. We can get the username after authentification.

API List (We are Project 2 Now):

1.  Start a new game
    
Project 2: 

    http://tuffix-vm/startgame

Project 1: 

    http://localhost:5000/startgame?username=jacob

2. Guess a word

Project 2: 

    http://tuffix-vm/guess?game_id=1&word=guess

Project 1: 

    http://localhost:5000/guess?username=jacob&game_id=1&word=mixed

3. List all game of the current user

Project 2: 

    http://tuffix-vm/allgame

Project 1: 

    http://localhost:5000/allgame?username=jacob

4. Retrieve a game with the game_id

Project 2: 

    http://tuffix-vm/retrievegame?game_id=1

Project 1: 

    http://localhost:5000/retrievegame?game_id=1


# Example show

Register:

<img width="515" alt="image" src="https://user-images.githubusercontent.com/98377452/201837505-6613fc2f-242e-41ea-b14c-7d86cbc09dfc.png">

startgame:

There will be auth if the users have not logged in. Use the above username and password to log in

<img width="977" alt="image" src="https://user-images.githubusercontent.com/98377452/201836582-c9b432cb-b29e-4df3-aece-3e538b174501.png">

If the user can't pass the auth

<img width="1014" alt="image" src="https://user-images.githubusercontent.com/98377452/201836736-a358ad0f-fdce-4640-8e35-eccf77aecf2c.png">

Success

<img width="506" alt="image" src="https://user-images.githubusercontent.com/98377452/201837826-b0cff198-221c-4a2a-a11b-b9079387c896.png">

Guess a word:

Use the game_id from the above image and guess a word whahever you want.

<img width="504" alt="image" src="https://user-images.githubusercontent.com/98377452/201838007-92e4620a-09bb-4e1f-bd97-3940cb26c24e.png">

Note: the returned json will tell you

wrong_spot means this character is in the correct word but not in the correct spot.

correct_spot means this character is in the correct word.

List all game:

<img width="362" alt="image" src="https://user-images.githubusercontent.com/98377452/201838100-78952511-5883-4fa2-b0b4-c13fc6168078.png">

Retrieve a game

Use the game_id from the above image

<img width="428" alt="image" src="https://user-images.githubusercontent.com/98377452/201838223-5f0ce995-068b-4d90-af78-efba4fc2f49b.png">

Load balancing: game service getting accessed in Round Robin fashion
![image](https://user-images.githubusercontent.com/67793141/202825231-2199edce-3ffb-4718-9d1a-5c39c38c696f.png)
