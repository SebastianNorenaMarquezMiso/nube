import http from 'k6/http';
import { check, sleep } from "k6";

export let options = {
  stages: [
      { duration: "1m", target: 5, vue:100 }
  ]
};
let binFile = open('./rauw.mp3', 'b');
export default function () {
  var data = {
    'file': http.file(binFile, 'test.mp3'),
    'newFormat': 'wma',
  };
  let params =  { headers: { "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNzMwODMxOCwianRpIjoiOGVkNjIyNWItMTY2NC00MDRmLThjNjgtOGEyYzI4ZmYxMGMyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjM3MzA4MzE4LCJleHAiOjE2MzczMDkyMTh9.JEIKymrMsTSJnGHDdXCYnZA_Yxcqvao1EDSwa6rKDc8" } }
  var response = http.post('http://ec2-3-239-16-234.compute-1.amazonaws.com/api/tasks', data,params);

  check(response, { "status is 200": (r) => r.status === 200 });
  console.log(response.status);
  sleep(.300);
};


//console.log(binFile);
  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  //check(response, { "status is 200": (r) => r.status === 200 });
  


  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  


