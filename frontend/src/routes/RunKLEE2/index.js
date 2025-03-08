import { useContext, useState, Fragment } from 'react'
import { AppContext } from '../../context/AppContext'
import Markdown from 'react-markdown'

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
            <Fragment key={index}>
              <pre
                style={{ display: 'inline', color: 'white', cursor: 'pointer' }}
                onClick={e => setSelectedIndex(index)}
              >
                {' '}
                {index + 1}
              </pre>
              <pre style={{ display: 'inline', color: 'white' }}> |</pre>
            </Fragment>
          ))}
        </div>
      ) : null}
      <div style={{ height: '1rem' }}></div>
      <div className={styles.card}>
        <h2>Analysis: </h2>
        <Markdown>{appState.advancedKleeResult.analysis}</Markdown>
      </div>
    </>
  )
}
