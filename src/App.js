import './App.css';
import { useEffect, useState } from 'react';

function ValidationInfo({ validity, field }) {
  if (validity == false)
    return <p className='invalid-label'>Invalid {field}</p>
  return null
}

function App() {
  const [validation, setValidation] = useState(null);
  const [cvv, setCvv] = useState("");
  const [pan, setPan] = useState("");
  const [date, setDate] = useState("");

  async function submit(event) {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, cvv, pan })
    };

    try {
      fetch("http://127.0.0.1:5000/validate", requestOptions);
      const response = await fetch("http://127.0.0.1:5000/validate", requestOptions);

      const data = await response.json()
      setValidation(data)
      console.log(data)
    }
    catch (e) {
      alert("Something went wrong!")
    }

    event.preventDefault()

  //   fetch("http://127.0.0.1:5000/validate", requestOptions)
  //     .then(response => response.json())
  //     .then(data => console.log(data));
  }


  return (
    <div>
      <div className='main'>
        <div className='window'>
          <form onSubmit={submit}>
            <div className='input-container'>
              <label htmlFor="pan">Pan</label>
              <input
                onChange={e => setPan(e.target.value)}
                value={pan}
                type="text"
                id="pan"
                name="pan"
              />
              <ValidationInfo validity={validation?.pan_valid} field="pan" />
            </div>
            <div className='input-container'>
              <label htmlFor="cvv">CVV</label>
              <input
                onChange={e => setCvv(e.target.value)}
                value={cvv}
                type="text"
                id="cvv"
                name="cvv"
              />
              <ValidationInfo validity={validation?.cvv_valid} field="cvv" />
            </div>
            <div className='input-container'><label htmlFor="">Exp</label>
              <input
                onChange={e => setDate(e.target.value)}
                value={date}
                type="month"
                id="date"
                name="date"
              <ValidationInfo validity={validation?.date_valid} field="date of expiry" /></div>
            <input className="submit" type="submit" value="Submit"></input>
          </form>
        </div>

      </div>
    </div>
  );
}


export default App;
