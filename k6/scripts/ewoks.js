import http from 'k6/http';
import { check, sleep } from "k6";

export let options = {
  stages: [
      { duration: "1m", target: 5, vue:5 }
  ]
};
let binFile = open('./rauw.mp3', 'b');
export default function () {
  var data = {
    'file': http.file(binFile, 'test.mp3'),
    'newFormat': 'wma',
  };
  let params =  { headers: { "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNzM2NTAzNywianRpIjoiNmM5Njg5YTYtZTg0OC00ZjE4LThlODItYzk2OWVhOGM0YzgzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjM3MzY1MDM3LCJleHAiOjE2MzczNjU5Mzd9.ghoq6L8V2VK4THLsjlUJegPgdgVy4sD5LDlV7y6i8xo" } }
  var response = http.post('http://ec2-52-3-227-19.compute-1.amazonaws.com/api/tasks', data,params);

  check(response, { "status is 200": (r) => r.status === 200 });
  console.log(response.status);
  sleep(.300);
};


//console.log(binFile);
  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  //check(response, { "status is 200": (r) => r.status === 200 });
  


  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  


