import { useContext } from 'react'
import { AppContext } from '../../context/AppContext'
import Markdown from 'react-markdown'

import styles from './styles.module.css'

export default function RunKLEE() {
  const { appState } = useContext(AppContext)

  return (
    <>
    <div className={styles.card}>
      <h2>Analysis: </h2>
      <div className={styles.scrollableArea}>
        <Markdown>{appState.kleeResult.analysis}</Markdown>
      </div>
    </div>
      <div style={{ height: '1rem' }}></div>
      <div className={styles.card}>
        <h2>KLEE Friendly Code: </h2>
        <textarea
          readOnly={true}
          value={appState.kleeResult ? appState.kleeResult.code : ''}
        ></textarea>
      </div>
    </>
  )
}
