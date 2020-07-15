import React , {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';

function loadBarks(callback) {
  const xhr = new XMLHttpRequest()
  const method = 'GET'
  const url = "http://127.0.0.1:8000/api/barks"
  const responseType = "json"
  xhr.responseType = responseType
  xhr.open(method, url)
  xhr.onload = function() {
      callback(xhr.response, xhr.status)
  }
  xhr.onerror = function (e) {
    console.log(e)
    callback({"message": "Request was an error"}, 400)
  }
  xhr.send()
}

function App() {
  const [barks, setBarks] = useState([])

  useEffect(() => {
    const myCallback =  (response, status) => {
      console.log(response, status)
      if(status === 200) {
        setBarks(response)
      } else {
        alert("There was an error")
      }
    }
    loadBarks(myCallback)
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          {barks.map((bark, index)=>{
            return <li>{bark.content}</li>
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
