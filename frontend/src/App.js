import { BrowserRouter as Router, Routes, Route } from 'react-router'
import Loading from './routes/Loading'
import Login from './routes/Login'
import Register from './routes/Register'

import './App.css'

function App() {
  return (
    <div className='App'>
      <Router>
        <Routes>
          <Route index element={<Loading />} />
          <Route path='/login' element={<Login />} />
          <Route path='/create-account' element={<Register />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
