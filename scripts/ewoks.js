import http from 'k6/http';
import { check, sleep } from "k6";

export let options = {
  stages: [
    // Ramp-up from 1 to 5 virtual users (VUs) in 5s
    { duration: "5s", target: 5 },

    /* // Stay at rest on 5 VUs for 10s
     { duration: "10s", target: 5 },

     // Ramp-down from 5 to 0 VUs for 5s
     { duration: "5s", target: 0 }*/
  ]
};
let binFile = open('./rauw.mp3', 'b');

let token = '';
let apiUrl = 'http://172.19.0.4:5000';

export function setup() {
  let data = {
    "username": "Pepito",
    "password": "1234"
  };
  let params = {
    headers: {
      "Content-Type": "application/json;",
    }
  }
  let response = http.post(apiUrl + '/api/auth/login', JSON.stringify(data), params);

  let checkRes = check(response, {
    "Token Request status is 200": (r) => r.status === 200,
  });

  if (checkRes) {
    let responseJson = response.json();
    token = responseJson.token;
  }
}

export default function () {
  let data = {
    'file': http.file(binFile, 'test.mp3'),
    'newFormat': 'wma',
  };
  let params = {
    headers: {
      "Authorization": "Bearer " + token,
      "Content-Type": "multipart/form-data;",
    }
  }
  let response = http.post(apiUrl + '/api/tasks', data, params);

  check(response, {"status is 200": (r) => r.status === 200});

  sleep(.300);
};