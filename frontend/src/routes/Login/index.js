import { useState } from 'react'
import { Link, useNavigate } from 'react-router'

import styles from './styles.module.css'

export default function Login() {
  const navigate = useNavigate()

  const [username, setUsername] = useState()
  const [password, setPassword] = useState()

  const handleLoginSubmit = e => {
    e.preventDefault()

    navigate('/dashboard')
  }

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
