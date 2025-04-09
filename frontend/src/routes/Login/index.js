import { useState, useEffect, useContext } from 'react'
import { Link, useNavigate } from 'react-router'
import { AppContext } from '../../context/AppContext'
import api from '../../utils/api'

import styles from './styles.module.css'

export default function Login() {
  console.log("Abdullah khasi")
  const navigate = useNavigate()

  const { appState, setAppState } = useContext(AppContext)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await api.get('/is-authenticated', {
          withCredentials: true,
        });

        if (response.data.is_authenticated) {
          setAppState({ ...appState, user: response.data.user })
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

  const handleLoginSubmit = async e => {
    e.preventDefault()
    
    try {
      const response = await api.post('/login/', { username, password }, {
        headers: { 'Content-Type': 'application/json' }, withCredentials: true
      })
  
      if (response.status === 200) {
        setAppState({ ...appState, user: response.data.user })
        alert(response.data.message)
        navigate('/dashboard')
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
            <h2>LOGIN</h2>
            <form className={styles.form} onSubmit={e => handleLoginSubmit(e)}>
              <input
                type='text'
                placeholder='Username'
                value={username}
                onChange={e => setUsername(e.target.value)}
              />
              <br />
              <input
                type='password'
                placeholder='Password'
                value={password}
                onChange={e => setPassword(e.target.value)}
              />
              <br />
              <button type='submit'>Login</button>
  
              <div className={styles.createAccountView}>
                <Link to='/create-account'>Create Account</Link>
                <Link>Forgot Password</Link>
              </div>
            </form>
          </div>
        </div>
      </div>
    )
  }
}
