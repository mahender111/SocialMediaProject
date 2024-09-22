
# Social Media Project

A brief description of what this project does and who it's for


FriendRequest Model:

Stores friend requests sent between users.
Fields:
sender: The user who sends the friend request.
receiver: The user who receives the friend request.
timestamp: Automatically records when the request was created.
status: The current status of the friend request, with choices ('pending', 'accepted', 'rejected').
Constraints:
unique_together: Ensures that a user cannot send multiple friend requests to the same person.
Friendship Model:

Represents a friendship between two users.
Fields:
user1 and user2: The two users in the friendship.
created_at: Timestamp for when the friendship was created.
Constraints:
unique_together: Ensures that the same friendship is not duplicated.
Ordering:
Orders the friendships based on their creation date.
UserList & UserRetrieveUpdateDestroy:

Standard CRUD operations for the User model.
Permissions:
Both UserList and UserRetrieveUpdateDestroy use AllowAny, allowing unrestricted access for now.
UserListCreate enables listing all users or creating a new user.
UserRetrieveUpdateDestroy enables retrieving, updating, or deleting specific user records.
Authentication Views:

SignupView:
Handles user registration.
Creates a new user, generates an authentication token, and returns the user data along with the token.
LoginView:
Authenticates users based on their credentials and returns a token and user data.
LogoutView:
Deletes the user’s authentication token, effectively logging the user out.
Friend Request Handling:

SendFriendRequestView:
Allows authenticated users to send friend requests.
Includes validation checks to prevent sending requests to non-existent users or to oneself, and avoids duplicate friend requests.
The request status is set to 'pending' initially.
User Search with Pagination:

UserListSearchView:
Allows searching for users by username or email.
Pagination ensures that the search results are returned in pages, with each page containing up to 5 results.
search_fields: Limits search to usernames and email addresses, with case-sensitive search.
In summary:
The code provides a REST API to manage user registration, login, logout, and CRUD operations for users. It also supports sending friend requests, managing friendships, and searching for users with pagination. The use of DRF’s built-in generics makes it easier to handle standard operations, while custom views and validation help manage the application’s unique needs like sending friend requests.

Base Image: Uses the python:3.11 image.
Environment Variable: Sets PYTHONUNBUFFERED=1 to ensure that Python output is sent straight to the terminal.
Working Directory: Sets the working directory to /socialproject.
Requirements: Copies requirements.txt and installs the dependencies.
Code: Copies the project files to the container.
Expose Port: Exposes port 8000.
Command: Runs the Django development server on 0.0.0.0:8000.
## MAHENDER KAMBOJ

- mahendersingh059@gmail.com
- https://hub.docker.com/u/mahender048
- https://github.com/mahender111
- https://www.linkedin.com/in/mahendersingh059/
- 9812284896


## 🔗 Links
https://github.com/mahender111

# SOCIA

A brief description of what this project does and who it's for

# Social Networking API

This API allows users to sign up, log in, log out, search for users, send friend requests, and manage friend requests (accept/reject). Below are the API endpoints, their descriptions, request methods, and parameters.

## Authentication
Some endpoints require user authentication. Include the token in the headers as follows:





## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## Deployment

To deploy this project run

```bash
  npm run deploy
  
```
Create a image  project run

```bash
  Docker  Build -t SocialMediaProjectimage
```
Create container project run

```bash
  Docker run -d --name container_name container_image
```

run container project run

```bash
docker compose up

```
run container project run

```bash
docker compose up

```
  


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`

`venv`


## Documentation

[Documentation](https://linktodocumentation)
- http://127.0.0.1:8000/


## Installation

how to django project start

```bash
  Python django-admin startproject socialproject
  python -m venv venv 
  venv/Scripts/activate
  pip install django
  python manage.py startapp socialapp
  python manage.py createsuperuser
  python manage.py makemigration
  python manage.py migrate
  python manage.py  runserver
```
    
requiements file install 

```bash
  pip install -r requirements.txt
```

Docker file install

```bash
    docker build -t socialproject .
    docker images
    docker run --name container-1 socilimages
    docker ps 
    docker ps -a
```


all container delete command in Dockerfile

```bash
    docker container prune 
    docker rm container_id or name
    docker rmi image_id
```
docker create image + container + running
```bash
    docker compose up -d
    docker compose up 
```

how to docker file pull docker hub 
```bash
    docker images 
    docker tag imagesname + username/socialimages or foldername 
    docker login
    docker images 

    docker tag socialprojectimages + mahender048/socialimagesfolder
    docker pull mahender048/socialimagesfolder
```
## Roadmap

- Additional browser support

- Add more integrations

Base URL
/
View: index
Description: Welcome page.
User Management
/UserList/

View: UserList
Description: List all users and create new users. (GET, POST)
/UserListCreate/

View: UserListCreate
Description: Create new users. (POST)
/users/<int:pk>/

View: UserRetrieveUpdateDestroy
Description: Retrieve, update, or delete a user by ID. (GET, PUT, PATCH, DELETE)
/signup/

View: SignupView
Description: Register a new user. (POST)
/Login/

View: LoginView
Description: Authenticate a user and issue a token. (POST)
/Logout/

View: LogoutView
Description: Invalidate the user's token. (POST)
/UserListSearchView/

View: UserListSearchView
Description: Search for users by username or email. (GET)
Friend Request Management
/send/

View: SendFriendRequestView
Description: Send a friend request to another user. (POST)
/AcceptRejectFriendRequestView/<int:pk>/

View: AcceptRejectFriendRequestView
Description: Accept or reject a friend request. (PATCH, DELETE)
/AcceptList/

View: AcceptListFriendsView
Description: List accepted friends. (GET)
/PendingList/

View: PendingListFriendsView
Description: List pending friend requests. (GET)
/RejectedListFriendsView/

View: RejectedListFriendsView
Description: List rejected friend requests. (GET)
/accept/<int:pk>/

View: AcceptFriendupdateRequestView
Description: Accept a friend request and update its status. (PATCH)
## Usage/Examples

```javascript
import Component from 'my-project'

function App() {
  return <Component />
}
```


## Used By

This project is used by the following companies:

- Company 1
- Company 2


## Features

- User Management

- Signup: Register a new user.
- Login: Authenticate a user and issue a token.
- Logout: Invalidate the user's token.
- Friend Request Management

- Send Friend Request: Send a friend request to another user.
- Accept/Reject Friend Request: Accept or reject a    received friend request.
- List Friends: View accepted, pending, and rejected - - friend requests.
- User Search

- Search Users: Search for users by username or email.