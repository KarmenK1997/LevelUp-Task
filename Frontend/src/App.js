import './App.css'
import { useEffect, useState } from 'react'

const apiUrl = "http://127.0.0.1:5000"

function ValidationInfo({ validity, field }) {
  if (validity == false) return <p className='invalid-label'>Invalid {field}</p>
  return null
}

function CreditCard({ pan, cvv, date, vendor }) {
  const sanitizedPan = pan?.replaceAll(' ', '')
  let panSeparated = ''

  for (let i = 0; i < sanitizedPan.length; i++) {
    if (i > 0 && i % 4 == 0) {
      panSeparated += ' '
    }
    panSeparated += sanitizedPan[i]
  }

  return (
    <div className={'creditCard ' + vendor}>
      <p className='CCPan'>{panSeparated}</p>
      <p className='CCCvv'>{cvv}</p>
      <p className='CCDate'>{date}</p>
      <p className='CCVendor'>{vendor}</p>
    </div>
  )
}

function App() {
  const [validation, setValidation] = useState(null)
  const [cvv, setCvv] = useState('')
  const [pan, setPan] = useState('')
  const [date, setDate] = useState('')

  async function validate() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, cvv, pan })
    }

    try {
      const response = await fetch(
        `${apiUrl}/validate`,
        requestOptions
      )

      const data = await response.json()
      setValidation(data)
      console.log(data)
    } catch (e) {
      alert('Something went wrong!')
    }
  }

  async function submit(event) {
    event.preventDefault()
    validate()
  }

  useEffect(() => {
    validate()
  }, [pan, cvv, date])

  return (
    <div>
      <div className='main'>
        <div className='window'>
          <CreditCard
            pan={pan}
            cvv={cvv}
            date={date}
            vendor={validation?.vendor}
          ></CreditCard>
          <form onSubmit={submit}>
            <div className='input-container'>
              <label htmlFor='pan'>Pan</label>
              <input
                onChange={e => setPan(e.target.value)}
                value={pan}
                type='text'
                id='pan'
                name='pan'
                inputMode='numeric'
                autoComplete='cc-number'
                maxLength='19'
                placeholder='xxxx xxxx xxxx xxxx'
                style={{
                  borderColor:
                    validation?.pan_valid === false ? 'red' : '#909090'
                }}
              />
              <ValidationInfo validity={validation?.pan_valid} field='pan' />
            </div>
            <div className='input-container'>
              <label htmlFor='cvv'>CVV</label>
              <input
                onChange={e => setCvv(e.target.value)}
                value={cvv}
                type='text'
                id='cvv'
                name='cvv'
                style={{
                  borderColor:
                    validation?.cvv_valid === false ? 'red' : '#909090'
                }}
              />
              <ValidationInfo validity={validation?.cvv_valid} field='cvv' />
            </div>
            <div className='input-container'>
              <label htmlFor=''>Exp</label>
              <input
                onChange={e => setDate(e.target.value)}
                value={date}
                type='month'
                id='date'
                name='date'
                style={{
                  borderColor:
                    validation?.date_valid === false ? 'red' : '#909090'
                }}
              />
              <ValidationInfo
                validity={validation?.date_valid}
                field='date of expiry'
              />
            </div>
            <input className='submit' type='submit' value='Submit'></input>
          </form>
        </div>
      </div>
    </div>
  )
}

export default App
