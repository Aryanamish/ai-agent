# Installation Instruction
this is a django + react project 

it is hosted on [shopwise.aryanamish.in](https://shopwise.aryanamish.in/)

to setup the project you will need uv and node version 24 or above


```
cp .env.example .env
```

open the .env file and fill all the environment variable
now you can run `docker compose up -d` to start the server
if you want to run the server locally you will need to copy the .env file to backend/.env (or create a symbolic link)

## Run command
```shell
cd backend
uv sync
uv run manage.py runserver
```
```shell
cd frontend
pnpm i
pnpm dev
```


since the project requires a DB with populated data you can download the db.sqlite from [google drive](https://drive.google.com/drive/folders/1ieCG4TlLn5PJqocYd4rG7tiUlmFNNXjB?usp=sharing)

there are two users you can use to login:


  - username: `admin`, password: `admin`

  - username: `user`, password: `user`

or you will need to run migration manually 

```shell
cd backend
uv run manage.py migrate_all # this will migrate all organization data also
```

# Backend Architecture
To isolate the DB for every organization. i create Db route in django to physically isolate the Database, this will create a separate db.sqlite for every organization (it will work same with mysql also)

when a request comes `OrganizationMiddleware` is called which based on the slug decides which DB will be used to make the query after it identifies the db name it removes the org slug from the url so that the rest of the application does not know about the different DB structure and the url structure because of it.


```
Request -> middleware (stores the DB name then modifies the url) -> App (not aware of the DB isolation)
```

# Agent Architecture
I have only added two intent to the Agent "product search" and "general query". it uses cosine_similarity to recommend, for simplicity i am storing the embeddings in the sqlite DB itself as a result vector search is done outside of the DB in the python application inside `search_products` will not work for large dataset.


[architecture of the Agent](https://excalidraw.com/#json=jeKEdt6_cl_Hkrr2ONQT_,LYLmQUO6UzOxoRAqAIA88g)

