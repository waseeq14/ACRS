import styles from './styles.module.css'

export default function Dashboard() {
  return (
    <>
      <div className={styles.appbar}>
        <div className={styles.appbarLeft}>
          <img
            className={styles.logo}
            src='/static/images/logo_mini.png'
            alt='Small Logo'
          />
          <h2 className={styles.title}>ACRS</h2>
        </div>
        <div className={styles.menu}>
          <p>admin</p>
          <img
            className={styles.userImg}
            src='/static/images/user.png'
            alt='User'
          />
        </div>
      </div>

      <div className={styles.sidebar}>
        <div className={styles.bar}></div>
        <ul>
          <li>
            <a href='#'>Vulnerability Assessment</a>
          </li>
          <li>
            <a href='#'>Exploit Generation</a>
          </li>
          <li>
            <a href='#'>Patch Suggestion</a>
          </li>
          <li>
            <a href='#'>Pentester Mode</a>
          </li>
          <li>
            <a href='#'>Reports</a>
          </li>
        </ul>
      </div>

      <div className={styles.content}>
        <h1>Dashboard</h1>
      </div>
    </>
  )
}
