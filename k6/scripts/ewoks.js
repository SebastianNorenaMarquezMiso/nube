import http from 'k6/http';
import { check, sleep } from "k6";

export let options = {
  stages: [
      { duration: "1m", target: 1 , vue:1 }
  ]
};
let binFile = open('./rauw.mp3', 'b');
export default function () {
  var data = {
    'file': http.file(binFile, 'test.mp3'),
    'newFormat': 'wma',
  };
  let params =  { headers: { "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNjMwNjAzMywianRpIjoiNzgwODFiMmUtMzc0Yy00NGIzLWE2N2UtMTQzMTQxMWEzMGI0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjM2MzA2MDMzLCJleHAiOjE2MzYzMDY5MzN9.cQQVxTbK5-1GK-C26lBE2SAExeAJuZXbzlVodsZ-sEc" } }
  var response = http.get('http://ec2-18-207-99-175.compute-1.amazonaws.com/api/tasks', data,params);

  check(response, { "status is 200": (r) => r.status === 200 });
  console.log(response.status);
  sleep(.300);
};


//console.log(binFile);
  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  //check(response, { "status is 200": (r) => r.status === 200 });
  


  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  


