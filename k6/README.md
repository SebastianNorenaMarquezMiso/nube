## Proyecto Convertidor Audio

### Equipo 5
>  Javier Vargas
>  Jimmy Cardenas
>  Sebastián Noreña
>  Zully Alarcón

-------



### *Para desplegar el proyecto* 

>  docker-compose build 
>  docker-compose up 

### *solo para desplegar las pruebas*
>  docker-compose up -d influxdb grafana
>  docker-compose run k6 run /scripts/ewoks.js

##*con proxy*
>  docker-compose run k6 run --env HTTP_PROXY=http://connect2.virtual.uniandes.edu.co:443 /scripts/ewoks.js

### *despues de ejecutar las pruebas para ver el grafana*
> http://localhost:3000/d/k6/k6-load-testing-results?orgId=1&refresh=5s

### *para eliminar todas las imagenes*
>  docker rmi -f $(docker images -a -q)
>  docker rm -f $(docker ps -a -q)

