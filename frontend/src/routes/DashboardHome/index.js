import { Chart } from 'react-google-charts'

import styles from './styles.module.css'

export default function DashboardHome() {
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
    </>
  )
}
