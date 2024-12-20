import styles from './styles.module.css'

const report =
  'Vulnerability Assessment Summary\n\nAnalyzed Function: main\nVulnerabilities Detected:\n- Double-Free: Variable d freed twice (line 7).\n- Use-After-Free: Variable a used after being freed (line 8, originally freed at line 4).\n\nCritical Functions:\n - malloc (lines 3, 5)\n - free (lines 4, 6, 7)\n - printf (line 8)\n\nExtracted CWE:\n - CWE-416: Use After Free\n\nSymbolic Execution Started: Address 0x400000 (vulnerable printf).'

export default function Reports() {
  return (
    <div class={styles.cards}>
      <div class={styles.card}>
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
      <div class={styles.card}>
        <h2>Report</h2>
        <textarea readOnly={true}>{report}</textarea>
        <button>Download</button>
      </div>
    </div>
  )
}
