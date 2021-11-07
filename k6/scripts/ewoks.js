import http from 'k6/http';
import { check, sleep } from "k6";

export let options = {
  stages: [
      // Ramp-up from 1 to 5 virtual users (VUs) in 5s
      { duration: "5s", target: 5 , vue:2 },

     /* // Stay at rest on 5 VUs for 10s
      { duration: "10s", target: 5 },

      // Ramp-down from 5 to 0 VUs for 5s
      { duration: "5s", target: 0 }*/
  ]
};
let binFile = open('./rauw.mp3', 'b');
export default function () {
  
  //console.log(binFile);
  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  //check(response, { "status is 200": (r) => r.status === 200 });
  


  //const response = http.get("https://swapi.dev/api/people/30/", {headers: {Accepts: "application/json"}});
  
  var data = {
    'file': http.file(binFile, 'test.mp3'),
    'newFormat': 'wma',
};
let params =  { headers: { "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTEwMzM5MCwianRpIjoiYzIxOGYwZDMtY2UzZC00NDFmLWI1M2EtODkwMzBlMTMzMzQ1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjM1MTAzMzkwLCJleHAiOjE2MzUxMDQyOTB9.kHZZBDYiwYN5tDkU6OB2sPFWDOMzJeUK1mqBLp9c_Jk" } }
var response = http.post('http://172.19.0.1:5000/api/tasks', data,params);

  check(response, { "status is 200": (r) => r.status === 200 });
  console.log(response.status);
  sleep(.300);
};



