import { useContext } from 'react'
import { AppContext } from '../../context/AppContext'

import styles from './styles.module.css'

export default function RunKLEE() {
  const { appState } = useContext(AppContext)

  return (
    <>
      <div className={styles.card}>
        <h2>AFL Friendly Code: </h2>
        <textarea
          readOnly={true}
          value={appState.fuzzerResult ? appState.fuzzerResult.code : ''}
        ></textarea>
      </div>
      <div style={{ height: '1rem' }}></div>
      <div className={styles.card}>
        <h2>Seeds: </h2>
        <textarea
          readOnly={true}
          value={appState.fuzzerResult ? appState.fuzzerResult.seeds : ''}
        ></textarea>
      </div>
      <div style={{ height: '1rem' }}></div>
      <div className={styles.card}>
        <h2>Analysis: </h2>
        <textarea
          readOnly={true}
          value={appState.fuzzerResult ? appState.fuzzerResult.analysis : ''}
        ></textarea>
      </div>
    </>
  )
}
