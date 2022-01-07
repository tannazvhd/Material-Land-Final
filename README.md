# Material Land
This project is designed to facilitate the study process for new students in University of Duisburg-Essen by sharing experience, advices, and helpful files among students.
> Project for the course: Advanced web technologies, International studies in engineering, Master of computer engineering, University of Duisburg-Essen

# A project logo/teaser image showcasing your project that is suitable for a medium-sized thumbnail image for the course web page
![logo/teaser](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/logo-teaser.jpeg)

# Features
## Users can do the following:
1. Register & login
2. Change username, password, and personal image
3. Add posts such as; inquiries and advices
4. Upload helpful files and materials (only pdf, zip, and images)
5. Interact on posts by adding comments, like, and dislike
6. User can update his/her own posts (title, category, contents, and attachment) or remove them. 

# Try on Heroku
[Material Land](https://flaskpro-advwebtech.herokuapp.com/)

# Live Demo
[Live demo and screenshots](https://www.youtube.com/watch?v=M09m9P4qvKg)

# Advertisement
[Advertisement Video](https://biteable.com/watch/educational-copy-2652764)

# Screenshots
>Logo

![logo](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/1.Logo.png)

>Landing page

![LandingPage](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/2.LandingPage.png)

>Footer

![Footer](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/3.Footer.png)

>Register page

![Register](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/4.Register.png)

>Login page

![Login](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/5.LoginPage.png)

>Profile page

![ProfilePage](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/6.UserPage.png)

>Updata personal data

![Updata personal data](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/7.Change-update%20userData.png)

>Add post

![AddPost](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/8.AddPost.png)

>Show post

![ShowPost](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/9.ShowPosts.png)

>Own posts

![OwnPosts](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/10.Review%20own%20posts.png)

> Modify posts

![ModifyPosts](https://github.com/AmrShakhshirUDE/testdeployUDE/blob/master/ProjectImages/11.Update-%20remove%20own%20posts.png)


# Technical architecture
The application consists of two main parts:
* Backend: responsible for server-side web application logic, consists of a server, an application, and a database.
* Frontend: the part that users interact with it.

# Technologies/ libraries used
## Backend technologies
* Flask
* MongoDB for database
## Frontend technologies
* React
* Bootstrap
## Connecting frontend to backend
* Axios
* Postman: to test connectivity especially for 'POST' method
## Deploy technologies
* Gunicorn as a web server gateway interface "WSGI"
* mLab as a cloud database service
* Github
* Heroku

# How to run the project
> Make sure that you have mongoDB installed on your PC and we highly recommend you to use visual studio code as a code editor

## To run locally
1. In the top level directory, go to `mongo.py` file

comment line.15

`app.config["MONGO_URI"] = os.environ.get("MONGODB_URI")`

then uncomment line.16

`app.config["MONGO_URI"] = "mongodb://localhost:27017/final"`

2. Open terminal and go to the path of *mongo.py* then type the following:
```
venv\scripts\activate
pip install -r requirements.txt
python mongo.py
```
The backend part should be running

3. Go to `client\src\contexts\urlContext.js`

comment line.3

`export const UrlContext = createContext("https://first-attempt-advwebtech-ude.herokuapp.com/");`

uncomment line.4

`export const UrlContext = createContext("http://localhost:3000/");`

4. Go to `client\package.json`

on line.41 make sure that proxy value is: `"http://127.0.0.1:5000/"`

5. Open a new terminal and go to the path of client folder

```
npm install
npm start
```

> If `npm start` doesn't work, do the following:
```
npm install rimraf -g
rimraf node_modules
npm start -- --reset-cache
```
then repeat step number 5

## To deploy
1. In the top level directory, go to `mongo.py` file

comment line.16

`app.config["MONGO_URI"] = "mongodb://localhost:27017/final"`

then uncomment line.15

`app.config["MONGO_URI"] = os.environ.get("MONGODB_URI")`

2. Go to `client\src\contexts\urlContext.js`

uncomment line.3

`export const UrlContext = createContext("https://first-attempt-advwebtech-ude.herokuapp.com/");`

comment line.4

`export const UrlContext = createContext("http://localhost:3000/");`


3. Seperate 'client' folder from main project folder to be deployed seperately as in the following guide


4. follow the guide [Deploy web app to Heroku](https://www.youtube.com/playlist?list=PLpSK06odCvYdSyGkWmc-AdqRc3zmiHPCc), mainly you need to do as follows:
* Deploy backend app to heroku after pushing it to github. Please follow the steps in the upmentioned guide
* Create an account on mLab, currently migrated to mongoDB Atlas, make sure to name database and collection as written in the code, and finally connect backend app to mLab as explained in the upmentioned guide
* Push client file to a new github repository and deploy it to heroku. Please follow the steps in the upmentioned guide and __note that here you don't need to change url in axios part as you did that on step number 2__

5. On file `package.json` make sure that proxy value is equal to the url of the deployed backend app on heroku

# Group members
> **Baohui Deng, Tannaz Vahidi, Amr Shakhshir**
