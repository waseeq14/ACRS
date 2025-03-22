import { useContext } from 'react'
import { AppContext } from '../../context/AppContext'

import styles from './styles.module.css'

export default function Profile() {
  const { appState: { user } } = useContext(AppContext)

  return (
    <>
      <div className={styles.card}>
        <h2>Account Information</h2>
        <div>
          <input name='username' placeholder='Username' value={user.username} contentEditable={false} />
          <input name='email' placeholder='Email' value={user.email} contentEditable={false} />
          <input name='password' placeholder='New Password' />
          <button>Change Password</button>
        </div>
      </div>
    </>
  )
}