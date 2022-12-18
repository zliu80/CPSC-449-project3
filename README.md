# CPSC-449-project4

    Add your name here

    Team Members:

    Alejandro Ramos Jr
    
    Kirti Chaudhary
    
    Anusha Hadagali
    
 Copy from project3: see details at: https://github.com/zliu80/CPSC-449-project3
    
    
Copy from project2: see details at: https://github.com/zliu80/CPSC449project2.git

# Instructions

    1. After clone the project, create folders like this. Empty folder can't be pushed to github so that's why you need to create these empty folder manually.
    
<img width="182" alt="image" src="https://user-images.githubusercontent.com/98377452/204716534-afd44446-21c0-4fc7-913d-897a1c7ca332.png">

    2. foreman start
    
    3. Don't do this step before "foreman start"
    
       cd CPSC449-project3/
    
       ./bin/init.sh

       If the permission is denied. try:

       sh ./bin/init.sh
       
    4. Updating nginx (see the file "tutorial-user-authentification" at the root folder)
    
        upstream backend {
                server localhost:5100;
                server localhost:5200;
                server localhost:5300;
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
                
                location ~ ^/(rank)$ {
                        proxy_pass http://localhost:5400;
                        proxy_set_header X-Original-URI $request_uri;
                        proxy_set_header X-Original-Remote-Addr $remote_addr;
                        proxy_set_header X-Original-Host $host;
                }
        }

As you can see, 1 user service, 3 game service, and 1 leaderboard service.

<img width="616" alt="image" src="https://user-images.githubusercontent.com/98377452/205391291-fd25919d-c2b1-4376-b265-f515dc621d47.png">

# Cron RQ Updates
Download Cron on terminal

Terminal:

mkdir ~/scripts

cd ~/.scripts

touch updates.sh

chmod u+x ./updates.sh

crontab -e

# In the cron tab insert:

*/10 * * * * rq requeue --all --queue default

<img width="572" alt="Screenshot 2022-12-17 at 5 30 22 PM" src="https://user-images.githubusercontent.com/92772530/208272706-f4037a43-a569-43d7-8de2-1db903ebcc53.png">


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

    http://tuffix-vm/startgame

2. Guess a word

    http://tuffix-vm/guess?game_id=1&word=guess

3. List all game of the current user

    http://tuffix-vm/allgame

4. Retrieve a game with the game_id

    http://tuffix-vm/retrievegame?game_id=1
   
# Leaderboard API

1. Post all scores (win or lose)

    Note: Reporting results is accessible only to internal services, you won't be able to access through API gateway.

    http://127.0.0.1:5400/post

2. Top 10 scores

    Accessing this api do not require authentification.

    http://tuffix-vm/rank

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

# Webhook Configuration

* Downloaded and installed ngrok to expose a port in the local development environment to the Internet.
* Added a Webhook to the Games service, allowing clients to receive updates when a user wins or loses a game.
* clients will need to register with the Games service, providing a callback URL where win/loss information should be sent.
* Add a new endpoint to the Games service allowing clients to register URLs to receive scores. 
