import { BrowserRouter as Router, Routes, Route } from 'react-router'
import Loading from './routes/Loading'
import Login from './routes/Login'
import Register from './routes/Register'
import Dashboard from './routes/Dashboard'

import './App.css'

function App() {
  return (
    <div className='App'>
      <Router>
        <Routes>
          <Route index element={<Loading />} />
          <Route path='/login' element={<Login />} />
          <Route path='/create-account' element={<Register />} />
          <Route path='/dashboard' element={<Dashboard />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
