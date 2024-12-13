import { BrowserRouter as Router, Routes, Route } from 'react-router'
import Loading from './routes/Loading'
import Login from './routes/Login'

import './App.css'

function App() {
  return (
    <div className='App'>
      <Router>
        <Routes>
          <Route index element={<Loading />} />
          <Route path='/login' element={<Login />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
