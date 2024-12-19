import { NavLink, Outlet } from 'react-router'
import styles from './styles.module.css'

export default function Dashboard({ navigationLinks }) {
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
          {navigationLinks.map(link => (
            <li>
              <NavLink
                className={({ isActive }) => (isActive ? styles.active : '')}
                to={`/dashboard${link.path}`}
                end
              >
                {link.name}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>

      <div className={styles.content}>
        <Outlet />
      </div>
    </>
  )
}
