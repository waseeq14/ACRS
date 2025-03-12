import { useState } from 'react'
import { Link, useNavigate } from 'react-router'

import styles from './styles.module.css'

export default function Login() {
  const navigate = useNavigate()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:8000/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
  
    const data = await response.json();
    if (response.ok) {
      alert("Login Successful");
      navigate("/dashboard");
    } else {
      alert(data.error);
    }
  };
  

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
