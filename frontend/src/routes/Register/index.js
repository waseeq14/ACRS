import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router'
import api from '../../utils/api'

import styles from './styles.module.css'

export default function Register() {
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await api.get('/is-authenticated', {
          withCredentials: true,
        });

        if (response.data.is_authenticated) {
          navigate('/dashboard')          
        } else {
          setLoading(false)
        }
      } catch (error) {
        console.error('Error checking authentication', error);
        setLoading(false)
        setError(true)
        // TODO: Showing some sort of error. (Flash message of some sort)
      }
    };

    checkAuthentication();
  }, [navigate])

  const handleRegisterSubmit = async e => {
    e.preventDefault()

    try {
      const response = await api.post('/register/', { username, email, password }, {
        headers: { 'Content-Type': 'application/json' }, withCredentials: true
      })

      if (response.status === 200) {
        alert(response.data.message)
        navigate('/login')
      }
    } catch (error) {
      if (error.response) {
        alert(error.response.data.error)
      } else {
        alert('An error occurred!')
      }
    }
  }

  if (loading || error) {
    return <></>
  } else {
    return (
      <div className={styles.container}>
        <div>
          <img
            className={styles.logo}
            src='/static/images/logo.png'
            alt='ACRS Logo'
          />
          <h1 className={styles.headingText}>ACRS</h1>
          <p className={styles.subText}>Automated Cyber Reasoning System</p>
        </div>
        <div>
          <div className={styles.modal}>
            <h2>SIGN UP</h2>
            <form className={styles.form} onSubmit={e => handleRegisterSubmit(e)}>
              <input
                type='text'
                placeholder='Username'
                value={username}
                onChange={e => setUsername(e.target.value)}
              />
              <br />
              <input
                type='email'
                placeholder='Email'
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
              <br />
              <input
                type='password'
                placeholder='Password'
                value={password}
                onChange={e => setPassword(e.target.value)}
              />
              <br />
              <input
                type='password'
                placeholder='Confirm Password'
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
              />
              <br />
              <button type='submit'>Register</button>
            </form>
          </div>
        </div>
      </div>
    )
  }
}
