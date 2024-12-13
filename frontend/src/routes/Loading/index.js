import { useEffect, useState } from 'react'
import styles from './styles.module.css'
import { useNavigate } from 'react-router'

export default function Loading() {
  const navigate = useNavigate()

  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      const value = Math.floor(Math.random() * 100) % 45

      setProgress(progress => {
        if (progress + value >= 100) {
          return 100
        } else {
          return progress + value
        }
      })
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (progress === 100) {
      navigate('/login')
    }
  }, [progress, navigate])

  return (
    <div className={styles.container}>
      <img
        className={styles.logo}
        src='/static/images/logo.png'
        alt='ACRS Logo'
      />

      <div className={styles.loadingBar}>
        <div style={{ width: (progress * 800) / 100 + 'px' }}></div>
      </div>

      <p className={styles.text}>Connecting to the DOOM Server...</p>
    </div>
  )
}
