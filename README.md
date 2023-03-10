# calorie-tracker-fast-api
Calorie tracker app with frontend in React and backend in fast-api

## To Setup the Calorie Tracker in gitpod.
You can add gitpod extension to your browser or directly create a workspace in gitpod by accessing
```
https://gitpod.io#github.com/rohitchauraisa1997/calorie-tracker
```    

## To Setup the Calorie Tracker in your local environment.

### Clone the repository to your local.
```
git clone https://github.com/rohitchauraisa1997/calorie-tracker-fast-api
```

### Move to the cloned directory.
```
cd calorie-tracker-fast-api
```

### Docker compose to bring the calorie tracker app up
```
docker compose up -d
```
### To access into different containers/services of docker compose 
```
 docker compose ps
```
### If all services are up and running well the app comes up at localhost:3000 so access
```
 http://localhost:3000
```
### to access into different containers/services of docker compose 

```
 docker compose exec mongodb mongosh calorie-tracker-db -u calorie-user -p calorie123
```

```
 docker compose exec backend sh
```

```
 docker compose exec frontend sh
```
