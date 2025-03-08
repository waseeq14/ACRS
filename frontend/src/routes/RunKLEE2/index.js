import { useContext, useState } from 'react'
import { AppContext } from '../../context/AppContext'

import styles from './styles.module.css'

export default function RunKLEE2() {
  const { appState } = useContext(AppContext)

  const [selectedIndex, setSelectedIndex] = useState(0)

  return (
    <>
      <div className={styles.card}>
        <h2>Sus Segments: </h2>
        <textarea
          readOnly={true}
          value={
            appState.advancedKleeResult
              ? appState.advancedKleeResult.segments[selectedIndex]
              : ''
          }
        ></textarea>
      </div>
      <div style={{ height: '1rem' }}></div>
      {appState.advancedKleeResult ? (
        <div style={{ textAlign: 'left' }}>
          <pre style={{ display: 'inline', color: 'white' }}>Segment: |</pre>
          {appState.advancedKleeResult.segments.map((_, index) => (
            <>
              <pre
                style={{ display: 'inline', color: 'white', cursor: 'pointer' }}
                onClick={e => setSelectedIndex(index)}
              >
                {' '}
                {index + 1}
              </pre>
              <pre style={{ display: 'inline', color: 'white' }}> |</pre>
            </>
          ))}
        </div>
      ) : null}
      <div style={{ height: '1rem' }}></div>
      <div className={styles.card}>
        <h2>Analysis: </h2>
        <textarea
          readOnly={true}
          value={
            appState.advancedKleeResult
              ? appState.advancedKleeResult.analysis
              : ''
          }
        ></textarea>
      </div>
    </>
  )
}
