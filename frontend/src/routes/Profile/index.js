import { useContext, useState } from 'react'
import { AppContext } from '../../context/AppContext'
import api from '../../utils/api'

import styles from './styles.module.css'

export default function Profile() {
  const { appState, setAppState } = useContext(AppContext)

  
  const [password, setPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')

  const handleChangePassword = async () => {
    try {
      const response = await api.post('/update-password/', { password, new_password: newPassword }, {
        headers: { 'Content-Type': 'application/json' }, withCredentials: true,
      })

      if (response.data.success) {
        setAppState({ ...appState, user: response.data.user })
      }

      alert(response.data.message)
    } catch (error) {
      console.error('Error checking authentication', error)
      // TODO: Showing some sort of error. (Flash message of some sort)
    }
  };

  return (
    <>
      <div className={styles.card}>
        <h2>Account Information</h2>
        <div>
          <input name='username' placeholder='Username' value={appState.user.username} readOnly />
          <input name='email' placeholder='Email' value={appState.user.email} readOnly />
        </div>
      </div>
      <div style={{ height: '1rem' }}></div>
      <div className={styles.card}>
        <h2>Change Password</h2>
        <div>
          <input name='password' placeholder='Old Password' value={password} onChange={e => setPassword(e.target.value)} />
          <input name='new-password' placeholder='New Password' value={newPassword} onChange={e => setNewPassword(e.target.value)} />
          <button onClick={handleChangePassword}>Change</button>
        </div>
      </div>
    </>
  )
}