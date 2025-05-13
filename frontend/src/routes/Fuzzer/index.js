import { useContext, useState, Fragment } from 'react'
import { AppContext } from '../../context/AppContext'
import Markdown from 'react-markdown'
import classNames from 'classnames'

import styles from './styles.module.css'

export default function RunKLEE() {
  const { appState } = useContext(AppContext)
  const [selectedIndex, setSelectedIndex] = useState(0)
  console.log(appState)
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
      <div className={classNames(styles.card, styles.noHeight, styles.white)}>
        <h2>Analysis: </h2>
        <Markdown>{appState.fuzzerResult.analysis[selectedIndex]}</Markdown>
      </div>
      <div style={{ height: '1rem' }}></div>
      {appState.fuzzerResult ? (
        <div style={{ textAlign: 'right' }}>
          {selectedIndex > 0 && (
            <pre
              style={{ display: 'inline', color: 'white', cursor: 'pointer' }}
              onClick={e => setSelectedIndex(index => index - 1)}
            >
              &lt;&lt;Prev
            </pre>
          )}
          <pre style={{ display: 'inline', color: 'white' }}> |</pre>
          {appState.fuzzerResult.analysis.map((_, index) => (
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
          {selectedIndex + 1 < appState.fuzzerResult.analysis.length && (
            <pre
              style={{ display: 'inline', color: 'white', cursor: 'pointer' }}
              onClick={e => setSelectedIndex(index => index + 1)}
            >
              {' '}
              Next&gt;&gt;
            </pre>
          )}
        </div>
      ) : null}

    </>
  )
}
