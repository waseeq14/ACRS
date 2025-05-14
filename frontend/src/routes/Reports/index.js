import { useState, useEffect } from 'react'
import api from '../../utils/api'

import styles from './styles.module.css'

export default function Reports() {
  const [reports, setReports] = useState({})

  const fetchReports = async () => {
    try {
      const response = await api.get('/fetch-reports/')

      console.log(response)

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
            </tr>
          </thead>
          <tbody>
            {reports.reports && (reports.reports.length == 0 ? (
              <p style={{ color: 'white', paddingTop: '8px' }}>No Report created yet</p>
            ) : reports.reports.map(report => (
              <tr style={{ cursor: 'pointer' }} onClick={() => loadReport(report.id)}>
                <td>{report.title}</td>
                <td>{report.time}</td>
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
            </tr>
          </thead>
          <tbody>
            {reports.pentestReports && (reports.pentestReports.length == 0 ? (
              <p style={{ color: 'white', paddingTop: '8px' }}>No Report created yet</p>
            ) : reports.pentestReports.map(report => (
              <tr style={{ cursor: 'pointer' }} onClick={() => loadPentestReport(report.id)}>
                <td>{report.title}</td>
                <td>{report.time}</td>
              </tr>
            )))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
