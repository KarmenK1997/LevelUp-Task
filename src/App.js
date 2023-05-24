import './App.css';
import { useEffect, useState } from 'react';

function ValidationInfo({ validity, field }) {
  if (validity == false)
    return <p className='invalid-label'>Invalid {field}</p>
  return null
}

function App() {
  // useEffect(() => {
  //   const requestOptions = {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify({ d: "2030 3 3", cvv: "563", pan: "1234567890123452" })
  //   };

  //   fetch("http://127.0.0.1:5000/validate", requestOptions)
  //     .then(response => response.json())
  //     .then(data => console.log(data));

  // }, []);

  return (
    <div>
      <form action="http://127.0.0.1:5000/validate" method="post" target='blank_'>
        <label for="cvv">cvv:</label>
        <input type="text" id="cvv" name="cvv"></input>
        <label for="pan">pan:</label>
        <input type="text" id="pan" name="pan"></input>
        <input type="date" id="date" name="date"></input>
        <input type="submit" value="Submit"></input>
      </form>

    </div>
  );
}


export default App;
