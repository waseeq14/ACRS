import { useContext, useState, useEffect } from 'react'
import { useNavigate, NavLink, Outlet } from 'react-router'
import { AppContext } from '../../context/AppContext'
import api from '../../utils/api'

import styles from './styles.module.css'
import { ModalProvider } from '../../utils/ModalManager'

export default function Dashboard({ navigationLinks }) {
  const navigate = useNavigate()

  const { appState, setAppState, showFuzzModal, setShowFuzzModal } = useContext(AppContext)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await api.get('/is-authenticated', {
          withCredentials: true,
        })

        if (response.data.is_authenticated) {
          setAppState({ ...appState, user: response.data.user })
          setLoading(false)
        } else {
          navigate('/login')
        }
      } catch (error) {
        console.error('Error checking authentication', error)
        setLoading(false)
        setError(true)
        // TODO: Showing some sort of error. (Flash message of some sort)
      }
    };

    checkAuthentication();
  }, [navigate])

  const handleLogout = async () => {
    try {
      const response = await api.get('/logout', {
        withCredentials: true,
      })

      if (response.status === 200) {
        navigate('/login')
      }
    } catch (error) {
      console.error('Error logging out', error)
    }
  }

  if (loading || error) {
    <></>
  } else {
    return (
      <>
        <div className={styles.appbar}>
          <div className={styles.appbarLeft}>
            <img
              className={styles.logo}
              src='/static/images/logo_mini.png'
              alt='Small Logo'
            />
            <h2 className={styles.title}>ACRS</h2>
          </div>
          <div className={styles.menu}>
            <p>{appState.user.username}</p>
            <img
              className={styles.userImg}
              src='/static/images/user.png'
              alt='User'
            />
            <ul className={styles.subMenu}>
              <li onClick={() => navigate('/dashboard/profile')}>Profile</li>
              <li onClick={handleLogout}>Logout</li>
            </ul>
            {/* <button type='button' onClick={handleLogout}>
              Logout
            </button> */}
          </div>
        </div>
  
        <div className={styles.sidebar}>
          <div className={styles.bar}></div>
          <ul>
            {navigationLinks.map(link => {
              if (link.condition && !link.condition(appState)) {
                return null
              } else {
                return (
                  <li>
                    <NavLink
                      className={({ isActive }) =>
                        isActive ? styles.active : ''
                      }
                      to={`/dashboard${link.path}`}
                      end
                    >
                      {link.name}
                    </NavLink>
                  </li>
                )
              }
            })}
          </ul>
        </div>
  
        <div className={styles.content}>
          <ModalProvider>
            <Outlet />
          </ModalProvider>
        </div>
      </>
    )
  }
}
