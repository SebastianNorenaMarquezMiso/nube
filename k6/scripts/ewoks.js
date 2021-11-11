import http from 'k6/http';
import { check, sleep } from "k6";

export let options = {
  stages: [
      { duration: "1m", target: 2 , vue:30 }
  ]
};
let binFile = open('./rauw.mp3', 'b');
export default function () {
  var data = {
    'file': http.file(binFile, 'test.mp3'),
    'newFormat': 'wma',
  };
  let params =  { headers: { "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNjMwNjczNCwianRpIjoiMmQzM2NkZGQtYjE0ZS00OGNhLWI4ZjYtNzQ3YmYzMzNjNTRjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjM2MzA2NzM0LCJleHAiOjE2MzYzMDc2MzR9.gpr8AHee3ncrs5-Lvas-rjGqJhEuH16bnoaZtVNk7gY" } }
  var response = http.post('http://ec2-18-207-99-175.compute-1.amazonaws.com/api/tasks', data,params);

  check(response, { "status is 200": (r) => r.status === 200 });
  console.log(response.status);
  sleep(.300);
};


//console.log(binFile);
  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  //check(response, { "status is 200": (r) => r.status === 200 });
  


  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  


