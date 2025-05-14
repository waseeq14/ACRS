import { useState, useEffect } from 'react'
import api from '../../utils/api'

import styles from './styles.module.css'

export default function Reports() {
  const [reports, setReports] = useState({})

  const fetchReports = async () => {
    try {
      const response = await api.get('/fetch-reports/')

      setReports({
        pentestReports: response.data.result.pentestReports,
        reports: response.data.result.reports
      });
    } catch (e) {
      console.error('An error occurred.')
    }
  }

  const loadReport = id => {
    window.open(
      `${process.env.REACT_APP_BACKEND_URL}/get-report?id=${id}`,
      '_blank',
      'noopener,noreferrer'
    )
  }

  const loadPentestReport = id => {
    window.open(
      `${process.env.REACT_APP_BACKEND_URL}/get-pentest-report?id=${id}`,
      '_blank',
      'noopener,noreferrer'
    )
  }

  const deleteReport = async id => {
    try {
      await api.delete('/delete-report/', {
        data: { id }
      })

      setReports(prevState => ({
        ...prevState,
        reports: prevState.reports.filter(report => report.id !== id)
      }));
    } catch (e) {
      console.error('An error occurred.')
    }
  }

  const deletePentestReport = async id => {
    try {
      await api.delete('/delete-pentest-report/', {
        data: { id }
      })

      setReports(prevState => ({
        ...prevState,
        pentestReports: prevState.pentestReports.filter(report => report.id !== id)
      }));
    } catch (e) {
      console.error('An error occurred.')
    }
  }

  useEffect(() => {
    fetchReports()
  }, [])

  return (
    <div class={styles.cards}>
      <div class={styles.card}>
        <h2>Code Analysis Reports</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Time</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {reports.reports && (reports.reports.length == 0 ? (
              <p style={{ color: 'white', paddingTop: '8px' }}>No Report created yet</p>
            ) : reports.reports.map(report => (
              <tr style={{ cursor: 'pointer' }} onClick={() => loadReport(report.id)}>
                <td>{report.title}</td>
                <td>{report.time}</td>
                <td style={{ width: '1%' }}>
                  <button onClick={e => {
                    e.stopPropagation()
                    deleteReport(report.id)
                  }}>
                    Delete
                  </button>
                </td>
              </tr>
            )))}
          </tbody>
        </table>
      </div>
      <div class={styles.card}>
        <h2>Pentest Reports</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Time</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {reports.pentestReports && (reports.pentestReports.length == 0 ? (
              <p style={{ color: 'white', paddingTop: '8px' }}>No Report created yet</p>
            ) : reports.pentestReports.map(report => (
              <tr style={{ cursor: 'pointer' }} onClick={() => loadPentestReport(report.id)}>
                <td>{report.title}</td>
                <td>{report.time}</td>
                <td style={{ width: '1%' }}>
                  <button onClick={e => {
                    e.stopPropagation()
                    deletePentestReport(report.id)
                  }}>
                    Delete
                  </button>
                </td>
              </tr>
            )))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
