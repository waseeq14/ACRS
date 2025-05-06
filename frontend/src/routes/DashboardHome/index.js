import { useContext, useEffect } from 'react'
import api from '../../utils/api'
import { AppContext } from '../../context/AppContext'
import { Chart } from 'react-google-charts'
import { useNavigate } from 'react-router'

import styles from './styles.module.css'

export default function DashboardHome() {
  const navigate = useNavigate()

  const { appState, setAppState } = useContext(AppContext)

  const data = [
    ['Vulnerability', 'Occurances'],
    ['Use After Free', 7],
    ['Out-of-bounds Read', 2],
    ['Improper Validation of Array Index', 2],
    ['Buffer Overflow', 5]
  ]

  const options = {
    title: 'Vulnerability Occurance',
    titleColor: 'white',
    backgroundColor: '#2b2a28',
    pieHole: 0.6,
    pieSliceText: 'none',
    legend: {
      textStyle: {
        color: 'white',
        fontSize: 14
      }
    },
    colors: ['#810002', '#D91B1E', '#D46061', '#EDAFB0']
  }

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects/')

      setAppState({
        ...appState,
        pentestProjects: response.data.result.pentestProjects,
        projects: response.data.result.projects
      })
    } catch (e) {
      console.error('An error occurred.')
    }
  }

  const loadPentestProject = async id => {
    try {
      const response = await api.get(`/load-pentest-project?id=${id}`)

      setAppState({
        ...appState,
        pentest: response.data.result.pentest,
        pentestExploit: response.data.result.pentestExploit,
        pentestPatch: response.data.result.pentestPatch
      })

      navigate('/dashboard/pentester-mode')
    } catch (e) {
      console.error('An error occurred.')
    }
  }

  const loadProject = async id => {
    try {
      const response = await api.get(`/load-project?id=${id}`)

      setAppState({
        ...appState,
        filePath: response.data.result.filePath,
        fileContent: response.data.result.fileContent,
        kleeResult:  response.data.result.kleeResult,
        advancedKleeResult: response.data.result.advancedKleeResult,
        fuzzerResult: response.data.result.fuzzerResult,
        rulesResult: response.data.result.rulesResult,
        exploitResult: response.data.result.exploitResult,
        patchResult: response.data.result.patchResult,
      })

      console.log(response.data)

      navigate('/dashboard/va')
    } catch (e) {
      console.log(e)
      console.error('An error occurred.')
    }
  }

  useEffect(() => {
    fetchProjects()
  }, [])

  return (
    <>
      <div className={styles.card}>
        <h2>Last Scan</h2>
        <Chart
          chartType='PieChart'
          data={data}
          options={options}
          width={'100%'}
          height={'400px'}
        />
      </div>
      <div style={{ height: '1rem' }}></div>
      <div className={styles.cards}>
        <div className={styles.card}>
          <h2>Recent Activity</h2>
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>File</th>
                <th>Vulnerability</th>
                <th>Fixed</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>May 1, 2024</td>
                <td>vuln.c</td>
                <td>Out of Bound Access</td>
                <td>Unpatched</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div className={styles.card}>
          <h2>Identified Vulnerabilities</h2>
          <table>
            <thead>
              <tr>
                <th>CWE</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>CWE-120</td>
                <td>Buffer Copy without Checking Size of Input</td>
              </tr>
              <tr>
                <td>CWE-125</td>
                <td>Out-of-bounds Read</td>
              </tr>
              <tr>
                <td>CWE-129</td>
                <td>Improper Validation of Array Index</td>
              </tr>
              <tr>
                <td>CWE-416</td>
                <td>Use After Free</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      {(appState.pentestProjects || appState.projects) && (
        <>
          <div style={{ height: '1rem' }}></div>
          <div className={styles.cards}>
            <div className={styles.card}>
              <h2>Code Analysis Projects</h2>
              <table>
                <tbody>
                  {appState.projects && appState.projects.map(project => (
                    <tr className={styles.grope} key={project.id} onClick={() => loadProject(project.id)}>
                      <td>{project.title}</td>
                    </tr>
                  ))}
                 </tbody>
              </table>
            </div>
            <div className={styles.card}>
              <h2>Pentest Projects</h2>
              <table>
                <tbody>
                  {appState.pentestProjects && appState.pentestProjects.map(project => (
                    <tr className={styles.grope} key={project.id} onClick={() => loadPentestProject(project.id)}>
                      <td>{project.title}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </>
  )
}
