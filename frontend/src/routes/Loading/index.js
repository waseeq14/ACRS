import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'

import styles from './styles.module.css'

const displayTexts = [
  'Connecting to the DOOM server',
  'KLEEning your exploit history',
  'Teaching LLM 2+2',
  'Initializing pwn frameworks',
  'Initiating suffering',
  'Applying bandage to patch'
]

export default function Loading() {
  const navigate = useNavigate()

  const [progress, setProgress] = useState(0)
  const [displayText, setDisplayText] = useState()

  useEffect(() => {
    const interval = setInterval(() => {
      const value = Math.floor(Math.random() * 100) % 45

      const randomText =
        displayTexts[Math.floor(Math.random() * displayTexts.length)]

      setDisplayText(randomText)
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
        src='/static/images/logo_transparent.png'
        alt='ACRS Logo'
      />

      <div className={styles.loadingBar}>
        <div style={{ width: (progress * 800) / 100 + 'px' }}></div>
      </div>

      <p className={styles.text}>{displayText}</p>
    </div>
  )
}
