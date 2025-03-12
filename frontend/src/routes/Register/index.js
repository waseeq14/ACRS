import { useState } from 'react'
import { Link, useNavigate } from 'react-router'
import styles from './styles.module.css'

export default function Register() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const handleRegisterSubmit = async (e) => {
    
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:8000/register/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });
  
    const data = await response.json();
    if (response.ok) {
      alert("Registration Successful");
      navigate("/login")
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
